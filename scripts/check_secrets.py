from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\b[0-9a-fA-F]{32,}\b"),
    re.compile(r"\b[A-Za-z0-9]{40,}\b"),
    re.compile(r"^\s*(?:TUSHARE_TOKEN|TS_TOKEN)\s*="),
    re.compile(r"\bapi_key\s*="),
    re.compile(r"\bpro_api\s*\(\s*token\s*="),
)

SKIP_DIRS = {
    ".git",
    ".claude",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    ".ipynb_checkpoints",
    ".index_pricing_cache",
    ".index_pricing_local",
}
SKIP_FILES = {".env.example", "CLAUDE.md", "LICENSE", "check_secrets.py"}
TEXT_EXTS = {
    ".cfg",
    ".css",
    ".dockerignore",
    ".example",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".py",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}


def _staged_files() -> list[Path]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [Path(line) for line in result.stdout.splitlines() if line.strip()]


def _working_tree_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path.relative_to(root))
    return files


def _is_text_candidate(path: Path) -> bool:
    if path.name in SKIP_FILES:
        return False
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    if path.suffix in TEXT_EXTS:
        return True
    return path.name in {
        ".gitignore",
        ".pre-commit-config.yaml",
        "Dockerfile",
        "docker-compose.yml",
    }


def _scan_file(path: Path) -> bool:
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    found = False
    for lineno, line in enumerate(content.splitlines(), start=1):
        if any(pattern.search(line) for pattern in SECRET_PATTERNS):
            print(f"{path}:{lineno}: potential secret pattern", file=sys.stderr)
            found = True
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan files for token-shaped secrets without printing values.")
    parser.add_argument("--staged", action="store_true", help="Scan staged files only.")
    args = parser.parse_args()

    root = Path.cwd()
    files = _staged_files() if args.staged else _working_tree_files(root)
    failed = False
    for rel_path in files:
        if not _is_text_candidate(rel_path):
            continue
        if _scan_file(root / rel_path):
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
