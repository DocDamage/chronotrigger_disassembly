#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tarfile
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from xref_index_utils_v1 import (
    build_xref_entries,
    export_closed_ranges_snapshot,
    load_xref_index,
    rom_sha256,
    write_xref_index,
)


def count_manifest_files(manifests_dir: Path) -> int:
    return sum(1 for p in manifests_dir.glob('pass*.json') if p.is_file())


def workspace_ready(repo_root: Path, manifests_rel: str, minimum_manifests: int) -> dict[str, Any]:
    manifests_dir = repo_root / manifests_rel
    manifest_count = count_manifest_files(manifests_dir) if manifests_dir.exists() else 0
    return {
        'repo_root': str(repo_root),
        'manifests_dir': str(manifests_dir),
        'repo_root_exists': repo_root.exists(),
        'git_dir_exists': (repo_root / '.git').exists(),
        'manifests_dir_exists': manifests_dir.exists(),
        'manifest_count': manifest_count,
        'minimum_manifests_required': minimum_manifests,
        'workspace_ready': manifest_count >= minimum_manifests,
    }


def run_git(args: list[str], cwd: Path) -> tuple[bool, str]:
    try:
        proc = subprocess.run(
            ['git', *args],
            cwd=str(cwd),
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return False, 'git executable not found'
    out = '\n'.join(x for x in [proc.stdout.strip(), proc.stderr.strip()] if x).strip()
    return proc.returncode == 0, out


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def copy_tree_contents(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)


def find_manifest_root(search_root: Path) -> Path | None:
    direct = search_root / 'passes' / 'manifests'
    if direct.exists() and count_manifest_files(direct) > 0:
        return direct
    for candidate in search_root.rglob('passes/manifests'):
        if candidate.is_dir() and count_manifest_files(candidate) > 0:
            return candidate
    for candidate in search_root.rglob('manifests'):
        if candidate.is_dir() and count_manifest_files(candidate) > 0:
            return candidate
    return None


def restore_manifests_from_source(source: Path, repo_root: Path, manifests_rel: str) -> tuple[bool, str]:
    manifests_target = repo_root / manifests_rel
    ensure_parent(manifests_target)

    if source.is_dir():
        manifest_root = find_manifest_root(source)
        if manifest_root is None:
            return False, f'no manifest directory found inside {source}'
        shutil.rmtree(manifests_target, ignore_errors=True)
        copy_tree_contents(manifest_root, manifests_target)
        return True, f'restored manifests from directory source {source}'

    if source.is_file() and zipfile.is_zipfile(source):
        with tempfile.TemporaryDirectory(prefix='ct_manifest_zip_') as tmp:
            tmp_path = Path(tmp)
            with zipfile.ZipFile(source) as zf:
                zf.extractall(tmp_path)
            manifest_root = find_manifest_root(tmp_path)
            if manifest_root is None:
                return False, f'no manifest directory found inside zip {source}'
            shutil.rmtree(manifests_target, ignore_errors=True)
            copy_tree_contents(manifest_root, manifests_target)
        return True, f'restored manifests from zip bundle {source}'

    if source.is_file() and tarfile.is_tarfile(source):
        with tempfile.TemporaryDirectory(prefix='ct_manifest_tar_') as tmp:
            tmp_path = Path(tmp)
            with tarfile.open(source) as tf:
                tf.extractall(tmp_path)
            manifest_root = find_manifest_root(tmp_path)
            if manifest_root is None:
                return False, f'no manifest directory found inside tar bundle {source}'
            shutil.rmtree(manifests_target, ignore_errors=True)
            copy_tree_contents(manifest_root, manifests_target)
        return True, f'restored manifests from tar bundle {source}'

    return False, f'unsupported manifest source {source}'


def try_checkout_repo(repo_root: Path, repo_url: str, branch: str) -> tuple[bool, str]:
    if (repo_root / '.git').exists():
        ok_fetch, out_fetch = run_git(['fetch', 'origin', branch, '--depth', '1'], repo_root)
        ok_checkout, out_checkout = run_git(['checkout', branch], repo_root)
        ok_reset, out_reset = run_git(['reset', '--hard', f'origin/{branch}'], repo_root)
        ok = ok_fetch and ok_checkout and ok_reset
        joined = '\n'.join(x for x in [out_fetch, out_checkout, out_reset] if x).strip()
        return ok, joined or 'updated existing checkout'

    if repo_root.exists() and any(repo_root.iterdir()):
        return False, f'target repo root {repo_root} exists and is not empty; refusing clone over existing files'

    repo_root.parent.mkdir(parents=True, exist_ok=True)
    ok_clone, out_clone = run_git(['clone', '--branch', branch, '--depth', '1', repo_url, str(repo_root)], repo_root.parent)
    return ok_clone, out_clone or 'cloned repository'


def ensure_cache(rom: Path, manifests_dir: Path, cache_dir: Path, xref_index_name: str, closed_ranges_name: str) -> dict[str, Any]:
    rom_bytes = rom.read_bytes()
    current_sha = rom_sha256(rom_bytes)

    cache_dir.mkdir(parents=True, exist_ok=True)
    xref_index_path = cache_dir / xref_index_name
    closed_ranges_path = cache_dir / closed_ranges_name

    xref_rebuilt = False
    if xref_index_path.exists():
        try:
            payload = load_xref_index(xref_index_path)
            indexed_sha = str(payload.get('rom_sha256', ''))
            if indexed_sha != current_sha:
                raise ValueError('rom sha mismatch')
        except Exception:
            entries = build_xref_entries(rom_bytes)
            write_xref_index(xref_index_path, rom_bytes, entries)
            xref_rebuilt = True
    else:
        entries = build_xref_entries(rom_bytes)
        write_xref_index(xref_index_path, rom_bytes, entries)
        xref_rebuilt = True

    snapshot_rebuilt = False
    if not closed_ranges_path.exists():
        export_closed_ranges_snapshot(closed_ranges_path, manifests_dir)
        snapshot_rebuilt = True

    return {
        'rom': str(rom),
        'rom_sha256': current_sha,
        'cache_dir': str(cache_dir),
        'xref_index_path': str(xref_index_path),
        'closed_ranges_snapshot_path': str(closed_ranges_path),
        'xref_index_rebuilt': xref_rebuilt,
        'closed_ranges_snapshot_rebuilt': snapshot_rebuilt,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Prepare the seam workspace by attempting a full git checkout first and falling back to manifest bundle restoration if needed.'
    )
    parser.add_argument('--repo-root', default='.')
    parser.add_argument('--repo-url', default='https://github.com/DocDamage/chronotrigger_disassembly.git')
    parser.add_argument('--branch', default='live-work-from-pass166')
    parser.add_argument('--rom', required=True)
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--cache-dir', default='tools/cache')
    parser.add_argument('--xref-index-name', default='chrono_trigger_raw_xref_index_v1.json')
    parser.add_argument('--closed-ranges-name', default='closed_ranges_snapshot_v1.json')
    parser.add_argument('--minimum-manifests', type=int, default=100)
    parser.add_argument('--manifest-source', action='append', default=[])
    parser.add_argument('--skip-git', action='store_true')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    rom_path = Path(args.rom).resolve()
    manifests_dir = repo_root / args.manifests_dir
    cache_dir = repo_root / args.cache_dir

    steps: list[dict[str, Any]] = []
    ready = workspace_ready(repo_root, args.manifests_dir, args.minimum_manifests)

    if not ready['workspace_ready'] and not args.skip_git:
        ok_git, git_message = try_checkout_repo(repo_root, args.repo_url, args.branch)
        steps.append({'step': 'git_checkout', 'ok': ok_git, 'message': git_message})
        ready = workspace_ready(repo_root, args.manifests_dir, args.minimum_manifests)

    bootstrap_used = False
    if not ready['workspace_ready']:
        for source_text in args.manifest_source:
            source = Path(source_text).resolve()
            ok_restore, restore_message = restore_manifests_from_source(source, repo_root, args.manifests_dir)
            steps.append({'step': 'manifest_bootstrap', 'source': str(source), 'ok': ok_restore, 'message': restore_message})
            if ok_restore:
                bootstrap_used = True
                ready = workspace_ready(repo_root, args.manifests_dir, args.minimum_manifests)
                if ready['workspace_ready']:
                    break

    result: dict[str, Any] = {
        'ok': False,
        'repo_root': str(repo_root),
        'branch': args.branch,
        'workspace': ready,
        'bootstrap_used': bootstrap_used,
        'steps': steps,
    }

    if ready['workspace_ready'] and rom_path.exists():
        result['cache'] = ensure_cache(
            rom_path,
            manifests_dir,
            cache_dir,
            args.xref_index_name,
            args.closed_ranges_name,
        )
        result['ok'] = True
        result['message'] = 'workspace ready; seam cache ensured'
    else:
        if not rom_path.exists():
            result['message'] = f'workspace not ready: ROM missing at {rom_path}'
        else:
            result['message'] = 'workspace not ready: full checkout failed and no usable manifest bundle restored'

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for key, value in result.items():
            print(f'{key}: {value}')

    return 0 if result['ok'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
