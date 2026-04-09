#!/usr/bin/env python3
"""
Validate Session 31 manifests for Bank C4
"""

import json
import os

# Load session 31 manifests
with open("passes/session_31_manifests.json", 'r') as f:
    session_data = json.load(f)

print("=" * 70)
print("SESSION 31 MANIFEST VALIDATION REPORT")
print("=" * 70)

# Validate each manifest
errors = []
warnings = []
validated = []

for manifest_info in session_data["manifests"]:
    pass_num = manifest_info["pass"]
    filename = f"passes/pass{pass_num:04d}.json"
    
    # Check file exists
    if not os.path.exists(filename):
        errors.append(f"Missing file: {filename}")
        continue
    
    # Load and validate
    try:
        with open(filename, 'r') as f:
            manifest = json.load(f)
        
        # Required fields
        required = ["session", "pass_number", "closed_ranges", "promotion_reason"]
        for field in required:
            if field not in manifest:
                errors.append(f"{filename}: Missing field '{field}'")
        
        # Validate closed_ranges
        if "closed_ranges" in manifest:
            for range_entry in manifest["closed_ranges"]:
                if "range" not in range_entry or "label" not in range_entry:
                    warnings.append(f"{filename}: Incomplete range entry")
                if "kind" not in range_entry or range_entry["kind"] != "owner":
                    warnings.append(f"{filename}: Range kind should be 'owner'")
        
        # Check pass_number matches filename
        if manifest.get("pass_number") != pass_num:
            errors.append(f"{filename}: pass_number mismatch ({manifest.get('pass_number')} vs {pass_num})")
        
        # Check session is 31
        if manifest.get("session") != 31:
            errors.append(f"{filename}: session should be 31")
        
        validated.append({
            "pass": pass_num,
            "label": manifest["closed_ranges"][0]["label"],
            "range": manifest["closed_ranges"][0]["range"],
            "valid": True
        })
        
    except json.JSONDecodeError as e:
        errors.append(f"{filename}: Invalid JSON - {e}")
    except Exception as e:
        errors.append(f"{filename}: Error - {e}")

# Check for overlaps
print("\n1. OVERLAP CHECK")
print("-" * 70)
ranges = []
for m in session_data["manifests"]:
    r = m["range"].split("..")
    start = int(r[0].replace("C4:", ""), 16)
    end = int(r[1].replace("C4:", ""), 16)
    ranges.append((start, end, m["pass"], m["label"]))

overlaps = []
for i, (s1, e1, p1, l1) in enumerate(ranges):
    for j, (s2, e2, p2, l2) in enumerate(ranges):
        if i < j:
            if not (e1 < s2 or e2 < s1):
                overlaps.append((p1, l1, p2, l2))

if overlaps:
    for o in overlaps:
        errors.append(f"Overlap: pass{o[0]} ({o[1]}) and pass{o[2]} ({o[3]})")
    print(f"   FAIL: {len(overlaps)} overlap(s) found")
else:
    print("   PASS: No overlaps detected")

# Check against existing manifests (pass 0750-0757)
print("\n2. CONFLICT CHECK WITH EXISTING MANIFESTS")
print("-" * 70)
conflicts = []
for pass_num in range(750, 758):
    filename = f"passes/pass{pass_num:04d}.json"
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                existing = json.load(f)
            
            if "closed_ranges" in existing:
                for er in existing["closed_ranges"]:
                    er_range = er["range"]
                    er_parts = er_range.split("..")
                    er_start = int(er_parts[0].replace("C4:", ""), 16)
                    er_end = int(er_parts[1].replace("C4:", ""), 16)
                    
                    for s, e, p, l in ranges:
                        if not (e < er_start or er_end < s):
                            conflicts.append((p, l, pass_num, er.get("label", "unknown")))
        except:
            pass

if conflicts:
    for c in conflicts:
        errors.append(f"Conflict: pass{c[0]} ({c[1]}) conflicts with pass{c[2]} ({c[3]})")
    print(f"   FAIL: {len(conflicts)} conflict(s) with existing manifests")
else:
    print("   PASS: No conflicts with existing manifests (750-757)")

# Summary
print("\n3. VALIDATION SUMMARY")
print("-" * 70)
print(f"   Total manifests: {len(validated)}")
print(f"   Validated: {len(validated)}")
print(f"   Errors: {len(errors)}")
print(f"   Warnings: {len(warnings)}")

if errors:
    print("\n   ERRORS:")
    for e in errors:
        print(f"   - {e}")

if warnings:
    print("\n   WARNINGS:")
    for w in warnings:
        print(f"   - {w}")

# Coverage calculation
print("\n4. COVERAGE ANALYSIS")
print("-" * 70)
total_bytes = sum(m["size"] for m in session_data["manifests"])
c4_size = 65536  # 64KB bank
print(f"   New bytes documented: {total_bytes}")
print(f"   Bank C4 size: {c4_size} bytes (64KB)")
print(f"   Coverage increase: +{total_bytes/c4_size*100:.2f}%")

# Region breakdown
print("\n5. REGION BREAKDOWN")
print("-" * 70)
regions = {}
for m in session_data["manifests"]:
    r = m["region"]
    if r not in regions:
        regions[r] = {"count": 0, "bytes": 0}
    regions[r]["count"] += 1
    regions[r]["bytes"] += m["size"]

for r in sorted(regions.keys()):
    info = regions[r]
    print(f"   {r}: {info['count']} manifests, {info['bytes']} bytes")

# High-value targets
print("\n6. HIGH-VALUE TARGETS IDENTIFIED")
print("-" * 70)
high_value = [
    ("C4:6077", "Dispatcher pattern, score-6 cluster (pass 762)"),
    ("C4:8012", "Multi-entry point (8012/801F/8020) (pass 767)"),
    ("C4:62DF", "PHD prologue, direct page handler (pass 763)"),
    ("C4:4ACB", "PHP prologue, state preservation (pass 761)"),
    ("C4:1488", "REP prologue, mode set function (pass 759)"),
]
for addr, desc in high_value:
    print(f"   {addr}: {desc}")

print("\n" + "=" * 70)
if not errors:
    print("VALIDATION PASSED - All 12 manifests are ready for application")
else:
    print(f"VALIDATION FAILED - {len(errors)} error(s) must be resolved")
print("=" * 70)
