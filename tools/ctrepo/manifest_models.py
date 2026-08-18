"""Manifest data models and representations."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

@dataclass
class ClosedRange:
    range_str: str  # Format: "BB:AAAA..BB:EEEE"
    bank: str
    start_addr: int
    end_addr: int
    kind: str = "code_owner"
    label: str = ""
    confidence: str = "medium"
    verification_status: Optional[str] = None
    parent_range: Optional[str] = None
    parent_label: Optional[str] = None
    evidence: Dict[str, Any] = field(default_factory=dict)
    legacy_metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def parse(cls, range_str: str, kind: str = "code_owner", label: str = "", confidence: str = "medium", **kwargs) -> 'ClosedRange':
        clean = range_str.strip().upper()
        # Support either .. or -
        sep = ".." if ".." in clean else "-"
        parts = clean.split(sep)
        if len(parts) != 2:
            raise ValueError(f"Invalid range syntax: '{range_str}'")
        
        start_part, end_part = parts[0].strip(), parts[1].strip()
        
        if ":" in start_part:
            bank_start, addr_start_str = start_part.split(":", 1)
        else:
            raise ValueError(f"Missing bank in start address: '{start_part}'")
            
        if ":" in end_part:
            bank_end, addr_end_str = end_part.split(":", 1)
            if bank_start != bank_end:
                raise ValueError(f"Cross-bank range not allowed: '{range_str}' ({bank_start} vs {bank_end})")
        else:
            bank_end = bank_start
            addr_end_str = end_part
            
        start_addr = int(addr_start_str, 16)
        end_addr = int(addr_end_str, 16)
        
        if start_addr > end_addr:
            raise ValueError(f"Reversed endpoints in range: '{range_str}' ({start_addr:04X} > {end_addr:04X})")
            
        canonical_str = f"{bank_start.upper()}:{start_addr:04X}..{bank_start.upper()}:{end_addr:04X}"
        
        kind_norm = (kind or "code_owner").lower().strip()
        kind_map = {
            "owner": "code_owner",
            "code": "code_owner",
            "function": "code_owner",
            "subroutine": "code_owner",
            "target": "code_owner",
            "cluster": "code_owner",
            "hub_candidate": "code_owner",
            "helper": "code_helper",
            "entry_stub": "wrapper",
            "stub": "wrapper"
        }
        allowed_kinds = ("code_owner", "code_helper", "wrapper", "veneer", "data", "text_marker", "tail_fragment", "superseded")
        kind_final = kind_map.get(kind_norm, kind_norm if kind_norm in allowed_kinds else None)
        if kind_final is None:
            raise ValueError(f"Unknown range kind '{kind}' for {range_str}")

        # Normalize confidence to controlled vocabulary
        conf_str = str(confidence or "medium").lower().strip()
        if conf_str in ("6", "score-6", "score_6"):
            conf_final = "score-6"
        elif conf_str in ("5", "score-5", "score_5"):
            conf_final = "score-5"
        elif conf_str in ("4", "score-4", "score_4"):
            conf_final = "score-4"
        elif conf_str in ("high", "medium-high", "medium", "low", "reviewed"):
            conf_final = conf_str
        else:
            conf_final = "medium"

        # Ensure non-empty label
        final_label = label.strip() if label else f"ct_{bank_start.lower()}_{start_addr:04X}"

        raw_ev = kwargs.get("evidence", {})
        if isinstance(raw_ev, list):
            evidence = {"items": raw_ev}
        elif isinstance(raw_ev, str):
            evidence = {"summary": raw_ev}
        elif isinstance(raw_ev, dict):
            evidence = raw_ev
        else:
            evidence = {}

        return cls(
            range_str=canonical_str,
            bank=bank_start.upper(),
            start_addr=start_addr,
            end_addr=end_addr,
            kind=kind_final,
            label=final_label,
            confidence=conf_final,
            verification_status=kwargs.get("verification_status") or "pending",
            parent_range=kwargs.get("parent_range"),
            parent_label=kwargs.get("parent_label"),
            evidence=evidence,
            legacy_metadata=kwargs.get("legacy_metadata", {})
        )

    @property
    def byte_count(self) -> int:
        return (self.end_addr - self.start_addr) + 1

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "range": self.range_str,
            "kind": self.kind,
            "label": self.label,
            "confidence": self.confidence,
        }
        if self.verification_status:
            d["verification_status"] = self.verification_status
        if self.parent_range:
            d["parent_range"] = self.parent_range
        if self.parent_label:
            d["parent_label"] = self.parent_label
        if self.evidence:
            d["evidence"] = self.evidence
        if self.legacy_metadata:
            d["legacy_metadata"] = self.legacy_metadata
        return d


@dataclass
class CanonicalManifest:
    pass_number: int
    schema_version: int = 2
    status: str = "reviewed"
    branch: str = "live-work-from-pass166"
    toolkit_version: str = "repo-native-vNext"
    rom_sha256: Optional[str] = "06d1c2b06b716052c5596aaa0c2e5632a027fee1a9a28439e509f813c30829a9"
    live_seam_after_pass: Optional[str] = None
    completion_estimate: Optional[float] = None
    closed_ranges: List[ClosedRange] = field(default_factory=list)
    new_labels: List[str] = field(default_factory=list)
    confidence: Dict[str, str] = field(default_factory=lambda: {"structural": "medium", "semantic": "medium", "rebuild": "low"})
    sources: Dict[str, str] = field(default_factory=dict)
    legacy_metadata: Dict[str, Any] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)
    source_path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "schema_version": self.schema_version,
            "pass_number": self.pass_number,
            "status": self.status,
            "branch": self.branch,
            "toolkit_version": self.toolkit_version,
        }
        if self.rom_sha256:
            d["rom_sha256"] = self.rom_sha256
        if self.live_seam_after_pass is not None:
            d["live_seam_after_pass"] = self.live_seam_after_pass
        if self.completion_estimate is not None:
            d["completion_estimate"] = self.completion_estimate
            
        d["closed_ranges"] = [r.to_dict() for r in self.closed_ranges]
        d["new_labels"] = self.new_labels or [r.label for r in self.closed_ranges if r.label]
        d["confidence"] = self.confidence
        if self.sources:
            d["sources"] = self.sources
        if self.legacy_metadata:
            d["legacy_metadata"] = self.legacy_metadata
        d["notes"] = self.notes
        return d
