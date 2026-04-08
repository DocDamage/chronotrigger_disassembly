from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_rom_path() -> str:
    return str(repo_root() / 'rom' / 'Chrono Trigger (USA).sfc')


def delegate_to(script_name: str, forwarded_args: list[str]) -> int:
    script_path = Path(__file__).with_name(script_name)
    completed = subprocess.run([sys.executable, str(script_path), *forwarded_args])
    return completed.returncode
