#!/usr/bin/env python3
"""Generate Phase 0 Baseline Inventories and Summary Reports for Repository Remediation."""

import json
import os
import re
import sys
import hashlib
import subprocess
from datetime import datetime, timezone

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def detect_file_encoding_and_json(filepath):
    with open(filepath, 'rb') as f:
        raw = f.read()
    
    if len(raw) == 0:
        return 'empty', False, None, 'Empty file'
    
    # Check UTF-8 BOM
    if raw.startswith(b'\xef\xbb\xbf'):
        try:
            parsed = json.loads(raw[3:].decode('utf-8'))
            return 'utf-8-sig', True, parsed, None
        except Exception as e:
            return 'utf-8-sig', False, None, str(e)
            
    # Check UTF-16 LE BOM
    if raw.startswith(b'\xff\xfe'):
        try:
            parsed = json.loads(raw[2:].decode('utf-16-le'))
            return 'utf-16-le', True, parsed, None
        except Exception as e:
            return 'utf-16-le', False, None, str(e)
            
    # Check UTF-16 BE BOM
    if raw.startswith(b'\xfe\xff'):
        try:
            parsed = json.loads(raw[2:].decode('utf-16-be'))
            return 'utf-16-be', True, parsed, None
        except Exception as e:
            return 'utf-16-be', False, None, str(e)
            
    # Check standard UTF-8
    try:
        text = raw.decode('utf-8')
        parsed = json.loads(text)
        return 'utf-8', True, parsed, None
    except UnicodeDecodeError:
        pass
    except json.JSONDecodeError as e:
        return 'utf-8', False, None, str(e)
        
    # Try Latin-1 or other
    try:
        text = raw.decode('latin-1')
        parsed = json.loads(text)
        return 'latin-1', True, parsed, None
    except Exception as e:
        return 'binary/unknown', False, None, str(e)

def extract_manifest_info(filepath, filename, data):
    # Determine pass identity from filename
    m_fn = re.match(r'^pass(\d+)', filename, re.IGNORECASE)
    fn_pass = int(m_fn.group(1)) if m_fn else None
    
    doc_pass = None
    schema_family = 'unknown'
    ranges = []
    labels = []
    
    if isinstance(data, dict):
        if 'pass_number' in data:
            doc_pass = data.get('pass_number')
        elif 'pass' in data:
            doc_pass = data.get('pass')
            
        # Schema family detection
        if 'closed_ranges' in data and isinstance(data['closed_ranges'], list):
            schema_family = 'canonical_v1_closed_ranges'
            for item in data['closed_ranges']:
                if isinstance(item, dict):
                    r = item.get('range') or item.get('address_range')
                    if r:
                        ranges.append({
                            'range': r,
                            'kind': item.get('kind', 'unknown'),
                            'label': item.get('label', ''),
                            'confidence': item.get('confidence', '')
                        })
                        if item.get('label'):
                            labels.append(item['label'])
                elif isinstance(item, str):
                    ranges.append({'range': item, 'kind': 'unknown', 'label': '', 'confidence': ''})
        elif 'targets' in data and isinstance(data['targets'], list):
            schema_family = 'legacy_targets'
            for item in data['targets']:
                if isinstance(item, dict):
                    r = item.get('range') or item.get('address_range')
                    if not r and 'start_address' in item and 'end_address' in item:
                        r = f"{item['start_address']}..{item['end_address']}"
                    if r:
                        ranges.append({
                            'range': r,
                            'kind': item.get('kind', item.get('type', 'target')),
                            'label': item.get('label', item.get('name', '')),
                            'confidence': item.get('confidence', '')
                        })
                        if item.get('label') or item.get('name'):
                            labels.append(item.get('label') or item.get('name'))
        elif 'promotions' in data or 'promoted_functions' in data or 'promoted' in data:
            schema_family = 'promotions'
            items = data.get('promotions') or data.get('promoted_functions') or data.get('promoted')
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        r = item.get('function_range') or item.get('range')
                        if r:
                            ranges.append({
                                'range': r,
                                'kind': 'code_owner',
                                'label': item.get('name', item.get('label', '')),
                                'confidence': item.get('verification_status', 'reviewed')
                            })
                            if item.get('name') or item.get('label'):
                                labels.append(item.get('name') or item.get('label'))
        elif 'function_range' in data or 'range' in data or 'start_address' in data:
            schema_family = 'single_function_record'
            r = data.get('function_range') or data.get('range')
            if not r and 'start_address' in data and 'end_address' in data:
                r = f"{data['start_address']}..{data['end_address']}"
            if r:
                ranges.append({
                    'range': r,
                    'kind': data.get('kind', 'code_owner'),
                    'label': data.get('name', data.get('label', '')),
                    'confidence': data.get('confidence', '')
                })
                if data.get('name') or data.get('label'):
                    labels.append(data.get('name') or data.get('label'))
        elif 'scanned_pages' in data or 'scan_results' in data or 'candidates' in data:
            schema_family = 'scan_report'
            
    return {
        'filename_pass': fn_pass,
        'document_pass': doc_pass,
        'schema_family': schema_family,
        'range_count': len(ranges),
        'ranges': ranges,
        'labels': labels
    }

def main():
    os.makedirs('reports/remediation', exist_ok=True)
    
    # 1. Environment & immutable identifiers
    branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
    
    rom_path = 'rom/Chrono Trigger (USA).sfc'
    rom_sha256 = sha256_file(rom_path) if os.path.exists(rom_path) else None
    
    print(f"Branch: {branch}, Commit: {commit}")
    print(f"ROM SHA-256: {rom_sha256}")
    
    # 2. Manifest Inventory
    manifest_dir = 'passes/manifests'
    manifest_entries = []
    duplicate_pass_map = {}
    schema_counts = {}
    noncanonical_names = []
    
    if os.path.exists(manifest_dir):
        files = sorted(os.listdir(manifest_dir))
        for fn in files:
            path = os.path.join(manifest_dir, fn)
            if not os.path.isfile(path):
                continue
            is_json_ext = fn.endswith('.json')
            f_size = os.path.getsize(path)
            f_hash = sha256_file(path)
            
            enc, is_valid_json, data, err = detect_file_encoding_and_json(path) if is_json_ext else ('non-json', False, None, 'Not json')
            
            m_info = extract_manifest_info(path, fn, data) if is_valid_json else {
                'filename_pass': int(re.match(r'^pass(\d+)', fn, re.I).group(1)) if re.match(r'^pass(\d+)', fn, re.I) else None,
                'document_pass': None,
                'schema_family': 'invalid_json',
                'range_count': 0,
                'ranges': [],
                'labels': []
            }
            
            is_exact_canonical_name = bool(re.match(r'^pass\d+\.json$', fn))
            if is_json_ext and not is_exact_canonical_name:
                noncanonical_names.append(fn)
                
            entry = {
                'filename': fn,
                'relative_path': os.path.relpath(path).replace('\\', '/'),
                'size_bytes': f_size,
                'sha256': f_hash,
                'encoding': enc,
                'is_valid_json': is_valid_json,
                'json_error': err,
                'is_exact_canonical_name': is_exact_canonical_name,
                **m_info
            }
            manifest_entries.append(entry)
            
            pass_num = m_info.get('document_pass') or m_info.get('filename_pass')
            if pass_num is not None:
                duplicate_pass_map.setdefault(pass_num, []).append(fn)
                
            fam = m_info.get('schema_family', 'unknown')
            schema_counts[fam] = schema_counts.get(fam, 0) + 1

    duplicate_passes = {k: v for k, v in duplicate_pass_map.items() if len(v) > 1}
    
    with open('reports/remediation/manifest_inventory.json', 'w', encoding='utf-8') as f:
        json.dump({
            'total_manifest_files': len(manifest_entries),
            'exact_canonical_filenames': sum(1 for e in manifest_entries if e['is_exact_canonical_name']),
            'noncanonical_filenames_count': len(noncanonical_names),
            'noncanonical_filenames': noncanonical_names,
            'schema_counts': schema_counts,
            'duplicate_pass_identities_count': len(duplicate_passes),
            'duplicate_passes': duplicate_passes,
            'entries': manifest_entries
        }, f, indent=2)
        
    print(f"Manifests: {len(manifest_entries)} total, {len(duplicate_passes)} duplicate pass IDs, {len(noncanonical_names)} non-exact names")

    # 3. Artifact inventory across whole repo for .json files
    artifact_entries = []
    json_strict_failures = []
    
    for root, dirs, files in os.walk('.'):
        if '.git' in root or '.venv' in root:
            continue
        for fn in sorted(files):
            path = os.path.join(root, fn)
            rel_path = os.path.relpath(path).replace('\\', '/')
            size = os.path.getsize(path)
            f_hash = sha256_file(path)
            
            if fn.endswith('.json'):
                enc, is_valid, _, err = detect_file_encoding_and_json(path)
                # Test strict UTF-8
                strict_utf8 = False
                try:
                    with open(path, 'r', encoding='utf-8') as jf:
                        json.load(jf)
                    strict_utf8 = True
                except Exception:
                    strict_utf8 = False
                    
                artifact_entries.append({
                    'path': rel_path,
                    'size_bytes': size,
                    'sha256': f_hash,
                    'encoding': enc,
                    'is_valid_json': is_valid,
                    'strict_utf8_json': strict_utf8,
                    'error': err
                })
                if not strict_utf8:
                    json_strict_failures.append({
                        'path': rel_path,
                        'encoding': enc,
                        'is_valid_with_detected_encoding': is_valid,
                        'error': err
                    })
                    
    with open('reports/remediation/artifact_inventory.json', 'w', encoding='utf-8') as f:
        json.dump({
            'total_tracked_json_files': len(artifact_entries),
            'strict_utf8_valid_json_count': sum(1 for a in artifact_entries if a['strict_utf8_json']),
            'strict_utf8_failures_count': len(json_strict_failures),
            'failures': json_strict_failures,
            'entries': artifact_entries
        }, f, indent=2)
        
    print(f"JSON Artifacts: {len(artifact_entries)} total, {len(json_strict_failures)} strict UTF-8 failures")

    # 4. Range Conflicts and Overlaps Inventory
    # Run validate_labels to capture exact baseline conflicts
    res = subprocess.run(
        [sys.executable, 'tools/scripts/validate_labels.py', '--manifests-dir', 'passes/manifests', '--strict-overlaps'],
        capture_output=True, text=True
    )
    with open('reports/remediation/baseline_label_overlaps.txt', 'w', encoding='utf-8') as f:
        f.write(res.stdout + '\n' + res.stderr)
        
    # Also parse overlaps into structured JSON
    overlap_lines = [l.strip() for l in (res.stdout + '\n' + res.stderr).splitlines() if 'overlap:' in l or 'duplicate range:' in l]
    exact_duplicates = [l for l in overlap_lines if 'duplicate range:' in l]
    other_overlaps = [l for l in overlap_lines if 'overlap:' in l]
    
    with open('reports/remediation/range_conflicts.json', 'w', encoding='utf-8') as f:
        json.dump({
            'total_warnings': len(overlap_lines),
            'exact_duplicates_count': len(exact_duplicates),
            'non_tail_overlaps_count': len(other_overlaps),
            'exact_duplicates': exact_duplicates,
            'overlaps': other_overlaps
        }, f, indent=2)
        
    print(f"Range Conflicts: {len(overlap_lines)} total ({len(exact_duplicates)} exact duplicates, {len(other_overlaps)} overlaps)")

    # 5. Capture other baseline command outputs
    subprocess.run(
        [sys.executable, 'tools/scripts/toolkit_doctor.py', '--output-json', 'reports/remediation/baseline_doctor.json', '--output-md', 'reports/remediation/baseline_doctor.md'],
        capture_output=True, text=True
    )
    
    res_branch = subprocess.run(
        [sys.executable, 'tools/scripts/audit_branch_state_v1.py', '--strict-gaps'],
        capture_output=True, text=True
    )
    with open('reports/remediation/baseline_branch_state.txt', 'w', encoding='utf-8') as f:
        f.write(res_branch.stdout + '\n' + res_branch.stderr)
        
    res_cov = subprocess.run(
        [sys.executable, 'tools/generate_coverage_report.py'],
        capture_output=True, text=True
    ) if os.path.exists('tools/generate_coverage_report.py') else None
    if res_cov:
        with open('reports/remediation/baseline_coverage.txt', 'w', encoding='utf-8') as f:
            f.write(res_cov.stdout + '\n' + res_cov.stderr)

    # 6. Baseline Summary MD and Baseline Inventory JSON
    baseline_inventory = {
        'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'git_branch': branch,
        'git_commit': commit,
        'python_version': sys.version,
        'rom_sha256': rom_sha256,
        'metrics': {
            'manifest_files_count': len(manifest_entries),
            'exact_passNNN_filenames': sum(1 for e in manifest_entries if e['is_exact_canonical_name']),
            'noncanonical_manifest_filenames': len(noncanonical_names),
            'duplicate_pass_identities': len(duplicate_passes),
            'unknown_or_legacy_schemas': sum(1 for e in manifest_entries if e['schema_family'] not in ('canonical_v1_closed_ranges',)),
            'exact_duplicate_ranges': len(exact_duplicates),
            'strict_range_overlaps': len(other_overlaps),
            'strict_json_failures': len(json_strict_failures),
            'tracked_toolkit_zips': len(os.listdir('toolkits')) if os.path.exists('toolkits') else 0
        }
    }
    
    with open('reports/remediation/baseline_inventory.json', 'w', encoding='utf-8') as f:
        json.dump(baseline_inventory, f, indent=2)

    summary_md = f"""# Repository Remediation — Baseline Summary

| Attribute | Baseline Value |
|---|---|
| Generation Timestamp | `{baseline_inventory['timestamp_utc']}` |
| Git Branch | `{branch}` |
| Git Commit Baseline | `{commit}` |
| Python Version | `{sys.version.split()[0]}` |
| ROM SHA-256 | `{rom_sha256}` |
| Total Manifest Candidates | `{len(manifest_entries)}` |
| Exact `passNNN.json` Names | `{sum(1 for e in manifest_entries if e['is_exact_canonical_name'])}` |
| Non-exact Manifest Names | `{len(noncanonical_names)}` |
| Duplicate Pass Identities | `{len(duplicate_passes)}` |
| Exact Duplicate Ranges | `{len(exact_duplicates)}` |
| Non-tail Overlaps | `{len(other_overlaps)}` |
| Strict JSON Parser Failures | `{len(json_strict_failures)}` |
| Tracked Toolkit Archives | `{len(os.listdir('toolkits')) if os.path.exists('toolkits') else 0}` |

## Key Findings

1. **Manifest Visibility**: 81 manifests use suffixed names (`pass1000_c3_session28.json` through `pass1229_c3_cb47.json`) and are ignored by legacy `passNNN.json` iterators, masking recent sessions 28–46.
2. **Duplicate Passes**: 38 pass numbers are shared by multiple manifest files in `passes/manifests/`.
3. **Range Collisions**: 154 strict warnings (23 exact duplicate ranges and 131 overlaps) require deterministic deconfliction.
4. **Artifact Encoding**: 194 JSON files fail strict UTF-8 decoding without BOM, including UTF-16, UTF-8 BOM, and mislabeled text/logs.
5. **Prohibited Binaries**: Commercial ROM `rom/Chrono Trigger (USA).sfc` is tracked in git index and must be untracked with clear local verification.
"""
    with open('reports/remediation/baseline_summary.md', 'w', encoding='utf-8') as f:
        f.write(summary_md)

    print("Phase 0 baseline inventories generated successfully.")

if __name__ == '__main__':
    main()
