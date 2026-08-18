"""Unified task runner and CLI entrypoint for Chrono Trigger Disassembly toolkit."""

import argparse
import sys
import subprocess
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

def run_check(args):
    from tools.scripts.check_all_manifests import main as check_main
    sys.argv = ["check_all_manifests.py", "--strict"]
    return check_main()

def run_test(args):
    return subprocess.call([sys.executable, "-m", "pytest", "-q"], cwd=str(repo_root))

def run_coverage(args):
    from tools.scripts.generate_coverage import main as cov_main
    sys.argv = ["generate_coverage.py", "--strict"]
    return cov_main()

def run_doctor(args):
    from tools.scripts.toolkit_doctor import main as doc_main
    sys.argv = ["toolkit_doctor.py", "--strict"]
    return doc_main()

def run_verify_rom(args):
    from tools.scripts.verify_rom import main as rom_main
    sys.argv = ["verify_rom.py", "--rom", args.rom]
    return rom_main()

def main() -> int:
    parser = argparse.ArgumentParser(description="Chrono Trigger Disassembly Toolkit CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # check
    p_check = subparsers.add_parser("check", help="Run strict manifest and range validation")
    p_check.set_defaults(func=run_check)

    # test
    p_test = subparsers.add_parser("test", help="Run automated test suite")
    p_test.set_defaults(func=run_test)

    # coverage
    p_cov = subparsers.add_parser("coverage", help="Rebuild coverage report from canonical manifests")
    p_cov.set_defaults(func=run_coverage)

    # doctor
    p_doc = subparsers.add_parser("doctor", help="Run comprehensive repository health checks")
    p_doc.set_defaults(func=run_doctor)

    # verify-rom
    p_rom = subparsers.add_parser("verify-rom", help="Verify local ROM SHA-256")
    p_rom.add_argument("--rom", default="rom/Chrono Trigger (USA).sfc", help="Path to local ROM")
    p_rom.set_defaults(func=run_verify_rom)

    args = parser.parse_args()
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
