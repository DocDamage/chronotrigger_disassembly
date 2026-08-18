#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from continuation_note_utils_v1 import latest_continuation_note_summary
from snes_utils import iter_manifest_paths, load_manifest, manifest_pass_number


README_BRANCH_RE = re.compile(r"working branch:\s*`([^`]+)`", re.IGNORECASE)
README_PASS_RE = re.compile(r"latest manifest-backed pass:\s*`?(\d+)`?", re.IGNORECASE)
README_NOTE_RE = re.compile(r"latest continuation(?:-note snapshot| note):\s*`([^`]+)`", re.IGNORECASE)
README_SEAM_RE = re.compile(r"current forward seam:\s*`([^`]+)`", re.IGNORECASE)

DEFAULT_INCLUDE_FILES = (
    "README.md",
    "LICENSE",
    "docs/session_23_progress_report.md",
)

DEFAULT_INCLUDE_DIRS = (
    "tools",
    "passes",
    "reports",
    "docs/handoffs",
    "docs/sessions",
    "templates",
)

SKIP_DIR_NAMES = {
    ".git",
    "__pycache__",
}

SKIP_SUFFIXES = {
    ".pyc",
    ".pyo",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a repo-native toolkit release zip plus release manifest.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output-dir", default="toolkits/repo_native")
    parser.add_argument("--reports-dir", default="reports")
    return parser.parse_args()


def read_text_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def find_readme_value(pattern: re.Pattern[str], text: str) -> str:
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def git_branch(repo_root: Path) -> str:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
        return completed.stdout.strip()
    except Exception:
        return ""


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def max_manifest_pass(manifests_dir: Path) -> int:
    max_pass = 0
    for path in iter_manifest_paths(manifests_dir):
        data = load_manifest(path)
        max_pass = max(max_pass, manifest_pass_number(data, path))
    return max_pass


def manifest_count(manifests_dir: Path) -> int:
    return sum(1 for _ in iter_manifest_paths(manifests_dir))


def load_closed_range_counts(repo_root: Path) -> dict[str, int]:
    snapshot_path = repo_root / "tools" / "cache" / "closed_ranges_snapshot_v1.json"
    if not snapshot_path.exists():
        return {
            "total": 0,
            "manifest_backed": 0,
            "continuation": 0,
        }
    data = json.loads(snapshot_path.read_text(encoding="utf-8"))
    if "range_count" in data or "manifest_range_count" in data or "continuation_range_count" in data:
        return {
            "total": int(data.get("range_count", 0)),
            "manifest_backed": int(data.get("manifest_range_count", 0)),
            "continuation": int(data.get("continuation_range_count", 0)),
        }
    return {
        "total": len(data.get("ranges", [])),
        "manifest_backed": sum(1 for item in data.get("ranges", []) if item.get("source") == "manifest"),
        "continuation": sum(1 for item in data.get("ranges", []) if item.get("source") == "continuation_note"),
    }


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts) or path.suffix.lower() in SKIP_SUFFIXES


def should_skip_relative(rel_path: str) -> bool:
    return rel_path.startswith("reports/toolkit_release_manifest_")


def iter_payload_paths(repo_root: Path) -> list[Path]:
    payload: dict[str, Path] = {}

    for rel_text in DEFAULT_INCLUDE_FILES:
        path = repo_root / rel_text
        if path.is_file():
            rel_path = path.relative_to(repo_root).as_posix()
            if not should_skip_relative(rel_path):
                payload[rel_path] = path

    for rel_text in DEFAULT_INCLUDE_DIRS:
        base = repo_root / rel_text
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or should_skip(path):
                continue
            rel_path = path.relative_to(repo_root).as_posix()
            if should_skip_relative(rel_path):
                continue
            payload[rel_path] = path

    return [payload[key] for key in sorted(payload)]


def build_release_id(latest_pass: int, note_number: int | None) -> str:
    release_id = f"pass{latest_pass}"
    if note_number is not None:
        release_id += f"_note{note_number}"
    return release_id


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    reports_dir = (repo_root / args.reports_dir).resolve()
    output_dir = (repo_root / args.output_dir).resolve()
    reports_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    readme_text = read_text_if_exists(repo_root / "README.md")
    branch = git_branch(repo_root) or find_readme_value(README_BRANCH_RE, readme_text) or "unknown"
    readme_latest_pass = find_readme_value(README_PASS_RE, readme_text)
    readme_latest_note = find_readme_value(README_NOTE_RE, readme_text)
    readme_current_seam = find_readme_value(README_SEAM_RE, readme_text)

    manifests_dir = repo_root / "passes" / "manifests"
    latest_pass = max_manifest_pass(manifests_dir)
    total_manifests = manifest_count(manifests_dir)

    latest_note = latest_continuation_note_summary(repo_root / "docs" / "sessions")
    latest_note_number = latest_note.note_number if latest_note else None
    latest_note_path = latest_note.source_path if latest_note else ""
    note_live_seam = latest_note.live_seam if latest_note else ""

    effective_seam = readme_current_seam or note_live_seam or ""
    range_counts = load_closed_range_counts(repo_root)

    release_id = build_release_id(latest_pass, latest_note_number)
    root_name = f"ct_repo_native_toolkit_{release_id}_release"
    zip_path = output_dir / f"{root_name}.zip"
    manifest_json_path = reports_dir / f"toolkit_release_manifest_{release_id}.json"
    manifest_md_path = reports_dir / f"toolkit_release_manifest_{release_id}.md"

    payload_paths = iter_payload_paths(repo_root)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for path in payload_paths:
            rel_path = path.relative_to(repo_root).as_posix()
            zf.write(path, arcname=f"{root_name}/{rel_path}")

    zip_sha256 = sha256_path(zip_path)
    zip_size_bytes = zip_path.stat().st_size

    manifest_data = {
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "branch": branch,
        "latest_manifest_pass": latest_pass,
        "manifest_count": total_manifests,
        "readme_latest_manifest_pass": int(readme_latest_pass) if readme_latest_pass else None,
        "latest_continuation_note_number": latest_note_number,
        "latest_continuation_note_path": str(Path(latest_note_path).relative_to(repo_root).as_posix()) if latest_note_path else None,
        "readme_latest_continuation_note": readme_latest_note or None,
        "readme_current_forward_seam": readme_current_seam or None,
        "note_backed_live_seam": note_live_seam or None,
        "effective_live_seam": effective_seam or None,
        "closed_range_counts": range_counts,
        "payload": {
            "root_name": root_name,
            "included_top_level_entries": list(DEFAULT_INCLUDE_FILES) + list(DEFAULT_INCLUDE_DIRS),
            "file_count": len(payload_paths),
        },
        "outputs": {
            "zip_path": str(zip_path.relative_to(repo_root).as_posix()),
            "zip_sha256": zip_sha256,
            "zip_size_bytes": zip_size_bytes,
            "manifest_json_path": str(manifest_json_path.relative_to(repo_root).as_posix()),
            "manifest_md_path": str(manifest_md_path.relative_to(repo_root).as_posix()),
        },
    }

    md_lines = [
        "# Repo-Native Toolkit Release Manifest",
        "",
        f"- branch: **{branch}**",
        f"- latest manifest pass: **{latest_pass}**",
        f"- manifest count: **{total_manifests}**",
        f"- latest continuation note: **{str(Path(latest_note_path).relative_to(repo_root).as_posix()) if latest_note_path else '(none)'}**",
        f"- effective live seam: **`{effective_seam or '(unknown)'}`**",
        f"- closed ranges: **{range_counts['total']} total** ({range_counts['manifest_backed']} manifest-backed, {range_counts['continuation']} continuation-note-backed)",
        f"- release zip: `{zip_path.relative_to(repo_root).as_posix()}`",
        f"- release root: `{root_name}`",
        f"- zip sha256: `{zip_sha256}`",
        f"- zip size bytes: `{zip_size_bytes}`",
        "",
        "## Payload",
        "",
        "- `README.md`",
        "- `LICENSE`",
        "- `docs/session_23_progress_report.md`",
        "- `tools/`",
        "- `passes/`",
        "- `reports/`",
        "- `docs/handoffs/`",
        "- `docs/sessions/`",
        "- `templates/`",
    ]

    write_text(manifest_json_path, json.dumps(manifest_data, indent=2) + "\n")
    write_text(manifest_md_path, "\n".join(md_lines) + "\n")

    print(str(zip_path.relative_to(repo_root)))
    print(str(manifest_json_path.relative_to(repo_root)))
    print(str(manifest_md_path.relative_to(repo_root)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
