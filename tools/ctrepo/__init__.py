"""Chrono Trigger Repository Remediation Shared Library."""

from .manifest_models import CanonicalManifest, ClosedRange
from .manifest_adapters import adapt_to_canonical, detect_schema_family
from .manifest_discovery import (
    discover_manifest_candidates,
    iter_canonical_manifests,
    extract_pass_from_filename,
    is_canonical_filename,
    ManifestDiscoveryResult
)
from .manifest_validation import validate_manifest, validate_manifest_schema, validate_manifest_semantics
from .range_model import detect_range_conflicts, compute_byte_union, RangeConflict
from .provenance import create_provenance_header, calculate_manifest_set_digest, get_git_provenance

__all__ = [
    "CanonicalManifest",
    "ClosedRange",
    "adapt_to_canonical",
    "detect_schema_family",
    "discover_manifest_candidates",
    "iter_canonical_manifests",
    "extract_pass_from_filename",
    "is_canonical_filename",
    "ManifestDiscoveryResult",
    "validate_manifest",
    "validate_manifest_schema",
    "validate_manifest_semantics",
    "detect_range_conflicts",
    "compute_byte_union",
    "RangeConflict",
    "create_provenance_header",
    "calculate_manifest_set_digest",
    "get_git_provenance",
]
