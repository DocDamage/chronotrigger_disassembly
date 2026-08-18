"""Schema and semantic validation for CanonicalManifest objects."""

import json
import os
from typing import List, Dict, Any, Tuple
import jsonschema
from .manifest_models import CanonicalManifest

SCHEMA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "pass_manifest_schema.json")

def load_canonical_schema() -> Dict[str, Any]:
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

_CACHED_SCHEMA = None

def get_schema() -> Dict[str, Any]:
    global _CACHED_SCHEMA
    if _CACHED_SCHEMA is None:
        _CACHED_SCHEMA = load_canonical_schema()
    return _CACHED_SCHEMA

def validate_manifest_schema(manifest_dict: Dict[str, Any]) -> List[str]:
    """Validate raw or dictionary manifest against canonical JSON schema."""
    schema = get_schema()
    validator = jsonschema.Draft202012Validator(schema)
    errors = []
    for err in validator.iter_errors(manifest_dict):
        errors.append(f"{err.json_path}: {err.message}")
    return errors

def validate_manifest_semantics(manifest: CanonicalManifest) -> List[str]:
    """Perform deep semantic validation of a CanonicalManifest instance."""
    errors = []
    
    if manifest.pass_number <= 0:
        errors.append(f"pass_number must be positive (got {manifest.pass_number})")

    if not manifest.closed_ranges:
        errors.append(f"Pass {manifest.pass_number} contains 0 closed ranges")

    for i, r in enumerate(manifest.closed_ranges):
        if r.start_addr > r.end_addr:
            errors.append(f"Range {i} ({r.range_str}): start 0x{r.start_addr:04X} > end 0x{r.end_addr:04X}")
        if r.start_addr < 0 or r.end_addr > 0xFFFF:
            errors.append(f"Range {i} ({r.range_str}): address out of 16-bit bounds")
        if not r.label:
            errors.append(f"Range {i} ({r.range_str}): missing label")

    return errors

def validate_manifest(manifest: CanonicalManifest, strict: bool = True) -> Tuple[bool, List[str]]:
    """Run both schema and semantic validation."""
    m_dict = manifest.to_dict()
    schema_errs = validate_manifest_schema(m_dict)
    semantic_errs = validate_manifest_semantics(manifest)
    all_errs = schema_errs + semantic_errs
    return len(all_errs) == 0, all_errs
