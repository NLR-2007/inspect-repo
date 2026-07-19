#!/usr/bin/env python3
"""
analyze_repository_structure.py - Map application entry points, modules, services, and architecture.

Scans the repository to build a comprehensive map of core components, API endpoints,
database schemas, controllers, entry points, and test suites.
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path

ENTRY_POINT_PATTERNS = [
    r"^main\.(py|js|ts|go|rs|cpp|c|scala|kt)$",
    r"^app\.(py|js|ts|rb|php)$",
    r"^server\.(js|ts|py|go)$",
    r"^index\.(js|ts|html|php)$",
    r"^manage\.py$",
    r"^Application\.(java|kt)$",
    r"^wsgi\.py$", r"^asgi\.py$",
    r"^cli\.(py|js|ts)$"
]

MODULE_TYPE_PATTERNS = {
    "controllers": [r"/controllers?/", r"/handlers?/", r"/endpoints?/", r"/routes?/"],
    "services": [r"/services?/", r"/providers?/", r"/usecases?/"],
    "models": [r"/models?/", r"/entities?/", r"/schemas?/", r"/domain/"],
    "views": [r"/views?/", r"/components?/", r"/pages?/", r"/ui/"],
    "middleware": [r"/middleware/", r"/interceptors?/"],
    "database": [r"/db/", r"/database/", r"/migrations?/", r"/repository/"],
    "utils": [r"/utils?/", r"/helpers?/", r"/common/", r"/shared/"],
    "config": [r"/config/", r"/settings/"],
    "tests": [r"/tests?/", r"/spec/"],
    "scripts": [r"/scripts?/", r"/bin/"]
}

ROUTE_DECLARATION_PATTERNS = [
    r'@app\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']',  # FastAPI / Flask
    r'router\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']', # Express / NestJS
    r'@([A-Z]\w+Mapping)\(["\']([^"\']+)["\']',                  # Spring Boot
    r'r\.(GET|POST|PUT|DELETE|PATCH)\(["\']([^"\']+)["\']',      # Gin (Go)
]

def find_entry_points(root: Path) -> list:
    """Locate application entry point files."""
    entry_points = []
    for file_path in root.glob("**/*"):
        if any(p in file_path.parts for p in ["node_modules", ".git", "venv", ".venv", "dist", "build"]):
            continue
        if file_path.is_file():
            name = file_path.name
            for pat in ENTRY_POINT_PATTERNS:
                if re.match(pat, name, re.IGNORECASE):
                    rel_p = str(file_path.relative_to(root)).replace("\\", "/")
                    entry_points.append({
                        "path": rel_p,
                        "filename": name,
                        "type": "Application Entry Point"
                    })
                    break
    return entry_points

def map_modules(root: Path) -> dict:
    """Categorize repository files into architectural modules."""
    module_map = {k: [] for k in MODULE_TYPE_PATTERNS.keys()}
    module_map["other"] = []

    for file_path in root.glob("**/*"):
        if any(p in file_path.parts for p in ["node_modules", ".git", "venv", ".venv", "dist", "build"]):
            continue
        if file_path.is_file():
            rel_p = str(file_path.relative_to(root)).replace("\\", "/")
            matched = False
            for mod_type, patterns in MODULE_TYPE_PATTERNS.items():
                for pat in patterns:
                    if re.search(pat, f"/{rel_p}/", re.IGNORECASE):
                        module_map[mod_type].append(rel_p)
                        matched = True
                        break
                if matched:
                    break

    return {k: v for k, v in module_map.items() if v}

def discover_routes(root: Path) -> list:
    """Scan code files to discover API route definitions."""
    discovered_routes = []
    for file_path in root.glob("**/*"):
        if any(p in file_path.parts for p in ["node_modules", ".git", "venv", ".venv", "dist", "build"]):
            continue
        if file_path.suffix.lower() in [".py", ".js", ".ts", ".go", ".java"]:
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                lines = content.splitlines()
                rel_p = str(file_path.relative_to(root)).replace("\\", "/")

                for idx, line in enumerate(lines, 1):
                    for pat in ROUTE_DECLARATION_PATTERNS:
                        match = re.search(pat, line)
                        if match:
                            method = match.group(1).upper()
                            endpoint = match.group(2)
                            discovered_routes.append({
                                "method": method,
                                "endpoint": endpoint,
                                "defined_in": rel_p,
                                "line_number": idx,
                                "snippet": line.strip()
                            })
            except Exception:
                continue

    return discovered_routes

def analyze_repository_structure(root_dir: str) -> dict:
    """Main repository structure analysis."""
    root = Path(root_dir).resolve()
    if not root.exists():
        raise ValueError(f"Directory not found: {root_dir}")

    entry_points = find_entry_points(root)
    modules = map_modules(root)
    routes = discover_routes(root)

    return {
        "repository_root": str(root),
        "entry_points": entry_points,
        "entry_points_count": len(entry_points),
        "module_architecture": modules,
        "discovered_routes_count": len(routes),
        "routes": routes
    }

def main():
    parser = argparse.ArgumentParser(description="Analyze repository architectural structure.")
    parser.add_argument("--root", required=True, help="Repository root directory")
    parser.add_argument("--output", help="Output JSON path")
    args = parser.parse_args()

    try:
        data = analyze_repository_structure(args.root)
        out_json = json.dumps(data, indent=2, ensure_ascii=False)
        if args.output:
            out_p = Path(args.output)
            out_p.parent.mkdir(parents=True, exist_ok=True)
            out_p.write_text(out_json, encoding="utf-8")
            print(f"Structure analysis saved to {args.output}")
        else:
            print(out_json)
    except Exception as e:
        print(f"Error executing analyze_repository_structure: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
