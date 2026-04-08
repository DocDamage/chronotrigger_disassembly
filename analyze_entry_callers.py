#!/usr/bin/env python3
import json

def analyze_entry_callers(filepath):
    with open(filepath, 'r', encoding='utf-16') as f:
        data = json.load(f)
    
    range_name = data.get('range', 'Unknown')
    print(f"\n=== Entry Callers for {range_name} ===")
    
    entry = data.get('entry_callers', {})
    print(f'Total entries: {entry.get("entry_count", 0)}')
    
    # Group by call type
    by_type = {}
    for e in entry.get('entries', []):
        ctype = e.get('call_type', 'unknown')
        if ctype not in by_type:
            by_type[ctype] = []
        by_type[ctype].append(e)
    
    for ctype, entries in by_type.items():
        print(f"\n  {ctype}: {len(entries)} entries")
        for e in entries[:5]:
            print(f"    {e['entry_point']}: from {e.get('caller_context', 'N/A')}")

if __name__ == "__main__":
    files = [
        'reports/c3_2900_3058_flow.json',
        'reports/c3_30b1_34ff_flow.json',
        'reports/c3_3761_3c7f_flow.json'
    ]
    
    for f in files:
        try:
            analyze_entry_callers(f)
        except Exception as e:
            print(f"Error processing {f}: {e}")
