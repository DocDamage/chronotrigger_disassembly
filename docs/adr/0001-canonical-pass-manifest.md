# ADR 0001: Canonical Pass Manifest Specification

## Status
Accepted

## Context
Historical reverse engineering in this repository used heterogeneous manifest formats, including:
1. `closed_ranges` format (schema v1) in `passNNN.json`.
2. Suffixed filenames such as `pass1000_c3_session28.json` through `pass1229_c3_cb47.json`.
3. Legacy `targets` format with `start_address`/`end_address` or `type`/`name`.
4. Single-function and top-level `function_range` records.
5. Promotion manifests from candidate review pipelines (`promotions` list).
6. Non-manifest scan outputs accidentally saved under `passes/manifests/`.

Because the original manifest iterator only parsed exact `passNNN.json` strings, 81 recent passes were ignored by repository automation, resulting in an obsolete live seam and truncated coverage calculations.

## Decision

### 1. Canonical Filename and Directory
- Canonical manifests live under `passes/manifests/`.
- Filenames MUST follow the pattern `passNNNN.json` where `NNNN` is the 4-digit zero-padded integer pass number (e.g., `pass0100.json`, `pass1229.json`).
- Integer pass sorting MUST be numeric, not purely lexicographical.

### 2. Canonical Manifest Schema (v2)
Every active manifest MUST adhere to `schema_version: 2`:
```json
{
  "schema_version": 2,
  "pass_number": 1229,
  "status": "reviewed",
  "branch": "live-work-from-pass166",
  "toolkit_version": "repo-native-vNext",
  "rom_sha256": "06d1c2b06b716052c5596aaa0c2e5632a027fee1a9a28439e509f813c30829a9",
  "live_seam_after_pass": "C3:D000..",
  "closed_ranges": [
    {
      "range": "C3:CB47..C3:CB64",
      "kind": "code_owner",
      "label": "ct_c3_cb47_php_prologue",
      "confidence": "medium",
      "verification_status": "reviewed",
      "evidence": {
        "source": "backtrack",
        "score": 6,
        "callers": ["C3:28E9"]
      }
    }
  ],
  "new_labels": ["ct_c3_cb47_php_prologue"],
  "confidence": {
    "structural": "medium",
    "semantic": "medium",
    "rebuild": "low"
  },
  "sources": {
    "disassembly_note": "passes/disasm/pass1229.md",
    "legacy_manifest": "passes/manifests/legacy/pass1229_c3_cb47.json"
  },
  "notes": []
}
```

### 3. Identity and Integrity Rules
- `pass_number` MUST exactly match the numeric component of the filename.
- `pass_number` MUST be unique across all active manifests.
- Endpoints in `range` MUST use uppercase hex `BB:AAAA..BB:EEEE` format with $AAAA \le EEEE$ within the same SNES bank.
- Non-manifest scan outputs MUST NOT be placed in `passes/manifests/`.
- All legacy manifests are mapped to canonical representations with legacy fields preserved under `legacy_metadata` or `sources`.

## Consequences
- Single iterator in `tools.ctrepo` discovers 100% of manifests deterministically.
- Strict schema validation fails on unadapted or duplicate manifests.
