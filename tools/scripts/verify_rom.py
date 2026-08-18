#!/usr/bin/env python3
"""Standalone ROM verification utility."""

import argparse
import hashlib
import os
import sys

EXPECTED_SHA256 = "06d1c2b06b716052c5596aaa0c2e5632a027fee1a9a28439e509f813c30829a9"
EXPECTED_SIZE = 4194304

def sha256_file(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    parser = argparse.ArgumentParser(description="Verify local Chrono Trigger ROM against expected SHA-256.")
    parser.add_argument("--rom", default="rom/Chrono Trigger (USA).sfc", help="Path to local ROM file")
    args = parser.parse_args()

    if not os.path.exists(args.rom):
        print(f"Error: ROM file not found at '{args.rom}'.")
        print("Please place a verified USA release ROM at that path.")
        return 1

    size = os.path.getsize(args.rom)
    computed_sha256 = sha256_file(args.rom)

    print(f"Checking ROM: {args.rom}")
    print(f"File Size: {size:,} bytes (expected {EXPECTED_SIZE:,} bytes)")
    print(f"SHA-256:   {computed_sha256}")

    if size != EXPECTED_SIZE:
        print(f"WARNING: File size mismatch ({size} != {EXPECTED_SIZE}). Is this a headered ROM?")

    if computed_sha256.lower() == EXPECTED_SHA256.lower():
        print("RESULT: PASS — ROM matches verified Chrono Trigger (USA) release.")
        return 0
    else:
        print("RESULT: FAIL — SHA-256 mismatch.")
        print(f"Expected: {EXPECTED_SHA256}")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
