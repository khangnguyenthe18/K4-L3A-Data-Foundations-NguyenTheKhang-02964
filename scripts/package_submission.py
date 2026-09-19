"""Create a source-only submission ZIP with a verified SHA-256 manifest."""
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "submission/K4-L3A-NguyenTheKhang-02964.zip"


def package() -> Path:
    files: list[Path] = []
    for directory in ("src", "scripts", "tests", "data", "benchmark", "report", "docs"):
        for path in (ROOT / directory).rglob("*"):
            relative = path.relative_to(ROOT)
            if (path.is_file() and not path.is_symlink()
                    and not any(part in {"__pycache__", ".pytest_cache", ".cache"} for part in relative.parts)
                    and path.name != "INSTRUCTOR_GUIDE.md"
                    and path.suffix.lower() in {".py", ".ps1", ".md", ".txt", ".json", ".csv", ".xml"}):
                files.append(path)
    for name in ("main.py", "README.md", "K4_VARIANT.md", "exercises.md", "requirements.txt",
                 "requirements-local.txt", ".python-version", ".gitignore", "ket_qua_benchmark.txt"):
        path = ROOT / name
        if not path.is_file():
            raise FileNotFoundError(path)
        files.append(path)
    files.sort(key=lambda path: path.relative_to(ROOT).as_posix())
    manifest = {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in files}
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DESTINATION, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(ROOT).as_posix())
        archive.writestr("MANIFEST.sha256.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    with zipfile.ZipFile(DESTINATION) as archive:
        if archive.testzip() is not None:
            raise ValueError("ZIP integrity check failed")
        for name, expected in manifest.items():
            if hashlib.sha256(archive.read(name)).hexdigest() != expected:
                raise ValueError(f"Manifest mismatch: {name}")
    print(f"Verified submission ZIP: {DESTINATION.name} ({len(files)} files, {DESTINATION.stat().st_size} bytes)")
    return DESTINATION


if __name__ == "__main__":
    package()
