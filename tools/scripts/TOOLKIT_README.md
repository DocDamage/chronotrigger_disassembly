# Chrono Trigger Disassembly Toolkit v2.0

Enhanced toolkit with batch processing and automation for Bank C0 disassembly.

## New Tools

### 1. `auto_promote.py` - Automated Pass Creation

Extracts high-caller targets from scan JSON and creates pass manifests automatically.

```bash
# Basic usage - extract and create passes for targets with 2+ callers
python auto_promote.py --scan-file scan_C0_6A00_4p.json

# Require 3+ callers
python auto_promote.py --scan-file scan.json --min-callers 3

# Dry run to preview without creating files
python auto_promote.py --scan-file scan.json --dry-run

# Auto-adjust boundaries to avoid conflicts
python auto_promote.py --scan-file scan.json --auto-fix
```

**Features:**
- Extracts targets from seam block scan JSON
- Filters by caller count and strength
- Suggests optimal boundaries using backtrack scores
- Detects conflicts with existing passes
- Auto-adjusts boundaries when possible

### 2. `batch_scan.py` - Multi-Region Scanning

Scans multiple Bank C0 regions in sequence.

```bash
# Scan default priority regions
python batch_scan.py

# Scan with auto-promotion
python batch_scan.py --auto-promote --min-callers 3

# Scan custom regions
python batch_scan.py --regions C0:1000:4 C0:5000:8

# Save results to custom directory
python batch_scan.py --output-dir ../../my_scans
```

**Default Regions:**
- C0:CF00-D5FF (7 pages) - Largest gap
- C0:B400-B8FF (5 pages)
- C0:F900-FDFF (5 pages)
- C0:3100-34FF (4 pages)
- C0:4700-4AFF (4 pages)

### 3. `gap_analyzer.py` - Coverage Gap Analysis

Analyzes Bank C0 coverage and suggests scanning priorities.

```bash
python gap_analyzer.py
```

**Output:**
- Current coverage statistics
- Top 15 largest gaps sorted by size
- Page-level coverage breakdown
- Quality assessment for each gap
- Recommended scan commands

### 4. `validate_passes.py` - Comprehensive Validation

Validates all pass manifests for issues.

```bash
python validate_passes.py
```

**Checks:**
- Overlapping passes
- Suspicious boundaries (too small/large)
- Confidence level distribution
- Suggests fixes for overlaps

### 5. `quick_promote.py` - Manual Target Promotion

Quickly promote a specific target.

```bash
# Basic promotion
python quick_promote.py C0:6D2F --callers 6

# With custom options
python quick_promote.py C0:6D2F \
    --start C0:6D2B \
    --size 35 \
    --callers 6 \
    --strength weak \
    --confidence high \
    --label ct_c0_6d2b_utility_handler
```

## Workflow Examples

### Example 1: Scan and Auto-Promote

```bash
# 1. Analyze gaps to find priority regions
python gap_analyzer.py

# 2. Scan priority regions with auto-promotion
python batch_scan.py --auto-promote --min-callers 2

# 3. Validate results
python validate_passes.py
```

### Example 2: Targeted Deep Scan

```bash
# 1. Scan a specific region
python run_seam_block_v1.py \
    --rom "../../rom/Chrono Trigger (USA).sfc" \
    --start C0:6A00 \
    --pages 4 \
    --json > scan_6a00.json

# 2. Auto-promote targets
python auto_promote.py --scan-file scan_6a00.json --auto-fix

# 3. Check for any remaining issues
python validate_passes.py
```

### Example 3: Manual Promotion with Validation

```bash
# 1. Quick promote a specific target
python quick_promote.py C0:B97F --callers 2 --size 30

# 2. Check if it caused any conflicts
python validate_passes.py

# 3. If conflicts, use auto_promote with fix
# Or manually adjust using gap_analyzer for context
```

## Old Tools (Still Available)

- `run_seam_block_v1.py` - Core scanning tool
- `validate_labels_v2.py` - Basic overlap validation
- `analyze_c0_coverage.py` - Coverage reporting

## Best Practices

1. **Always validate after creating passes:**
   ```bash
   python validate_passes.py
   ```

2. **Use gap_analyzer before scanning:**
   ```bash
   python gap_analyzer.py
   ```
   Then scan the highest-quality gaps first.

3. **Start with --dry-run:**
   ```bash
   python auto_promote.py --scan-file scan.json --dry-run
   ```

4. **Use --auto-fix for minor conflicts:**
   ```bash
   python auto_promote.py --scan-file scan.json --auto-fix
   ```

5. **Prefer batch_scan for routine work:**
   ```bash
   python batch_scan.py --auto-promote
   ```

## Migration from Old Workflow

| Old Way | New Way |
|---------|---------|
| Manual JSON editing | `quick_promote.py` |
| Single region scan | `batch_scan.py` |
| Manual target extraction | `auto_promote.py` |
| Guess what to scan next | `gap_analyzer.py` |
| Basic overlap check | `validate_passes.py` |

## Troubleshooting

### "No targets with N+ callers found"

Try lowering the threshold:
```bash
python auto_promote.py --scan-file scan.json --min-callers 1
```

### "Cannot auto-fix, skipping"

The conflict is too complex for automatic fixing. Manually inspect:
```bash
python gap_analyzer.py  # See context
# Then manually adjust boundary or use quick_promote with different range
```

### Validation shows many overlaps

Use auto_promote with --auto-fix flag, or manually resolve using validate_passes.py suggestions.

## Performance Tips

1. Cache is reused between scans - subsequent scans are faster
2. Use batch_scan instead of multiple individual scans
3. gap_analyzer is instant - use it frequently to track progress
4. validate_passes.py is fast - run it after every promotion batch
