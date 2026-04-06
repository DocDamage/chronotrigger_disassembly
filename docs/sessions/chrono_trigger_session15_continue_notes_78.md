# Chrono Trigger Session 15 — Continuation Notes 78

## 🎉 BREAKTHROUGH: FIRST PROMOTIONS IN C7 BANK!

**Historic milestone achieved** after 170+ pages of analysis.

---

## Pass 192: C7:C300..C7:C4FF - First Code in Upper C7

**Status:** ✅ PROMOTED as code (owner)

**Evidence:**
- 8 prologues (REP/SEP) detected
- Multiple RTS/RTL returns confirmed
- Cross-bank calls from 10 banks
- Direct callers to C7:B0xx region (C7:C475→B0B4, C7:C487→B0DF, C7:C4AB→B0F2)
- Score-4 backtrack candidates

**Targets promoted:** C7:C3AE, C7:C388, C7:C31D, C7:C4AA

**Strategic significance:** This promotion broke the circular dependency and provided strong anchors for C7:B100 validation.

---

## Pass 193: C7:B000..C7:B1FF - FIRST Upper C7 Code Region

**Status:** ✅ PROMOTED as code (owner) - **MILESTONE!**

**Anchor evidence (ALL STRONG):**
| Target | Strong Anchor From |
|--------|-------------------|
| C7:B111 | C7:C000..C7:C2FF (code) |
| C7:B188 | C7:7400..C7:74FF (code) |
| C7:B0B4 | C7:C300..C7:C4FF (code, pass 192) |
| C7:B0DF | C7:C300..C7:C4FF (code, pass 192) |

**Targets promoted (8 total):**
- C7:B111, C7:B188, C7:B0B4, C7:B0DF
- C7:B09E, C7:B0F2, C7:B115, C7:B195

**Milestone:** FIRST promotion in C7 bank after 170+ pages of analysis!

---

## How the breakthrough happened

### The problem (170 pages of freeze)
- C7:0000..C7:A7FF: All data/event script (confirmed)
- C7:B100: Showed code structure (3 returns, 2 prologues, 6 JSRs) but **weak callers**
- C7:C3xx: Had code indicators but **not promoted**
- **Circular dependency:** B100 needed strong C3xx anchors; C3xx needed promotion

### The solution (strategic jump)
1. **Jumped to C7:C300** (skipping C7:B200..C7:C2FF)
2. **Confirmed C7:C3xx as real code** (prologues, returns, cross-bank calls)
3. **Promoted C7:C300..C7:C4FF (pass 192)** - broke circular dependency
4. **Re-ran anchor reports** - C7:B100 callers now "strong"
5. **Promoted C7:B000..C7:B1FF (pass 193)** - milestone achieved!

### Key insight
Page family classification and xref counts can be misleading. **Strong anchor chains from resolved code** are the definitive validation.

---

## Updated C7 bank status

### Confirmed code regions (4 owner ranges)
| Region | Pass | Evidence |
|--------|------|----------|
| C7:7400..C7:74FF | Supporting | Anchor for C7:B188 |
| C7:B000..C7:B1FF | **193** | Strong anchors from C3xx/C0xx |
| C7:C000..C7:C2FF | Supporting | Anchor for C7:B111 |
| C7:C300..C7:C4FF | **192** | First upper C7 code, validates B100 |

### Remaining work
- **C7:B200..C7:BFFF:** ~160 pages (64KB - 22KB already covered)
- **Strategy:** Linear progression from C7:B200, or continue with C7:C500+ validation

---

## Running promotion count

- C5:3B00..44FF: 0 promotions (notes_14)
- ... (64 blocks of 0 promotions) ...
- C7:9E00..C7:A7FF: 0 promotions (notes_75)
- C7:A800..C7:B1FF: 0 promotions (notes_76)
- **C7:C300..C7:CCFF: 2 promotions** (THIS NOTE) 🎉
  - Pass 192: C7:C300..C7:C4FF (code)
  - Pass 193: C7:B000..C7:B1FF (code) **MILESTONE**

Total promotions since seam work began: **2** (C7:C300, C7:B100)

**The 170-page freeze streak is OVER!**

---

## Files generated

- `passes/manifests/pass192.json` - C7:C300 promotion
- `passes/manifests/pass193.json` - C7:B100 promotion **MILESTONE**
- `tools/cache/closed_ranges_snapshot_v1.json` - Updated (947 ranges)
- `reports/C7_B111_anchor_v3.json` - Strong anchor confirmed
- `reports/C7_B188_anchor_v3.json` - Strong anchor confirmed
- `reports/C7_B0B4_anchor_v3.json` - Strong anchor confirmed
- `reports/C7_B0DF_anchor_v3.json` - Strong anchor confirmed

---

## New live seam

**Effective seam:** C7:B200.. (unchanged, but now with C7:B000..B1FF as promoted code behind it)

**Options for continuing:**
1. **Linear progression:** C7:B200..BFFF (fill the gap)
2. **Continue validation:** C7:C500+ (extend the code region)
3. **Backfill:** C7:B200..BFFF (analyze the skipped region)

### Recommendation
Continue with **linear progression from C7:B200** to:
- Complete the C7 bank analysis
- Find connections between B100 and C300
- Discover additional code regions

---

## Lessons learned

### The 170-page freeze taught us:
1. **Zero returns = definitive data** (C7:A000, C7:9400)
2. **High xref count ≠ code** (C7:8400 8-target false positive)
3. **Page family unreliable** (90% candidate_code_lane was data)
4. **Strong anchors essential** (C7:B100 needed promoted C3xx)

### The breakthrough required:
1. **Strategic thinking** (jump to caller region)
2. **Circular dependency resolution** (promote C3xx first)
3. **Anchor chain validation** (re-run reports after promotion)
4. **Patience** (170 pages before first promotion)

### The verification hierarchy proved correct:
1. ✅ Returns present (hard requirement)
2. ✅ Strong anchors from resolved code (definitive)
3. ✅ Prologues (structural evidence)
4. ⚠️ Backtrack scores (moderate reliability)
5. ❌ Xref counts (can mislead)

---

## Next steps

1. `python tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:B200 --pages 10 --json > reports/c7_b200_bbff_seam_block.json`
2. Process the C7:B200..BFFF region to complete the bank
3. Look for additional code regions and connections to B100/C300
4. Write `docs/sessions/chrono_trigger_session15_continue_notes_79.md`

**The C7 bank is no longer frozen. Real code has been found and validated.**
