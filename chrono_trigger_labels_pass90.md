# Chrono Trigger Labels — Pass 90

## Purpose
Pass 89 froze the local D1 write-side cluster, but it still lacked the exact caller-side contract.

Pass 90 closes that seam.

The strongest keepable result is:

- `D1:F331..F410` is an exact local seed/reset + four-stage follow-up invoke orchestrator
- `D1:F83D..F8EA` is an exact quartet-table seed helper for `C030..C14F`
- `D1:F474..F47B` is an exact `C0:FE00` lookup helper indexed by `A + 7C`
- `D1:F47C..F4BF` is the exact `CA5A / CA5C` masked-pair staging path
- `CA5A..CA5D` can now be strengthened as real center-offset seed words paired with `CA5E..CA60`

I am still keeping the final gameplay-facing nouns of the broader pipeline one notch below frozen.

---

## Strong labels

### D1:F331..D1:F410  ct_d1_seed_local_lane_and_raster_workspace_then_invoke_four_stage_followup_pipeline   [strong structural]
- Clears `C861 / C862`.
- Seeds `CD46` from `2A21.bit0` as exact `00` vs `FD`.
- Seeds exact constants into `C14F / C150`, `BEA1 / BEA5 / BEA9`, `CA04 / CA08 / CA0C / CA10 / CA14`, and `C02B / C02D`.
- Calls the already-frozen `D1:F411` descriptor-header snapshot helper.
- Seeds exact stepped table families at `BEAB/BEAD` and `BF6B/BF6D`.
- Fills both `C161` and `C4E1` with `0x00FF` across an exact `0x0380` span.
- Clears `BB05` across an exact `0x0180` span.
- Copies `2030..203E` into `CCEE..CCFC`.
- Runs the exact tail `CE:EE6E -> D1:F83D -> CD:0235 -> C0:0008`, then increments `CAD3` and returns.
- Strongest safe reading: local orchestrator for the pass-88/89 lane+raster build pipeline.

### D1:F83D..D1:F8EA  ct_d1_seed_c030_c090_c0f0_c120_quartet_table_family_and_tail_sentinels   [strong structural]
- Clears `C02F..C14E` across an exact `0x0120`-byte span.
- Builds 24 exact 4-byte records in the `C030/C031` and `C090/C091` neighborhoods using running words stepped by `-0x55` and `+0x55`.
- Builds 12 exact 4-byte records in the `C0F0/C0F1` and `C120/C121` neighborhoods using running words stepped by `-0xAA` and `+0xAA`.
- Seeds `C0ED = 0xE0` and `C14D = 0xE0`.
- Clears `C0EB / C0EC / C0EE / C14B / C14C / C14E`.
- Strongest safe reading: quartet-table seed helper immediately upstream of `CD:0235 / C0:0008`.

### D1:F474..D1:F47B  ct_d1_lookup_c0fe00_byte_indexed_by_a_plus_7c   [strong helper]
- Exact body: `ADC $7C ; TAX ; LDA C0:FE00,X ; RTS`.
- Strongest safe reading: tiny lookup helper over table `C0:FE00`, indexed by `A + 7C`.

### D1:F47C..D1:F4BF  ct_d1_stage_negated_masked_pair_into_ca5a_ca5c_from_stream_and_c0fe00_lookup   [strong structural]
- Reads two exact stream-side bytes through `[$40]` / `[$40],Y`.
- Uses `D1:F474` to fetch lookup bytes from `C0:FE00` indexed by `A + 7C`.
- Applies `AND` with the saved stream byte, then adds the corresponding base stream byte.
- Stores exact negated 16-bit results into `CA5A,X` and `CA5C,X` for the runtime slot selected by `43`.
- Advances the stream pointer by 2 before returning.
- Strongest safe reading: masked-pair staging helper for the `CA5A / CA5C` center-offset seed words.

---

## Strengthened RAM / workspace labels

### 7E:CA5A..7E:CA5D  ct_d1_primary_curve_center_offset_seed_words_paired_with_ca5e_ca60   [provisional strengthened]
- Pass 90 proves `D1:F47C..F4BF` writes exact negated 16-bit seed words into `CA5A,X` and `CA5C,X`.
- Pass 89 already proved `D1:EEC5..F107` builds the local center words from `CA5A + CA5E` and `CA5C + CA60`.
- Strongest safe reading: center-offset seed words paired with the already-frozen `CA5E / CA60` accumulator fields.

### 7E:C030..7E:C14F  ct_d1_local_quartet_table_family_upstream_of_cd0235_c00008   [provisional strengthened]
- Pass 90 proves `D1:F83D..F8EA` clears and seeds exact quartets at `C030/C031`, `C090/C091`, `C0F0/C0F1`, and `C120/C121`, plus the exact tail bytes near `C0EB..C0EE` and `C14B..C14E`.
- `D1:F331..F410` calls this helper immediately before `CD:0235` and `C0:0008`.
- Strongest safe reading: local quartet-table family immediately upstream of the final follow-up tail.

### 7E:CD46  ct_cd_auxiliary_token_f5_immediate_or_2a21_seeded_pipeline_byte   [provisional strengthened]
- Earlier passes proved token `0xF5` writes this byte directly.
- Pass 90 adds an exact non-token seed path: `D1:F331..F410` writes `00` or `FD` here from `2A21.bit0`.
- Final gameplay-facing noun still open.

---

## Honest caution kept explicit
Even after this pass:

- I have **not** frozen the final gameplay-facing noun of the `C030..C14F` quartet family.
- I have **not** frozen the final gameplay-facing noun of the broader pass-88/89 lane+raster workspace.
- I have **not** frozen the exact final roles of `CE:EE6E`, `CD:0235`, or `C0:0008`.
- I have **not** frozen the first exact clean-code external reader of `CE0F`.
