"""Adapters to normalize historical and heterogeneous manifest formats into CanonicalManifest."""

from typing import Dict, Any, Optional, List
import re
from .manifest_models import CanonicalManifest, ClosedRange

def detect_schema_family(data: Any) -> str:
    """Classify the schema family of a raw parsed dictionary."""
    if not isinstance(data, dict):
        return "invalid"
        
    if data.get("schema_version") == 2 and "closed_ranges" in data:
        return "canonical_v2"
        
    if "closed_ranges" in data and isinstance(data["closed_ranges"], list):
        return "canonical_v1"
        
    if "targets" in data and isinstance(data["targets"], list):
        return "legacy_targets"
        
    if any(k in data for k in ("promotions", "promoted_functions", "promoted")):
        return "promotions"
        
    if any(k in data for k in ("function_range", "range", "start_address", "addr")):
        return "single_function"
        
    if any(k in data for k in ("scanned_pages", "scan_results", "candidates")):
        return "scan_report"
        
    return "unknown"


def adapt_to_canonical(
    data: Dict[str, Any],
    source_path: Optional[str] = None,
    filename_pass: Optional[int] = None
) -> CanonicalManifest:
    """Adapt any recognized manifest dictionary into a CanonicalManifest model."""
    schema_fam = detect_schema_family(data)
    
    if schema_fam == "invalid":
        raise ValueError(f"Data is not a dictionary: {data}")
    if schema_fam == "scan_report":
        raise ValueError(f"File appears to be a scan report rather than a manifest: {source_path}")
    if schema_fam == "unknown":
        raise ValueError(f"Unknown schema family in {source_path}: keys={list(data.keys())}")
        
    # Extract pass identity
    pass_raw = data.get("pass_number") or data.get("pass") or data.get("pass_id") or data.get("pass_num") or filename_pass
    if isinstance(pass_raw, str):
        m_p = re.search(r'\d+', pass_raw)
        pass_number = int(m_p.group(0)) if m_p else filename_pass
    else:
        pass_number = int(pass_raw) if pass_raw is not None else filename_pass
        
    if pass_number is None:
        raise ValueError(f"Could not determine pass_number for manifest at {source_path}")

    branch = data.get("branch", "live-work-from-pass166")
    status = data.get("status", "reviewed")
    toolkit_version = data.get("toolkit_version", "repo-native-vNext")
    rom_sha256 = data.get("rom_sha256", "06d1c2b06b716052c5596aaa0c2e5632a027fee1a9a28439e509f813c30829a9")
    live_seam = data.get("live_seam_after_pass")
    completion_est = data.get("completion_estimate")
    
    # Confidence dictionary
    raw_conf = data.get("confidence")
    if isinstance(raw_conf, dict):
        confidence = {
            "structural": raw_conf.get("structural", "medium"),
            "semantic": raw_conf.get("semantic", "medium"),
            "rebuild": raw_conf.get("rebuild", "low")
        }
    else:
        confidence = {"structural": "medium", "semantic": "medium", "rebuild": "low"}

    closed_ranges: List[ClosedRange] = []
    new_labels: List[str] = []
    notes: List[str] = data.get("notes", []) if isinstance(data.get("notes"), list) else []
    sources: Dict[str, str] = data.get("sources", {}) if isinstance(data.get("sources"), dict) else {}
    legacy_meta: Dict[str, Any] = {}

    if schema_fam in ("canonical_v1", "canonical_v2"):
        for item in data.get("closed_ranges", []):
            if isinstance(item, dict):
                r_str = item.get("range") or item.get("address_range")
                if r_str:
                    cr = ClosedRange.parse(
                        range_str=r_str,
                        kind=item.get("kind", "code_owner"),
                        label=item.get("label", ""),
                        confidence=item.get("confidence", "medium"),
                        verification_status=item.get("verification_status"),
                        parent_range=item.get("parent_range"),
                        parent_label=item.get("parent_label"),
                        evidence=item.get("evidence", {}),
                        legacy_metadata=item.get("legacy_metadata", {})
                    )
                    closed_ranges.append(cr)
                    if cr.label:
                        new_labels.append(cr.label)
                        
    elif schema_fam == "legacy_targets":
        for item in data.get("targets", []):
            if isinstance(item, dict):
                r_str = item.get("range") or item.get("address_range")
                if not r_str and "start_address" in item and "end_address" in item:
                    r_str = f"{item['start_address']}..{item['end_address']}"
                if not r_str and "addr" in item:
                    addr_str = item["addr"].strip().upper()
                    cov = int(item.get("coverage_bytes") or data.get("coverage_bytes") or 1)
                    if ":" in addr_str:
                        bank, s_hex = addr_str.split(":", 1)
                        s_addr = int(s_hex, 16)
                        e_addr = s_addr + cov - 1
                        r_str = f"{bank}:{s_addr:04X}..{bank}:{e_addr:04X}"
                if r_str:
                    raw_kind = item.get("kind") or item.get("type") or "code_owner"
                    label = item.get("label") or item.get("name") or item.get("symbol") or ""
                    conf = item.get("confidence", "medium")
                    cr = ClosedRange.parse(
                        range_str=r_str,
                        kind=raw_kind,
                        label=label,
                        confidence=conf,
                        legacy_metadata={"raw_target": item}
                    )
                    closed_ranges.append(cr)
                    if cr.label:
                        new_labels.append(cr.label)
                        
    elif schema_fam == "promotions":
        items = data.get("promotions") or data.get("promoted_functions") or data.get("promoted") or []
        for item in items:
            if isinstance(item, dict):
                r_str = item.get("function_range") or item.get("range")
                if not r_str and "start_address" in item and "end_address" in item:
                    r_str = f"{item['start_address']}..{item['end_address']}"
                if not r_str and "addr" in item and "end" in item:
                    r_str = f"{item['addr']}..{item['end']}"
                if not r_str and "addr" in item:
                    r_str = item.get("addr")
                    if r_str and ".." not in r_str:
                        b, s = r_str.split(":")
                        r_str = f"{b}:{int(s,16):04X}..{b}:{int(s,16)+0x1F:04X}"
                if r_str:
                    label = item.get("name") or item.get("label") or ""
                    v_stat = item.get("verification_status", "reviewed")
                    if v_stat == "pending_final_review":
                        v_stat = "reviewed"
                    score_val = item.get("score")
                    conf = "high" if (score_val and ("score-6" in str(score_val) or score_val == 6)) else item.get("confidence", "medium")
                    cr = ClosedRange.parse(
                        range_str=r_str,
                        kind="code_owner",
                        label=label,
                        confidence=conf,
                        verification_status=v_stat,
                        evidence=item.get("evidence") or {"reason": item.get("reason"), "source": item.get("source")},
                        legacy_metadata={"raw_promotion": item}
                    )
                    closed_ranges.append(cr)
                    if cr.label:
                        new_labels.append(cr.label)
                        
        for item in data.get("frozen_ranges", []):
            if isinstance(item, dict) and "range" in item:
                cr = ClosedRange.parse(
                    range_str=item["range"],
                    kind="data",
                    label=item.get("label", ""),
                    confidence="medium",
                    verification_status="reviewed",
                    legacy_metadata={"raw_frozen": item}
                )
                closed_ranges.append(cr)
                if cr.label:
                    new_labels.append(cr.label)
                        
    elif schema_fam == "single_function":
        r_str = data.get("function_range") or data.get("range")
        if not r_str and "start_address" in data and "end_address" in data:
            r_str = f"{data['start_address']}..{data['end_address']}"
        if not r_str and "addr" in data and "end" in data:
            r_str = f"{data['addr']}..{data['end']}"
        if not r_str and "addr" in data and "size" in data:
            addr_str = data["addr"].strip().upper()
            if ":" in addr_str:
                b, s_h = addr_str.split(":", 1)
                s_a = int(s_h, 16)
                e_a = s_a + int(data["size"]) - 1
                r_str = f"{b}:{s_a:04X}..{b}:{e_a:04X}"
        if r_str:
            label = data.get("name") or data.get("label") or ""
            cr = ClosedRange.parse(
                range_str=r_str,
                kind=data.get("kind") or data.get("type", "code_owner"),
                label=label,
                confidence=data.get("confidence", "medium"),
                verification_status=data.get("verification_status", "reviewed"),
                legacy_metadata={"raw_single_function": True}
            )
            closed_ranges.append(cr)
            if cr.label:
                new_labels.append(cr.label)

    # Record source path in sources
    if source_path:
        sources["source_manifest"] = source_path.replace("\\", "/")

    return CanonicalManifest(
        pass_number=pass_number,
        schema_version=2,
        status=status,
        branch=branch,
        toolkit_version=toolkit_version,
        rom_sha256=rom_sha256,
        live_seam_after_pass=live_seam,
        completion_estimate=completion_est,
        closed_ranges=closed_ranges,
        new_labels=data.get("new_labels") or new_labels,
        confidence=confidence,
        sources=sources,
        legacy_metadata=legacy_meta,
        notes=notes,
        source_path=source_path
    )
