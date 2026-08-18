"""Provenance metadata, hashing, and report signing."""

import hashlib
import json
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
from .manifest_models import CanonicalManifest

def calculate_manifest_set_digest(manifests: List[CanonicalManifest]) -> str:
    """Calculate a deterministic SHA-256 digest over all manifests sorted by pass number."""
    h = hashlib.sha256()
    for m in sorted(manifests, key=lambda x: x.pass_number):
        serialized = json.dumps(m.to_dict(), sort_keys=True)
        h.update(serialized.encode('utf-8'))
    return h.hexdigest()

def get_git_provenance() -> Dict[str, Any]:
    """Retrieve current Git commit, tree, branch, and dirty status."""
    try:
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        commit = "unknown"

    try:
        tree = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}'], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        tree = "unknown"
        
    try:
        branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        branch = "unknown"

    try:
        status_out = subprocess.check_output(['git', 'status', '--porcelain'], stderr=subprocess.DEVNULL).decode().strip()
        is_dirty = len(status_out) > 0
    except Exception:
        is_dirty = True

    return {
        "source_commit": commit,
        "source_tree": tree,
        "git_commit": commit,
        "git_branch": branch,
        "is_dirty": is_dirty,
        "worktree_clean_before_generation": not is_dirty
    }

def create_provenance_header(
    generator_name: str,
    manifests: Optional[List[CanonicalManifest]] = None,
    extra: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create standard provenance block for all generated reports."""
    git_info = get_git_provenance()
    header = {
        "generator": generator_name,
        "generation_command": shlex.join(["python", *sys.argv]),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_commit": git_info["source_commit"],
        "source_tree": git_info["source_tree"],
        "git_commit": git_info["git_commit"],
        "git_branch": git_info["git_branch"],
        "is_dirty_worktree": git_info["is_dirty"],
        "worktree_clean_before_generation": git_info["worktree_clean_before_generation"],
        "report_schema_version": 2
    }
    root = Path(__file__).resolve().parent.parent.parent
    generator_candidates = [root / generator_name, root / "tools" / "scripts" / generator_name]
    generator_path = next((path for path in generator_candidates if path.is_file()), None)
    if generator_path is not None:
        header["generator_source_digest"] = hashlib.sha256(generator_path.read_bytes()).hexdigest()
    if manifests is not None:
        header["manifest_count"] = len(manifests)
        header["manifest_set_digest"] = calculate_manifest_set_digest(manifests)
    else:
        # Compute digest from existing canonical manifests if discoverable
        try:
            from .manifest_discovery import iter_canonical_manifests
            discovered = list(iter_canonical_manifests())
            header["manifest_count"] = len(discovered)
            header["manifest_set_digest"] = calculate_manifest_set_digest(discovered)
        except Exception:
            header["manifest_count"] = 0
            header["manifest_set_digest"] = hashlib.sha256(b"empty").hexdigest()
        
    if extra:
        header.update(extra)
        
    return header
