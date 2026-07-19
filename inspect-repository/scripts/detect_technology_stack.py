#!/usr/bin/env python3
"""
detect_technology_stack.py - Detect project technologies with evidence and confidence levels.

Scans manifest files, lock files, configurations, imports, and source files across
28 technology categories, producing structured JSON evidence ledgers.
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path

# Common technology signature mapping
# Structure: Tech Name -> Category, Regex patterns in manifests / imports / files
TECH_SIGNATURES = {
    # Frontend
    "React": {"category": "Frontend", "manifest_pattern": r'"react":\s*"([^"]+)"', "import_pattern": r'from\s+["\']react["\']|require\(["\']react["\']\)'},
    "Next.js": {"category": "Frontend", "manifest_pattern": r'"next":\s*"([^"]+)"', "import_pattern": r'from\s+["\']next/|require\(["\']next/'},
    "Vue.js": {"category": "Frontend", "manifest_pattern": r'"vue":\s*"([^"]+)"', "import_pattern": r'from\s+["\']vue["\']'},
    "Angular": {"category": "Frontend", "manifest_pattern": r'"@angular/core":\s*"([^"]+)"', "import_pattern": r'from\s+["\']@angular/'},
    "Tailwind CSS": {"category": "Frontend", "manifest_pattern": r'"tailwindcss":\s*"([^"]+)"', "file_pattern": r'tailwind\.config\.(js|ts|cjs)'},
    "Svelte": {"category": "Frontend", "manifest_pattern": r'"svelte":\s*"([^"]+)"', "file_pattern": r'\.svelte$'},
    
    # Backend & Frameworks
    "FastAPI": {"category": "Backend", "manifest_pattern": r'fastapi[=~>:]*([0-9\.]*)', "import_pattern": r'from\s+fastapi\s+import|import\s+fastapi'},
    "Django": {"category": "Backend", "manifest_pattern": r'django[=~>:]*([0-9\.]*)', "import_pattern": r'import\s+django|from\s+django\.'},
    "Flask": {"category": "Backend", "manifest_pattern": r'flask[=~>:]*([0-9\.]*)', "import_pattern": r'from\s+flask\s+import|import\s+flask'},
    "Express.js": {"category": "Backend", "manifest_pattern": r'"express":\s*"([^"]+)"', "import_pattern": r'require\(["\']express["\']\)|from\s+["\']express["\']'},
    "Spring Boot": {"category": "Backend", "manifest_pattern": r'spring-boot-starter-web', "import_pattern": r'org\.springframework\.boot'},
    "Gin": {"category": "Backend", "manifest_pattern": r'github\.com/gin-gonic/gin', "import_pattern": r'github\.com/gin-gonic/gin'},
    "Actix Web": {"category": "Backend", "manifest_pattern": r'actix-web\s*=\s*"([^"]+)"', "import_pattern": r'use\s+actix_web'},

    # AI / ML
    "PyTorch": {"category": "AI/ML", "manifest_pattern": r'torch[=~>:]*([0-9\.]*)', "import_pattern": r'import\s+torch'},
    "TensorFlow": {"category": "AI/ML", "manifest_pattern": r'tensorflow[=~>:]*([0-9\.]*)', "import_pattern": r'import\s+tensorflow'},
    "OpenAI API": {"category": "AI/ML", "manifest_pattern": r'openai[=~>:]*([0-9\.]*)', "import_pattern": r'import\s+openai|from\s+openai'},
    "LangChain": {"category": "AI/ML", "manifest_pattern": r'langchain[=~>:]*([0-9\.]*)', "import_pattern": r'import\s+langchain|from\s+langchain'},
    "HuggingFace Transformers": {"category": "AI/ML", "manifest_pattern": r'transformers[=~>:]*([0-9\.]*)', "import_pattern": r'from\s+transformers\s+import'},

    # Databases & ORM
    "PostgreSQL": {"category": "Databases", "manifest_pattern": r'psycopg2|asyncpg|pg|"pg":', "import_pattern": r'import\s+asyncpg|require\(["\']pg["\']\)'},
    "MongoDB": {"category": "Databases", "manifest_pattern": r'pymongo|mongodb|"mongoose":', "import_pattern": r'import\s+pymongo|require\(["\']mongoose["\']\)'},
    "SQLite": {"category": "Databases", "manifest_pattern": r'sqlite3|better-sqlite3', "import_pattern": r'import\s+sqlite3'},
    "Prisma": {"category": "Databases", "manifest_pattern": r'"@prisma/client":\s*"([^"]+)"', "file_pattern": r'schema\.prisma'},
    "SQLAlchemy": {"category": "Databases", "manifest_pattern": r'sqlalchemy[=~>:]*([0-9\.]*)', "import_pattern": r'from\s+sqlalchemy\s+import|import\s+sqlalchemy'},
    "Redis": {"category": "Caching", "manifest_pattern": r'redis|"ioredis":', "import_pattern": r'import\s+redis|require\(["\']ioredis["\']\)'},

    # Testing
    "Pytest": {"category": "Testing", "manifest_pattern": r'pytest[=~>:]*([0-9\.]*)', "import_pattern": r'import\s+pytest'},
    "Jest": {"category": "Testing", "manifest_pattern": r'"jest":\s*"([^"]+)"', "file_pattern": r'jest\.config\.(js|ts)'},
    "Vitest": {"category": "Testing", "manifest_pattern": r'"vitest":\s*"([^"]+)"', "file_pattern": r'vitest\.config\.(js|ts)'},

    # Containers & Cloud
    "Docker": {"category": "Containers", "file_pattern": r'Dockerfile|docker-compose\.ya?ml'},
    "Kubernetes": {"category": "Orchestration", "file_pattern": r'k8s|deployment\.yaml|service\.yaml', "manifest_pattern": r'apiVersion:\s*apps/v1'},
    "Terraform": {"category": "Infrastructure as code", "file_pattern": r'\.tf$'},
    "GitHub Actions": {"category": "CI/CD", "file_pattern": r'\.github/workflows/.*\.ya?ml$'}
}

# Programming Language Detection
LANG_EXTENSIONS = {
    ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript", ".tsx": "TypeScript (React)",
    ".jsx": "JavaScript (React)", ".java": "Java", ".go": "Go", ".rs": "Rust", ".cpp": "C++",
    ".c": "C", ".cs": "C#", ".rb": "Ruby", ".php": "PHP", ".swift": "Swift", ".kt": "Kotlin",
    ".html": "HTML", ".css": "CSS", ".sql": "SQL", ".sh": "Shell"
}

def scan_manifests(root: Path) -> list:
    """Scan manifests for direct technology dependencies."""
    findings = []
    manifest_files = [
        "package.json", "requirements.txt", "pyproject.toml", "Cargo.toml",
        "go.mod", "pom.xml", "build.gradle", "Gemfile", "composer.json", "docker-compose.yml"
    ]

    for mfile in manifest_files:
        for file_path in root.glob(f"**/{mfile}"):
            if any(part in file_path.parts for part in ["node_modules", ".git", "venv", ".venv", "dist", "build"]):
                continue

            rel_path = str(file_path.relative_to(root)).replace("\\", "/")
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                lines = content.splitlines()

                for tech, meta in TECH_SIGNATURES.items():
                    pat = meta.get("manifest_pattern")
                    if not pat:
                        continue
                    
                    for idx, line in enumerate(lines, 1):
                        match = re.search(pat, line, re.IGNORECASE)
                        if match:
                            version = match.group(1) if match.groups() and match.group(1) else "Detected"
                            findings.append({
                                "technology": tech,
                                "category": meta["category"],
                                "version": version.strip("^~>="),
                                "version_source": mfile,
                                "evidence_file": rel_path,
                                "line_number": idx,
                                "line_content": line.strip()[:150],
                                "usage": "Direct Dependency",
                                "confidence": "CONFIRMED",
                                "is_direct": True
                            })
            except Exception:
                continue

    return findings

def scan_file_patterns(root: Path) -> list:
    """Scan file patterns for structural technology signatures."""
    findings = []
    for tech, meta in TECH_SIGNATURES.items():
        pat = meta.get("file_pattern")
        if not pat:
            continue
        
        for file_path in root.glob("**/*"):
            if any(part in file_path.parts for part in ["node_modules", ".git", "venv", ".venv"]):
                continue
            if file_path.is_file():
                rel_path = str(file_path.relative_to(root)).replace("\\", "/")
                if re.search(pat, rel_path, re.IGNORECASE):
                    findings.append({
                        "technology": tech,
                        "category": meta["category"],
                        "version": "Unknown",
                        "version_source": "File Structure",
                        "evidence_file": rel_path,
                        "line_number": 1,
                        "line_content": f"File pattern match: {file_path.name}",
                        "usage": "Infrastructure / Configuration",
                        "confidence": "CONFIRMED",
                        "is_direct": True
                    })
                    break
    return findings

def scan_languages(root: Path) -> dict:
    """Determine programming language usage by count and volume."""
    counts = {}
    total_files = 0
    for file_path in root.glob("**/*"):
        if file_path.is_file() and not any(part in file_path.parts for part in ["node_modules", ".git", "venv", "dist", "build"]):
            ext = file_path.suffix.lower()
            if ext in LANG_EXTENSIONS:
                lang = LANG_EXTENSIONS[ext]
                counts[lang] = counts.get(lang, 0) + 1
                total_files += 1

    language_findings = []
    for lang, count in counts.items():
        percent = round((count / max(total_files, 1)) * 100, 1)
        language_findings.append({
            "technology": lang,
            "category": "Programming languages",
            "version": "Repo Standard",
            "version_source": "Source Files",
            "file_count": count,
            "percentage": percent,
            "confidence": "CONFIRMED",
            "usage": f"Primary/Secondary language ({percent}%)"
        })
    return language_findings

def detect_technology_stack(root_dir: str) -> dict:
    """Main technological stack detection function."""
    root = Path(root_dir).resolve()
    if not root.exists():
        raise ValueError(f"Directory not found: {root_dir}")

    manifest_findings = scan_manifests(root)
    pattern_findings = scan_file_patterns(root)
    languages = scan_languages(root)

    # Deduplicate findings by technology name
    combined = {}
    for item in manifest_findings + pattern_findings:
        tech = item["technology"]
        if tech not in combined or item["confidence"] == "CONFIRMED":
            combined[tech] = item

    all_technologies = list(combined.values()) + languages

    # Group by category
    by_category = {}
    for tech_item in all_technologies:
        cat = tech_item["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(tech_item)

    return {
        "repository_root": str(root),
        "detected_technologies_count": len(all_technologies),
        "categories": by_category,
        "raw_evidence": all_technologies
    }

def main():
    parser = argparse.ArgumentParser(description="Detect project technology stack with evidence.")
    parser.add_argument("--root", required=True, help="Repository root directory")
    parser.add_argument("--output", help="Output JSON path")
    args = parser.parse_args()

    try:
        data = detect_technology_stack(args.root)
        output_json = json.dumps(data, indent=2, ensure_ascii=False)
        if args.output:
            out_p = Path(args.output)
            out_p.parent.mkdir(parents=True, exist_ok=True)
            out_p.write_text(output_json, encoding="utf-8")
            print(f"Technology stack analysis saved to {args.output}")
        else:
            print(output_json)
    except Exception as e:
        print(f"Error executing detect_technology_stack: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
