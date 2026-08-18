#!/usr/bin/env python3
"""Compatibility entrypoint for durable range adjudication.

This command no longer edits manifests or creates reviewed waivers. It builds the
explicit ownership ledger consumed by migration.
"""

from tools.scripts.adjudicate_range_conflicts import main


if __name__ == "__main__":
    raise SystemExit(main())
