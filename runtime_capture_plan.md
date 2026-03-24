# Runtime Capture Plan

- Latest pass: **96**
- Live seam: **Do not go broad. The cleanest next move now is: 1. Tighten 0155 and the immediate bridge around the 0x18..0x3F family keep the whole C7 low-bank send path warm while the helper cluster is fresh 2. Then go back to CE0F the helper fog that was blocking the return is now gone**

Use this when static naming stalls or when you want hard proof for WRAM ownership, APU traffic, or selector-state transitions.

## Capture order
1. Start with the active C7 low-bank sound/APU seam while it is fresh.
2. Then capture WRAM validation around `CFFF`, `CDC8`, and `CE0F`.
3. Import traces into `traces/imported/` and rerun `python3 scripts/ct_resume_workspace.py --workdir .`.

## C7 low-bank sound/APU seam
Primary runtime capture for the live pass-96 seam. Use this to prove the `0x18..0x3F` bridge, `0155`, and the post-emit C7 low-bank path with real APU traffic.

### CPU break / trace points
- `C7:0140`
- `C7:0155`
- `C7:01A1`
- `C7:04B1`
- `C7:061C`
- `C7:0655`
- `C7:071D`
- `C7:0734`
- `C7:0755`
- `C7:08E3`
- `C7:0A39`

### WRAM / low-bank watches
- `00:1E00..00:1E10`
- `00:1E20..00:1E63`
- `00:1F00..00:1FC0`
- `7E:CFFF`
- `7E:CDC8`
- `7E:CE0F`

### APU / hardware ports
- `00:2140`
- `00:2141`
- `00:2142`
- `00:2143`

### Questions this capture should answer
- Which exact opcodes inside the `0x18..0x3F` bridge hit `0155`, `061C`, and `071D` in live play?
- What `1E00/1E01/1E05` values precede the negative-path `01A1` flow?
- What exact byte triplets hit `$2141/$2142/$2143` during `0755`, `08E3`, `0655`, and the `04B1` tail?
- Do `1E20..1E63` and `1F00..1FC0` behave like live slot strips and staged emit strips under runtime pressure?

### Suggested output file
- `traces/imported/c7_lowbank_sound_apu_trace.csv`

## CDC8 / CE0F / CFFF control return path
Follow-up runtime capture once the C7 seam cools off. Use this to prove the gate bytes that static work already narrowed down but has not fully named.

### CPU break / trace points
- `CE:E18E`
- `CD:18C2`
- `D1:E91A`
- `D1:E984`
- `D1:F431`
- `D1:F457`

### WRAM / low-bank watches
- `7E:CDC8`
- `7E:CE0F`
- `7E:CFFF`
- `7E:CD47..7E:CDC6`

### Questions this capture should answer
- When does `CDC8` flip from seed to promote state in real scenes?
- Does `CE0F` act like a phase byte, an arm byte, or both?
- What exact nonzero values does `CFFF` ever take outside the common `01` case?
- Which code paths actually clear the `CD47..CDC6` band when `CDC8` is nonzero?

### Suggested output file
- `traces/imported/cdc8_ce0f_cfff_runtime_trace.csv`

## WRAM ownership hotspots
Use this when you want to promote provisional WRAM labels with debugger-backed proof instead of pure static inference.

### CPU break / trace points
- `C1:B80D`
- `C1:AFD7`
- `C1:8C0A`
- `C1:8CE7`
- `C1:8D88`
- `FD:B8F7`

### WRAM / low-bank watches
- `7E:0B40..7E:0CBF`
- `7E:0CC0..7E:0E3F`
- `7E:0E80..7E:0FFF`
- `7E:99DD..7E:99DF`
- `7E:9F22..7E:9F24`
- `7E:AEFF..7E:AF15`
- `7E:AFAB..7E:AFB5`
- `7E:B03A..7E:B044`
- `7E:B158..7E:B162`
- `7E:B242`
- `7E:B24A`
- `7E:B263`

### Questions this capture should answer
- Which addresses are write-dominant versus read-dominant under normal gameplay?
- Which provisional WRAM nouns have repeated execute-adjacent proof from hot C1 callsites?
- Which hotspots still have no stable owner after live tracing and should stay provisional?

### Suggested output file
- `traces/imported/wram_hotspot_validation_trace.csv`

