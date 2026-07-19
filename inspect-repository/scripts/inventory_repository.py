#!/usr/bin/env python3
"""
inventory_repository.py - Safely inventory files and directories in a repository.

Generates structured JSON detailing file categories, size metrics, ignored folders,
binary file classification, and inspection coverage without exposing secret content.
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Directories to skip contents of (content-ignored directories)
IGNORED_DIR_NAMES = {
    "node_modules", ".git", "dist", "build", "coverage", "target", "out",
    ".next", ".nuxt", "vendor", "__pycache__", ".pytest_cache", ".mypy_cache",
    ".tox", "venv", ".venv", "env", ".idea", ".vscode", "cache", ".cache",
    "bin", "obj", ".gradle"
}

# Extension & pattern classifications
CATEGORY_PATTERNS = {
    "dependency_manifest": {
        "package.json", "requirements.txt", "pyproject.toml", "Cargo.toml", "go.mod",
        "Gemfile", "composer.json", "pom.xml", "build.gradle", "settings.gradle",
        "pubspec.yaml", "Podfile", "Package.swift", "Pipfile", "Mix.exs"
    },
    "lock_file": {
        "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock", "Pipfile.lock",
        "Cargo.lock", "go.sum", "Gemfile.lock", "composer.lock", "pubspec.lock"
    },
    "container": {
        "Dockerfile", "docker-compose.yml", "docker-compose.yaml", "Containerfile"
    },
    "cicd": {
        ".gitlab-ci.yml", "Jenkinsfile", ".travis.yml", "azure-pipelines.yml"
    }
}

EXTENSION_MAP = {
    # Source Code
    ".py": "source_code", ".js": "source_code", ".ts": "source_code", ".jsx": "source_code",
    ".tsx": "source_code", ".java": "source_code", ".c": "source_code", ".cpp": "source_code",
    ".h": "source_code", ".hpp": "source_code", ".cs": "source_code", ".go": "source_code",
    ".rs": "source_code", ".rb": "source_code", ".php": "source_code", ".swift": "source_code",
    ".kt": "source_code", ".scala": "source_code", ".ex": "source_code", ".exs": "source_code",
    ".sh": "script", ".ps1": "script", ".bat": "script", ".cmd": "script",
    # Configuration
    ".json": "configuration", ".yaml": "configuration", ".yml": "configuration",
    ".toml": "configuration", ".env.example": "configuration", ".ini": "configuration",
    ".xml": "configuration", ".properties": "configuration",
    # Database & Migrations
    ".sql": "migration", ".db": "database", ".sqlite": "database", ".sqlite3": "database",
    # Documentation
    ".md": "documentation", ".rst": "documentation", ".txt": "documentation",
    # Infrastructure
    ".tf": "infrastructure", ".tfvars": "infrastructure", ".bicep": "infrastructure",
    # Tests
    ".spec.js": "test", ".test.js": "test", ".spec.ts": "test", ".test.ts": "test",
    # Images & Media
    ".png": "image", ".jpg": "image", ".jpeg": "image", ".gif": "image", ".svg": "image",
    ".webp": "image", ".ico": "image",
    # Models & Data
    ".onnx": "model", ".pth": "model", ".pt": "model", ".bin": "model", ".safetensors": "model",
    ".csv": "data_file", ".tsv": "data_file", ".parquet": "data_file",
    # Archives & Binaries
    ".zip": "archive", ".tar": "archive", ".gz": "archive", ".7z": "archive",
    ".exe": "binary", ".dll": "binary", ".so": "binary", ".dylib": "binary", ".class": "binary",
    ".pyc": "binary"
}

def is_binary_file(file_path: Path, sample_size: int = 1024) -> bool:
    """Check if a file appears to be binary by reading a small chunk."""
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(sample_size)
            if b"\x00" in chunk:
                return True
            # Check non-text ratio
            if not chunk:
                return False
            text_characters = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
            non_text = chunk.translate(None, text_characters)
            return len(non_text) / len(chunk) > 0.3
    except Exception:
        return False

def classify_file(file_path: Path, filename: str) -> str:
    """Classify file into one of 22 standard categories."""
    # Check filename exact matches
    for category, filenames in CATEGORY_PATTERNS.items():
        if filename in filenames or filename.lower() in filenames:
            return category

    if ".github/workflows" in str(file_path).replace("\\", "/"):
        return "cicd"

    # Check path indicators for test / migration
    path_str = str(file_path).lower().replace("\\", "/")
    if "/test/" in path_str or "/tests/" in path_str or filename.startswith("test_") or filename.endswith("_test.go"):
        return "test"
    if "/migration/" in path_str or "/migrations/" in path_str:
        return "migration"

    # Check extensions
    ext = file_path.suffix.lower()
    if ext in EXTENSION_MAP:
        return EXTENSION_MAP[ext]

    return "unknown"

def inventory_repository(root_dir: str, max_file_size_kb: int = 1024) -> dict:
    """Perform deterministic safe repository inventory."""
    root = Path(root_dir).resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Invalid directory path: {root_dir}")

    total_files_discovered = 0
    files_analyzed = 0
    binary_files_excluded = 0
    large_files_sampled = 0
    ignored_directories_found = set()

    categories = {}
    file_list = []
    seen_paths = set()

    for current_root, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current_root)
        
        # Check if current directory or parent is in ignored list
        rel_parts = current_path.relative_to(root).parts
        ignored_ancestors = [p for p in rel_parts if p in IGNORED_DIR_NAMES]
        
        if ignored_ancestors:
            ignored_directories_found.add(ignored_ancestors[0])
            # Don't recurse into ignored directories
            dirs[:] = []
            continue

        # Prune ignored subdirectories from dirs list
        for d in list(dirs):
            if d in IGNORED_DIR_NAMES:
                ignored_directories_found.add(d)
                dirs.remove(d)

        for filename in files:
            total_files_discovered += 1
            file_path = current_path / filename

            # Prevent loop/duplicate
            try:
                real_path = file_path.resolve()
            except Exception:
                real_path = file_path

            if real_path in seen_paths:
                continue
            seen_paths.add(real_path)

            rel_path_str = str(file_path.relative_to(root)).replace("\\", "/")

            try:
                stat = file_path.stat()
                size_bytes = stat.st_size
                size_kb = round(size_bytes / 1024.0, 2)
            except Exception as e:
                file_list.append({
                    "path": rel_path_str,
                    "category": "unreadable",
                    "size_bytes": 0,
                    "error": str(e)
                })
                continue

            category = classify_file(file_path, filename)
            is_bin = is_binary_file(file_path) if size_bytes > 0 else False
            is_large = size_kb > max_file_size_kb

            if is_bin and category not in ("image", "model", "archive", "binary"):
                category = "binary"

            if is_bin:
                binary_files_excluded += 1

            if is_large:
                large_files_sampled += 1

            categories[category] = categories.get(category, 0) + 1
            files_analyzed += 1

            file_list.append({
                "path": rel_path_str,
                "category": category,
                "size_bytes": size_bytes,
                "size_kb": size_kb,
                "is_binary": is_bin,
                "is_large": is_large
            })

    result = {
        "repository_root": str(root),
        "total_files_discovered": total_files_discovered,
        "files_analyzed": files_analyzed,
        "binary_files_excluded": binary_files_excluded,
        "large_files_sampled": large_files_sampled,
        "ignored_directories_detected": sorted(list(ignored_directories_found)),
        "categories_summary": categories,
        "files": file_list
    }
    return result

def main():
    parser = argparse.ArgumentParser(description="Inventory repository files safely.")
    parser.add_argument("--root", required=True, help="Path to repository root directory")
    parser.add_argument("--output", help="Path to output JSON file (default: stdout)")
    parser.add_argument("--max-size-kb", type=int, default=1024, help="Large file size threshold in KB")
    args = parser.parse_args()

    try:
        inventory_data = inventory_repository(args.root, args.max_size_kb)
        json_output = json.dumps(inventory_data, indent=2, ensure_ascii=False)

        if args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(json_output)
            print(f"Inventory saved to {args.output}")
        else:
            print(json_output)
    except Exception as e:
        print(f"Error executing inventory_repository: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
