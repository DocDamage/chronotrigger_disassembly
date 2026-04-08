#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import py_compile
import re
import subprocess
import sys
from pathlib import Path

import snes_utils
import snes_utils_hirom_v2


SCRIPT_REF_RE = re.compile(r'`(?P<path>tools/scripts/[^`]+\.py)`')
LOCAL_SCRIPT_REF_RE = re.compile(r'`(?P<name>[A-Za-z0-9_./-]+\.py)`')

CORE_ENTRYPOINTS = [
    'tools/scripts/find_next_callable_lane.py',
    'tools/scripts/build_call_anchor_report.py',
    'tools/scripts/classify_c3_ranges.py',
    'tools/scripts/validate_labels.py',
    'tools/scripts/publish_pass_bundle.py',
    'tools/scripts/update_bank_progress.py',
]

HELP_SMOKE_TARGETS = [
    'tools/scripts/find_next_callable_lane.py',
    'tools/scripts/build_call_anchor_report.py',
    'tools/scripts/classify_c3_ranges.py',
    'tools/scripts/validate_labels.py',
    'tools/scripts/publish_pass_bundle.py',
    'tools/scripts/update_bank_progress.py',
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Audit toolkit health, compatibility entrypoints, and low-bank mapping correctness')
    parser.add_argument('--output-json', default='reports/toolkit_doctor.json')
    parser.add_argument('--output-md', default='reports/toolkit_doctor.md')
    return parser.parse_args()


def add_check(results: list[dict[str, object]], name: str, ok: bool, details: object) -> None:
    results.append({'name': name, 'ok': ok, 'details': details})


def compile_check(root: Path) -> tuple[bool, dict[str, object]]:
    failures: list[dict[str, str]] = []
    scripts = sorted(root.glob('tools/scripts/*.py'))
    for path in scripts:
        try:
            py_compile.compile(str(path), doraise=True)
        except Exception as exc:  # pragma: no cover - surfaced in doctor output
            failures.append({'path': str(path.relative_to(root)).replace('\\', '/'), 'error': str(exc)})
    return (not failures, {'script_count': len(scripts), 'failures': failures})


def legacy_entrypoint_check(root: Path) -> tuple[bool, dict[str, object]]:
    missing: list[str] = []
    stub_markers: list[str] = []
    for rel in CORE_ENTRYPOINTS:
        path = root / rel
        if not path.exists():
            missing.append(rel)
            continue
        text = path.read_text(encoding='utf-8')
        if re.search(r"""print\(\s*f?['"]\[stub\]""", text):
            stub_markers.append(rel)
    return (not missing and not stub_markers, {'required': CORE_ENTRYPOINTS, 'missing': missing, 'stub_markers': stub_markers})


def collect_script_refs(root: Path) -> tuple[list[str], list[str]]:
    refs: list[str] = []
    workflow_path = root / 'tools/docs/workflow.md'
    workflow_text = workflow_path.read_text(encoding='utf-8')
    refs.extend(f"tools/scripts/{m.group('name')}" for m in LOCAL_SCRIPT_REF_RE.finditer(workflow_text) if '/' not in m.group('name'))

    for rel in ['README.md', 'tools/README.md']:
        text = (root / rel).read_text(encoding='utf-8')
        refs.extend(m.group('path') for m in SCRIPT_REF_RE.finditer(text))
    refs = sorted(set(refs))

    missing: list[str] = []
    for rel in refs:
        if not (root / rel).exists():
            missing.append(rel)
    return refs, missing


def readme_reference_check(root: Path) -> tuple[bool, dict[str, object]]:
    refs, missing = collect_script_refs(root)
    return (not missing, {'referenced_scripts': refs, 'missing': missing})


def low_bank_mapping_check() -> tuple[bool, dict[str, object]]:
    samples = [
        {'address': 'C3:0000', 'offset': 0x030000},
        {'address': 'C3:0557', 'offset': 0x030557},
        {'address': 'CF:F3DC', 'offset': 0x0FF3DC},
    ]
    mismatches: list[dict[str, object]] = []

    for sample in samples:
        bank, addr = snes_utils.parse_snes_address(sample['address'])
        legacy_offset = snes_utils.hirom_to_file_offset(bank, addr)
        legacy_roundtrip = f'{snes_utils.file_offset_to_snes(sample["offset"])[0]:02X}:{snes_utils.file_offset_to_snes(sample["offset"])[1]:04X}'
        v2_offset = snes_utils_hirom_v2.hirom_to_file_offset(bank, addr)
        v2_roundtrip = f'{snes_utils_hirom_v2.file_offset_to_snes(sample["offset"])[0]:02X}:{snes_utils_hirom_v2.file_offset_to_snes(sample["offset"])[1]:04X}'
        if legacy_offset != sample['offset'] or v2_offset != sample['offset'] or legacy_roundtrip != sample['address'] or v2_roundtrip != sample['address']:
            mismatches.append(
                {
                    'sample': sample,
                    'legacy_offset': legacy_offset,
                    'legacy_roundtrip': legacy_roundtrip,
                    'v2_offset': v2_offset,
                    'v2_roundtrip': v2_roundtrip,
                }
            )

    return (not mismatches, {'samples': samples, 'mismatches': mismatches})


def help_smoke_check(root: Path) -> tuple[bool, dict[str, object]]:
    failures: list[dict[str, object]] = []
    for rel in HELP_SMOKE_TARGETS:
        completed = subprocess.run(
            [sys.executable, str(root / rel), '--help'],
            cwd=root,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            failures.append(
                {
                    'script': rel,
                    'returncode': completed.returncode,
                    'stderr_tail': completed.stderr.splitlines()[-10:],
                }
            )
    return (not failures, {'smoke_targets': HELP_SMOKE_TARGETS, 'failures': failures})


def manifest_schema_smoke_check(root: Path) -> tuple[bool, dict[str, object]]:
    samples = [
        'passes/manifests/pass402.json',
        'passes/manifests/pass763.json',
    ]
    failures: list[dict[str, object]] = []
    for rel in samples:
        completed = subprocess.run(
            [sys.executable, str(root / 'tools/scripts/check_pass_manifest.py'), '--manifest', str(root / rel)],
            cwd=root,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            failures.append(
                {
                    'manifest': rel,
                    'returncode': completed.returncode,
                    'stdout_tail': completed.stdout.splitlines()[-10:],
                    'stderr_tail': completed.stderr.splitlines()[-10:],
                }
            )
    return (not failures, {'sample_manifests': samples, 'failures': failures})


def branch_state_smoke_check(root: Path) -> tuple[bool, dict[str, object]]:
    completed = subprocess.run(
        [sys.executable, str(root / 'tools/scripts/audit_branch_state_v1.py')],
        cwd=root,
        capture_output=True,
        text=True,
    )
    return (
        completed.returncode == 0,
        {
            'returncode': completed.returncode,
            'stdout_tail': completed.stdout.splitlines()[-12:],
            'stderr_tail': completed.stderr.splitlines()[-12:],
        },
    )


def render_markdown(data: dict[str, object]) -> str:
    lines = [
        '# Toolkit Doctor',
        '',
        f"- overall health: **{data['health_percent']:.1f}%**",
        f"- passing checks: **{data['passed_checks']} / {data['total_checks']}**",
        '',
        '## Checks',
        '',
    ]
    for item in data['checks']:
        status = 'ok' if item['ok'] else 'fail'
        lines.append(f"- **{item['name']}**: {status}")
        details_text = json.dumps(item['details'], indent=2)
        for line in details_text.splitlines():
            lines.append(f'  {line}')
    return '\n'.join(lines) + '\n'


def main() -> int:
    args = parse_args()
    root = repo_root()
    checks: list[dict[str, object]] = []

    ok, details = compile_check(root)
    add_check(checks, 'python_script_compile_health', ok, details)

    ok, details = legacy_entrypoint_check(root)
    add_check(checks, 'legacy_entrypoints_upgraded', ok, details)

    ok, details = readme_reference_check(root)
    add_check(checks, 'doc_script_references', ok, details)

    ok, details = low_bank_mapping_check()
    add_check(checks, 'low_bank_mapping', ok, details)

    ok, details = help_smoke_check(root)
    add_check(checks, 'core_help_smoke', ok, details)

    ok, details = manifest_schema_smoke_check(root)
    add_check(checks, 'manifest_schema_smoke', ok, details)

    ok, details = branch_state_smoke_check(root)
    add_check(checks, 'branch_state_audit', ok, details)

    passed = sum(1 for item in checks if item['ok'])
    total = len(checks)
    health = round((passed / total) * 100.0, 1) if total else 0.0

    report = {
        'generated_from': str(root),
        'health_percent': health,
        'passed_checks': passed,
        'total_checks': total,
        'checks': checks,
    }

    json_path = (root / args.output_json).resolve()
    md_path = (root / args.output_md).resolve()
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    md_path.write_text(render_markdown(report), encoding='utf-8')

    print(str(json_path.relative_to(root)).replace('\\', '/'))
    print(str(md_path.relative_to(root)).replace('\\', '/'))
    return 0 if passed == total else 1


if __name__ == '__main__':
    raise SystemExit(main())
