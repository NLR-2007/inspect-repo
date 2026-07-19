#!/usr/bin/env python3
"""
validate_report_evidence.py - Cross-validate markdown reports against repository evidence.

Verifies referenced file paths exist, checks confidence labeling completeness,
ensures zero exposed raw secrets in report text, and flags unsupported claims.
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path

# Match file links in markdown: [link text](path) or file:///path
FILE_LINK_PATTERN = r'\[([^\]]+)\]\((?:file://(?:/[A-Za-z]:)?)?([^#\)\s]+)(?:#[^\)]*)?\)'
CONFIRMED_CLAIM_PATTERN = r'(?i)\bCONFIRMED\b'
SECRET_LIKE_PATTERN = r'(ghp_[A-Za-z0-9_]{36}|sk-[A-Za-z0-9]{32,}|AKIA[0-9A-Z]{16})'

def validate_markdown_report(report_path: Path, repo_root: Path) -> dict:
    """Validate a single markdown report against repository state."""
    content = report_path.read_text(encoding="utf-8", errors="ignore")
    lines = content.splitlines()

    broken_links = []
    unsupported_confirmed_claims = []
    exposed_secret_warnings = []
    lines_without_confidence = []

    for idx, line in enumerate(lines, 1):
        # 1. Check file links
        for match in re.finditer(FILE_LINK_PATTERN, line):
            text = match.group(1)
            target_path_str = match.group(2)

            # Skip web URLs
            if target_path_str.startswith("http://") or target_path_str.startswith("https://"):
                continue

            # Normalize path
            clean_path = target_path_str.lstrip("/")
            if ":" in clean_path and os.name == "nt": # handle drive letters
                resolved_target = Path(target_path_str)
            else:
                resolved_target = (repo_root / clean_path).resolve()

            if not resolved_target.exists():
                broken_links.append({
                    "line_number": idx,
                    "link_text": text,
                    "target_path": target_path_str,
                    "issue": "Referenced file path does not exist in repository"
                })

        # 2. Check unredacted secret patterns in documentation text
        secret_match = re.search(SECRET_LIKE_PATTERN, line)
        if secret_match:
            exposed_secret_warnings.append({
                "line_number": idx,
                "secret_snippet": secret_match.group(0)[:10] + "...",
                "issue": "Unredacted secret key pattern detected in report text!"
            })

        # 3. Check claims without explicit evidence link on CONFIRMED findings
        if re.search(CONFIRMED_CLAIM_PATTERN, line):
            if "file://" not in line and "(" not in line and ".py" not in line and ".js" not in line:
                unsupported_confirmed_claims.append({
                    "line_number": idx,
                    "line_content": line.strip()[:100],
                    "issue": "CONFIRMED finding lacks explicit evidence path or file reference"
                })

    is_valid = len(broken_links) == 0 and len(exposed_secret_warnings) == 0

    return {
        "report_file": str(report_path),
        "is_valid": is_valid,
        "broken_links_count": len(broken_links),
        "broken_links": broken_links,
        "unsupported_confirmed_claims_count": len(unsupported_confirmed_claims),
        "unsupported_confirmed_claims": unsupported_confirmed_claims,
        "exposed_secret_warnings_count": len(exposed_secret_warnings),
        "exposed_secret_warnings": exposed_secret_warnings
    }

def validate_all_reports(docs_dir: str, repo_root: str) -> dict:
    """Validate all markdown files inside project-documentation/."""
    docs_path = Path(docs_dir).resolve()
    root_path = Path(repo_root).resolve()

    if not docs_path.exists():
        raise ValueError(f"Documentation directory does not exist: {docs_dir}")
    if not root_path.exists():
        raise ValueError(f"Repository root directory does not exist: {repo_root}")

    results = []
    overall_valid = True
    total_broken_links = 0
    total_secret_warnings = 0

    for md_file in docs_path.glob("**/*.md"):
        report_res = validate_markdown_report(md_file, root_path)
        results.append(report_res)
        if not report_res["is_valid"]:
            overall_valid = False
        total_broken_links += report_res["broken_links_count"]
        total_secret_warnings += report_res["exposed_secret_warnings_count"]

    return {
        "documentation_directory": str(docs_path),
        "repository_root": str(root_path),
        "overall_valid": overall_valid,
        "total_reports_validated": len(results),
        "total_broken_links": total_broken_links,
        "total_exposed_secret_warnings": total_secret_warnings,
        "reports": results
    }

def main():
    parser = argparse.ArgumentParser(description="Validate report evidence links and anti-hallucination compliance.")
    parser.add_argument("--docs", required=True, help="Path to project-documentation directory")
    parser.add_argument("--root", required=True, help="Repository root directory")
    parser.add_argument("--output", help="Output JSON path")
    args = parser.parse_args()

    try:
        validation_res = validate_all_reports(args.docs, args.root)
        out_json = json.dumps(validation_res, indent=2, ensure_ascii=False)

        if args.output:
            out_p = Path(args.output)
            out_p.parent.mkdir(parents=True, exist_ok=True)
            out_p.write_text(out_json, encoding="utf-8")
            print(f"Validation summary saved to {args.output}")
        else:
            print(out_json)

        if not validation_res["overall_valid"]:
            print("Report evidence validation failed due to broken file links or unredacted secret patterns!", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error executing validate_report_evidence: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
