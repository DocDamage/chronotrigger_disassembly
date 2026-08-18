#!/usr/bin/env python3
"""Validate and normalize repository structured artifacts (JSON/YAML encodings, filenames)."""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any

import yaml

repo_root = Path(__file__).resolve().parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_structured_text(text: str, path: str) -> Any:
    if Path(path).suffix.lower() in {".yaml", ".yml"}:
        return list(yaml.safe_load_all(text))
    return json.loads(text)

def detect_and_normalize_file(path: str, normalize: bool = False) -> Dict[str, Any]:
    with open(path, "rb") as f:
        raw = f.read()
    
    orig_hash = sha256_bytes(raw)
    orig_size = len(raw)
    
    if orig_size == 0:
        if normalize:
            # If empty file with .json, write empty dict or list
            with open(path, "w", encoding="utf-8") as f:
                f.write("{}\n")
            return {
                "path": path,
                "action": "initialized_empty_document",
                "original_encoding": "empty",
                "original_sha256": orig_hash,
                "new_sha256": sha256_bytes(b"{}\n"),
                "status": "normalized"
            }
        return {
            "path": path,
            "action": "none",
            "original_encoding": "empty",
            "original_sha256": orig_hash,
            "status": "error_empty_file"
        }

    # Decode text for inspection
    text = ""
    if raw.startswith(b"\xef\xbb\xbf"):
        try:
            text = raw[3:].decode("utf-8")
        except Exception:
            pass
    elif raw.startswith(b"\xff\xfe"):
        try:
            text = raw[2:].decode("utf-16-le")
        except Exception:
            pass
    elif raw.startswith(b"\xfe\xff"):
        try:
            text = raw[2:].decode("utf-16-be")
        except Exception:
            pass
    else:
        try:
            text = raw.decode("utf-8")
        except Exception:
            try:
                text = raw.decode("latin-1")
            except Exception:
                pass

    if text.strip().startswith("target:"):
        if normalize:
            new_path = path[:-5] + ".txt"
            with open(new_path, "w", encoding="utf-8") as f:
                f.write(text)
            if os.path.exists(path):
                os.remove(path)
            return {
                "path": path,
                "new_path": new_path,
                "action": "renamed_to_txt",
                "original_encoding": "text",
                "original_sha256": orig_hash,
                "status": "renamed"
            }
        return {
            "path": path,
            "action": "none",
            "original_encoding": "text",
            "original_sha256": orig_hash,
            "status": "error_plaintext_mislabeled_as_json"
        }

    if "Traceback (most recent call last)" in text or "python : usage:" in text or ("usage:" in text and "At line:" in text):
        if normalize:
            new_path = path[:-5] + ".log"
            with open(new_path, "w", encoding="utf-8") as f:
                f.write(text)
            if os.path.exists(path):
                os.remove(path)
            return {
                "path": path,
                "new_path": new_path,
                "action": "renamed_to_log",
                "original_encoding": "text",
                "original_sha256": orig_hash,
                "status": "renamed"
            }
        return {
            "path": path,
            "action": "none",
            "original_encoding": "text",
            "original_sha256": orig_hash,
            "status": "error_traceback_mislabeled_as_json"
        }

    # Detect encoding
    detected_enc = None
    parsed_obj = None
    
    if raw.startswith(b"\xef\xbb\xbf"):
        detected_enc = "utf-8-sig"
        try:
            parsed_obj = parse_structured_text(raw[3:].decode("utf-8"), path)
        except Exception:
            pass
    elif raw.startswith(b"\xff\xfe"):
        detected_enc = "utf-16-le"
        try:
            parsed_obj = parse_structured_text(raw[2:].decode("utf-16-le"), path)
        except Exception:
            pass
    elif raw.startswith(b"\xfe\xff"):
        detected_enc = "utf-16-be"
        try:
            parsed_obj = parse_structured_text(raw[2:].decode("utf-16-be"), path)
        except Exception:
            pass
    else:
        try:
            parsed_obj = parse_structured_text(raw.decode("utf-8"), path)
            detected_enc = "utf-8"
        except UnicodeDecodeError:
            try:
                parsed_obj = parse_structured_text(raw.decode("latin-1"), path)
                detected_enc = "latin-1"
            except Exception:
                pass
        except (json.JSONDecodeError, yaml.YAMLError):
            pass

    if parsed_obj is None:
        return {
            "path": path,
            "action": "none",
            "original_encoding": detected_enc or "unknown",
            "original_sha256": orig_hash,
            "status": "error_structured_parse_failed"
        }

    if detected_enc != "utf-8" or raw.startswith(b"\xef\xbb\xbf"):
        if normalize:
            # Re-write cleanly as UTF-8 without BOM
            with open(path, "w", encoding="utf-8") as f:
                if Path(path).suffix.lower() in {".yaml", ".yml"}:
                    yaml.safe_dump_all(parsed_obj, f, sort_keys=False)
                else:
                    json.dump(parsed_obj, f, indent=2)
                    f.write("\n")
            new_raw = open(path, "rb").read()
            return {
                "path": path,
                "action": "re_encoded_utf8",
                "original_encoding": detected_enc,
                "original_sha256": orig_hash,
                "new_sha256": sha256_bytes(new_raw),
                "status": "normalized"
            }
        return {
            "path": path,
            "action": "none",
            "original_encoding": detected_enc,
            "original_sha256": orig_hash,
            "status": "warn_non_canonical_encoding"
        }

    return {
        "path": path,
        "action": "none",
        "original_encoding": "utf-8",
        "original_sha256": orig_hash,
        "status": "valid"
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and normalize repository JSON/YAML artifacts.")
    parser.add_argument("--normalize", action="store_true", help="Normalize UTF-16/BOM and rename mislabeled files")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on non-canonical encodings or errors")
    parser.add_argument("--report", default="reports/remediation/artifact_migration_map.json", help="Path to write JSON report")
    args = parser.parse_args()

    root = repo_root
    structured_files = []
    report_path = Path(args.report).resolve() if args.report else None
    
    for r, d_list, f_list in os.walk(root):
        if ".git" in r or ".venv" in r:
            continue
        for fn in sorted(f_list):
            if fn.endswith((".json", ".yaml", ".yml")):
                candidate = Path(r, fn).resolve()
                if report_path is not None and candidate == report_path:
                    continue
                structured_files.append(str(candidate))

    records = []
    errors = []
    normalized_count = 0
    valid_count = 0

    for path in structured_files:
        rel_path = os.path.relpath(path, root).replace("\\", "/")
        rec = detect_and_normalize_file(path, normalize=args.normalize)
        records.append(rec)
        
        status = rec["status"]
        if status.startswith("error"):
            errors.append(f"{rel_path}: {status}")
        elif status == "normalized":
            normalized_count += 1
        elif status == "valid":
            valid_count += 1
        elif status.startswith("warn"):
            if args.strict and not args.normalize:
                errors.append(f"{rel_path}: {status} ({rec['original_encoding']})")

    report_payload = {
        "total_scanned": len(structured_files),
        "valid_count": valid_count,
        "normalized_count": normalized_count,
        "error_count": len(errors),
        "errors": errors,
        "records": records
    }

    if args.report:
        os.makedirs(os.path.dirname(os.path.abspath(args.report)), exist_ok=True)
        with open(args.report, "w", encoding="utf-8") as f:
            json.dump(report_payload, f, indent=2)
        print(f"Saved artifact report to {args.report}")

    print(f"Artifact Validation: {len(structured_files)} scanned ({valid_count} valid, {normalized_count} normalized, {len(errors)} errors)")

    if errors:
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
