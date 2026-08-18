#!/usr/bin/env python3
"""Generate manifest source discrepancy report for the 22 omitted pass1000-pass1021 baseline files."""

import json
import re
import subprocess


def main():
    with open('reports/remediation/corrective_baseline.json', 'r', encoding='utf-8') as f:
        baseline = json.load(f)
    with open('passes/manifests/manifest_migration_map.json', 'r', encoding='utf-8') as f:
        mig_map = json.load(f)

    mig_hashes = {r['source_sha256'] for r in mig_map['migration_records']}
    missing = [m for m in baseline['manifests'] if m['sha256'] not in mig_hashes]

    missing_entries = []
    for m in missing:
        fn = m['path'].split('/')[-1]
        m_pass = re.search(r'^pass(10[0-2][0-9])\.json$', fn)
        if not m_pass:
            continue
        pass_num = int(m_pass.group(1))
        if pass_num > 1021:
            continue

        raw = subprocess.run(['git', 'cat-file', '-p', m['blob_id']], capture_output=True).stdout
        parsed = json.loads(raw.decode('utf-8-sig', errors='replace'))
        ranges = []
        if 'range' in parsed and isinstance(parsed['range'], str):
            ranges.append(parsed['range'])
        elif 'addr' in parsed and 'end' in parsed:
            ranges.append(f"{parsed['addr']}..{parsed['end']}")
        elif 'ranges' in parsed:
            ranges = [r.get('range', '') for r in parsed['ranges'] if isinstance(r, dict)]
        elif 'closed_ranges' in parsed:
            ranges = [r.get('range', '') for r in parsed['closed_ranges'] if isinstance(r, dict)]
        elif 'targets' in parsed:
            ranges = [t.get('range', t.get('addr', '')) for t in parsed['targets'] if isinstance(t, dict)]

        missing_entries.append({
            'baseline_commit': baseline['baseline_commit'],
            'source_path': m['path'],
            'source_blob': m['blob_id'],
            'source_sha256': m['sha256'],
            'pass_number': pass_num,
            'normalized_ranges': ranges,
            'current_disposition': 'missing_from_migration_ledger',
            'recovery_status': 'recoverable_from_git'
        })

    missing_entries.sort(key=lambda x: x['pass_number'])
    print(f"Identified {len(missing_entries)} missing pass1000-pass1021 source manifests:")
    for me in missing_entries:
        print(f"  {me['source_path']} (Pass {me['pass_number']}) -> {me['normalized_ranges']}")

    with open('reports/remediation/manifest_source_discrepancy.json', 'w', encoding='utf-8') as f:
        json.dump({
            'total_missing_count': len(missing_entries),
            'missing_sources': missing_entries
        }, f, indent=2)

    print("Wrote reports/remediation/manifest_source_discrepancy.json")

if __name__ == "__main__":
    main()
