"""Run tests, freeze actual artifacts, render reports, and package the submission."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    artifacts = ROOT / "report/artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    tests = subprocess.run([sys.executable, "-X", "utf8", "-m", "pytest", "tests/", "-v",
                            "--junitxml=report/artifacts/test_results.xml"],
                           cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    log = tests.stdout + tests.stderr
    (artifacts / "test_results.txt").write_text(log, encoding="utf-8")
    if tests.returncode:
        print(log)
        raise SystemExit(tests.returncode)
    print(log.strip().splitlines()[-1])
    for module in ("scripts.import_hiep", "scripts.import_dung", "scripts.run_benchmark", "scripts.build_reports", "scripts.package_submission"):
        subprocess.run([sys.executable, "-X", "utf8", "-m", module], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
