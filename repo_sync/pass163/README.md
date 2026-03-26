# Chrono Trigger repo-first bootstrap at pass 163

This sync establishes a repo-side starting point for the active ChatGPT-driven disassembly workflow.

## Synced state
- active master handoff: session 9
- latest closed pass: 163
- current live seam: `C3:0307..C3:0528`
- completion estimate: `~70.2%`
- toolkit baseline in local workspace: `v6.8 pass161 upgraded`

## Why this sync exists
The working state had been living mainly in chat-uploaded artifacts and the extracted local toolkit workspace. That makes continuity fragile. This bootstrap copies the current authoritative markdown artifacts into the repository so future passes can treat the repo as the canonical history lane.

## Included files
- session 9 master handoff
- pass 163 disassembly note
- pass 163 labels note
- pass 163 next-session start file
- pass 163 session packet
- pass 163 completion score
- pass 163 consistency report
- pass 163 toolkit doctor report
- pass 163 workspace report
- local workspace toolkit README used during this sync

## Important repo policy going forward
- do not commit the ROM
- do not treat older chat attachments as canonical once the repo copy exists
- future pass artifacts should be added from the latest live pass forward
- keep callable-boundary corrections explicit when a seam must be split honestly

## Immediate next target after this sync
- inspect and close the live seam at `C3:0307..C3:0528`
