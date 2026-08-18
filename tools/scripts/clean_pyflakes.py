#!/usr/bin/env python3
"""Automatically clean up pyflakes warnings across tools and tests."""

import re
import subprocess
import sys
from pathlib import Path

def run_pyflakes():
    res = subprocess.run([sys.executable, "-m", "pyflakes", "tools", "tests"], capture_output=True, text=True)
    return res.stdout.splitlines()

def main():
    lines = run_pyflakes()
    print(f"Initial pyflakes warnings: {len(lines)}")
    
    # Process each warning
    for line in lines:
        if "imported but unused" in line:
            # File:line:col: 'foo' imported but unused
            m = re.match(r'^([^:]+):(\d+):(?:\d+:)?\s*\'([^\']+)\' imported but unused', line)
            if m:
                filepath, lineno_str, imp_name = m.group(1), int(m.group(2)), m.group(3)
                p = Path(filepath)
                if p.exists():
                    f_lines = p.read_text(encoding='utf-8').splitlines()
                    idx = lineno_str - 1
                    if idx < len(f_lines):
                        orig_line = f_lines[idx]
                        short_name = imp_name.split('.')[-1]
                        # If single import line like 'import os' or 'from x import y'
                        if orig_line.strip() in (f"import {imp_name}", f"import {short_name}", f"from {imp_name.rsplit('.', 1)[0]} import {short_name}"):
                            f_lines[idx] = ""
                        elif f", {short_name}" in orig_line:
                            f_lines[idx] = orig_line.replace(f", {short_name}", "")
                        elif f"{short_name}, " in orig_line:
                            f_lines[idx] = orig_line.replace(f"{short_name}, ", "")
                        elif f"import {short_name}" in orig_line:
                            f_lines[idx] = ""
                        p.write_text("\n".join(f_lines) + "\n", encoding='utf-8')

        elif "f-string is missing placeholders" in line:
            # File:line:col: f-string is missing placeholders
            m = re.match(r'^([^:]+):(\d+):(?:\d+:)?\s*f-string is missing placeholders', line)
            if m:
                filepath, lineno_str = m.group(1), int(m.group(2))
                p = Path(filepath)
                if p.exists():
                    f_lines = p.read_text(encoding='utf-8').splitlines()
                    idx = lineno_str - 1
                    if idx < len(f_lines):
                        orig_line = f_lines[idx]
                        # Replace f" or f' with " or ' if no { in line
                        # Be careful with multiline
                        new_line = re.sub(r'f(["\'])', r'\1', orig_line)
                        f_lines[idx] = new_line
                        p.write_text("\n".join(f_lines) + "\n", encoding='utf-8')

    remaining = run_pyflakes()
    print(f"Remaining pyflakes warnings after automated pass: {len(remaining)}")
    for r in remaining:
        print(" ", r)

if __name__ == "__main__":
    main()
