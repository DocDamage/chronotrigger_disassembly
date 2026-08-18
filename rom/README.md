# ROM Setup and Verification

This repository does **NOT** distribute or track the commercial Super Nintendo ROM for *Chrono Trigger*.

## Providing Your ROM

Place your legally acquired, headerless USA release ROM in this directory:
```
rom/Chrono Trigger (USA).sfc
```

## Expected Checksums

| Algorithm | Expected Hash |
|---|---|
| SHA-256 | `06d1c2b06b716052c5596aaa0c2e5632a027fee1a9a28439e509f813c30829a9` |
| SHA-1 | `898471c6d3762886f4a8ac1f4ca74e2dbe655074` |
| MD5 | `a2bc447961e52fd2227baed164f7293c` |
| CRC32 | `2D206BF7` |
| File Size | `4,194,304` bytes (4.00 MiB) |

## Verification Tool

Verify your local ROM without modifying or uploading any files:
```powershell
python tools/scripts/verify_rom.py --rom "rom/Chrono Trigger (USA).sfc"
```
