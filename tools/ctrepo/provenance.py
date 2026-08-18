"""Provenance metadata, hashing, and report signing."""

import hashlib
import json
import subprocess
from datetime import datetime, timezone
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
    """Retrieve current Git commit, branch, and dirty status."""
    try:
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        commit = "unknown"
        
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
        "git_commit": commit,
        "git_branch": branch,
        "is_dirty": is_dirty
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
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_info["git_commit"],
        "git_branch": git_info["git_branch"],
        "is_dirty_worktree": git_info["is_dirty"],
        "schema_version": 2
    }
    if manifests is not None:
        header["manifest_count"] = len(manifests)
        header["manifest_set_digest"] = calculate_manifest_set_digest(manifests)
        
    if extra:
        header.update(extra)
        
    return header
