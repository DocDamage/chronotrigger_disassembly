# Emulator Setup and Documentation

This directory contains configuration and documentation for SNES emulation used during reverse-engineering verification.

## Supported Emulators

- **bsnes-plus / bsnes**: Recommended for cycle-accurate debugging, memory tracing, and breakpoint verification.
- **Snes9x**: Lightweight testing and quick savestate verification.

## Licensing and Provenance

- Emulator binaries must comply with their respective open-source licenses (GPLv2/GPLv3).
- Pre-compiled binaries should not be committed to the Git working tree. Users should download approved releases directly from upstream repositories:
  - [bsnes-plus releases](https://github.com/devinacker/bsnes-plus)
  - [Snes9x releases](https://github.com/snes9xgit/snes9x)
