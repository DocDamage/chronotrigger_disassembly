"""Manifest candidate discovery and iteration."""

import os
import re
import json
from typing import List, Dict, Tuple, Optional, Iterator, NamedTuple
from .manifest_models import CanonicalManifest
from .manifest_adapters import adapt_to_canonical, detect_schema_family

class ManifestDiscoveryResult(NamedTuple):
    manifest: Optional[CanonicalManifest]
    source_path: str
    filename: str
    is_canonical_filename: bool
    is_valid_json: bool
    schema_family: str
    pass_number: Optional[int]
    error: Optional[str]

def extract_pass_from_filename(filename: str) -> Optional[int]:
    """Extract pass integer from filename (e.g. pass0100.json -> 100, pass1229_c3_cb47.json -> 1229)."""
    m = re.match(r'^pass(\d+)', filename, re.IGNORECASE)
    return int(m.group(1)) if m else None

def is_canonical_filename(filename: str) -> bool:
    """Check if filename strictly matches passNNNN.json or passNNN.json."""
    return bool(re.match(r'^pass\d{3,5}\.json$', filename, re.IGNORECASE))

def read_json_safely(path: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
    """Attempt to decode JSON supporting UTF-8, UTF-8 BOM, and UTF-16."""
    try:
        with open(path, 'rb') as f:
            raw = f.read()
    except Exception as e:
        return False, None, f"IO error reading file: {e}"

    if len(raw) == 0:
        return False, None, "File is empty"

    if raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]
    elif raw.startswith(b'\xff\xfe'):
        try:
            return True, json.loads(raw[2:].decode('utf-16-le')), None
        except Exception as e:
            return False, None, f"UTF-16-LE decode error: {e}"
    elif raw.startswith(b'\xfe\xff'):
        try:
            return True, json.loads(raw[2:].decode('utf-16-be')), None
        except Exception as e:
            return False, None, f"UTF-16-BE decode error: {e}"

    try:
        return True, json.loads(raw.decode('utf-8')), None
    except UnicodeDecodeError:
        try:
            return True, json.loads(raw.decode('latin-1')), None
        except Exception as e:
            return False, None, f"Decode error: {e}"
    except json.JSONDecodeError as e:
        return False, None, f"JSON parse error: {e}"


def discover_manifest_candidates(
    manifests_dir: str = "passes/manifests",
    allow_legacy_schemas: bool = True
) -> List[ManifestDiscoveryResult]:
    """Discover all manifest files in the target directory."""
    if not os.path.exists(manifests_dir):
        return []

    results: List[ManifestDiscoveryResult] = []
    for fn in os.listdir(manifests_dir):
        path = os.path.join(manifests_dir, fn)
        if not os.path.isfile(path) or not fn.endswith('.json'):
            continue
        if fn.startswith('manifest_migration_map') or fn.startswith('package'):
            continue

        fn_pass = extract_pass_from_filename(fn)
        is_canon_fn = is_canonical_filename(fn)

        is_valid_json, data, err = read_json_safely(path)
        if not is_valid_json:
            results.append(ManifestDiscoveryResult(
                manifest=None,
                source_path=path,
                filename=fn,
                is_canonical_filename=is_canon_fn,
                is_valid_json=False,
                schema_family="invalid_json",
                pass_number=fn_pass,
                error=err
            ))
            continue

        fam = detect_schema_family(data)
        if fam in ("invalid", "scan_report"):
            results.append(ManifestDiscoveryResult(
                manifest=None,
                source_path=path,
                filename=fn,
                is_canonical_filename=is_canon_fn,
                is_valid_json=True,
                schema_family=fam,
                pass_number=fn_pass,
                error=f"Non-manifest schema family '{fam}'"
            ))
            continue

        try:
            manifest = adapt_to_canonical(data, source_path=path, filename_pass=fn_pass)
            results.append(ManifestDiscoveryResult(
                manifest=manifest,
                source_path=path,
                filename=fn,
                is_canonical_filename=is_canon_fn,
                is_valid_json=True,
                schema_family=fam,
                pass_number=manifest.pass_number,
                error=None
            ))
        except Exception as e:
            results.append(ManifestDiscoveryResult(
                manifest=None,
                source_path=path,
                filename=fn,
                is_canonical_filename=is_canon_fn,
                is_valid_json=True,
                schema_family=fam,
                pass_number=fn_pass,
                error=str(e)
            ))

    # Sort deterministically by integer pass number, then filename
    results.sort(key=lambda r: (r.pass_number if r.pass_number is not None else 999999, r.filename))
    return results


def iter_canonical_manifests(
    manifests_dir: str = "passes/manifests",
    strict: bool = True
) -> Iterator[CanonicalManifest]:
    """Yield all valid canonical manifests sorted numerically."""
    results = discover_manifest_candidates(manifests_dir=manifests_dir)
    seen_passes: Dict[int, str] = {}

    for res in results:
        if res.error:
            if strict:
                raise ValueError(f"Manifest error in {res.source_path}: {res.error}")
            continue

        if res.manifest is None:
            continue

        p_num = res.manifest.pass_number
        if p_num in seen_passes:
            if strict:
                raise ValueError(f"Duplicate pass identity {p_num} in {res.source_path} (previous: {seen_passes[p_num]})")
            continue

        seen_passes[p_num] = res.source_path
        yield res.manifest
