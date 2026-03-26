# Chrono Trigger Disassembly Toolkit

This folder is the repo-native home for the active reverse-engineering toolkit.

## Goals
- keep tooling versioned with the disassembly work
- eliminate stale zip/tool drift
- make every pass reproducible
- separate source scripts from generated pass artifacts
- support repo-first workflow on the live working branch

## Layout
- `scripts/` — executable helpers and report generators
- `config/` — schemas, rules, scoring weights, and tracked indexes
- `docs/` — workflow notes, confidence rules, repo layout, and conventions
- `requirements.txt` — lightweight Python dependency note

## Core workflow
1. derive the next callable/data target
2. inspect bytes / xrefs / boundaries
3. close the pass honestly
4. publish one pass bundle
5. update bank progress and pass manifest
6. validate labels and overlapping owners/helpers
7. commit the result to the working branch

## Current missing-capability backlog
See `../reports/toolkit_missing_capabilities.md`.
