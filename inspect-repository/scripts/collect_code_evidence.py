#!/usr/bin/env python3
"""
collect_code_evidence.py - Safely extract line-level code evidence with automatic secret redaction.

Allows targeted inspection of specific line ranges in repository files while masking
sensitive strings, credentials, and API keys.
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path

# Common secret regex patterns for redaction
SECRET_PATTERNS = [
    (r'(?i)(api[_-]?key|secret|token|password|auth|pwd)\s*[:=]\s*["\']([^"\']{8,})["\']', 2),
    (r'(ghp_[A-Za-z0-9_]{36}|github_pat_[A-Za-z0-9_]{82})', 1),
    (r'(sk-[A-Za-z0-9]{32,})', 1),
    (r'(AKIA[0-9A-Z]{16})', 1),
    (r'-----BEGIN\s+(PRIVATE\s+KEY|RSA\s+PRIVATE\s+KEY)-----[\s\S]+?-----END', 0)
]

def redact_sensitive_line(line: str) -> str:
    """Redact suspected secret values from a line of code."""
    redacted = line
    for pat_info in SECRET_PATTERNS:
        pattern = pat_info[0]
        group_idx = pat_info[1]

        def replace_fn(match):
            val = match.group(group_idx if group_idx > 0 else 0)
            if "REDACTED" in val or "example" in val.lower() or "your_" in val.lower():
                return match.group(0)
            return match.group(0).replace(val, "[REDACTED_SECRET]")

        try:
            redacted = re.sub(pattern, replace_fn, redacted)
        except Exception:
            continue
    return redacted

def collect_code_evidence(root_dir: str, rel_file_path: str, start_line: int, end_line: int) -> dict:
    """Extract and redact specified line range from a repository file."""
    root = Path(root_dir).resolve()
    target_file = (root / rel_file_path).resolve()

    if not target_file.exists() or not target_file.is_file():
        raise ValueError(f"File not found: {rel_file_path}")

    # Ensure path stays inside root
    if not str(target_file).startswith(str(root)):
        raise ValueError("Target file path is outside repository root.")

    content = target_file.read_text(encoding="utf-8", errors="ignore")
    lines = content.splitlines()
    total_lines = len(lines)

    start = max(1, start_line)
    end = min(total_lines, end_line)

    extracted_snippets = []
    for idx in range(start - 1, end):
        raw_line = lines[idx]
        safe_line = redact_sensitive_line(raw_line)
        extracted_snippets.append({
            "line_number": idx + 1,
            "content": safe_line
        })

    return {
        "repository_root": str(root),
        "file_path": rel_file_path,
        "total_file_lines": total_lines,
        "requested_range": {"start": start_line, "end": end_line},
        "returned_range": {"start": start, "end": end},
        "lines": extracted_snippets
    }

def main():
    parser = argparse.ArgumentParser(description="Collect line-level code evidence with safe secret redaction.")
    parser.add_argument("--root", required=True, help="Repository root directory")
    parser.add_argument("--file", required=True, help="Relative path to target file")
    parser.add_argument("--start", type=int, default=1, help="Start line number (1-based)")
    parser.add_argument("--end", type=int, default=100, help="End line number (1-based)")
    parser.add_argument("--output", help="Output JSON file path")
    args = parser.parse_args()

    try:
        data = collect_code_evidence(args.root, args.file, args.start, args.end)
        out_json = json.dumps(data, indent=2, ensure_ascii=False)

        if args.output:
            out_p = Path(args.output)
            out_p.parent.mkdir(parents=True, exist_ok=True)
            out_p.write_text(out_json, encoding="utf-8")
            print(f"Evidence collected to {args.output}")
        else:
            print(out_json)
    except Exception as e:
        print(f"Error executing collect_code_evidence: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
