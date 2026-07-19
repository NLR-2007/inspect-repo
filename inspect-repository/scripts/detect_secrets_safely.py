#!/usr/bin/env python3
"""
detect_secrets_safely.py - Scan for potential secret exposures without logging raw secrets.

Identifies API keys, private keys, connection strings, and tokens, categorizing them into
placeholder, environment reference, test credential, or suspected real credential.
"""

import os
import re
import sys
import json
import math
import argparse
from pathlib import Path

# Pattern catalog with severity classification
SECRET_PATTERNS = [
    {
        "type": "GitHub Personal Access Token",
        "pattern": r'(ghp_[A-Za-z0-9_]{36}|github_pat_[A-Za-z0-9_]{82})',
        "severity": "CRITICAL"
    },
    {
        "type": "OpenAI API Key",
        "pattern": r'(sk-[A-Za-z0-9_-]{32,})',
        "severity": "CRITICAL"
    },
    {
        "type": "AWS Access Key",
        "pattern": r'(AKIA[0-9A-Z]{16})',
        "severity": "HIGH"
    },
    {
        "type": "Generic Private Key",
        "pattern": r'-----BEGIN\s+(PRIVATE\s+KEY|RSA\s+PRIVATE\s+KEY)-----',
        "severity": "CRITICAL"
    },
    {
        "type": "Database Connection String",
        "pattern": r'(postgres|mysql|mongodb|redis)://[^:]+:([^@]+)@',
        "severity": "HIGH"
    },
    {
        "type": "Generic Secret Keyword Assignment",
        "pattern": r'(?i)(api[_-]?key|secret[_-]?key|auth[_-]?token|password|passwd)\s*[:=]\s*["\']([^"\']{8,})["\']',
        "severity": "MEDIUM"
    }
]

EXPLICIT_PLACEHOLDERS = [
    "example", "your_", "change_me", "placeholder", "<key>", "<secret>",
    "todo", "sample", "test_key", "dummy", "fake", "insert_"
]

def calculate_shannon_entropy(data: str) -> float:
    """Calculate Shannon entropy to measure randomness."""
    if not data:
        return 0.0
    entropy = 0.0
    for x in set(data):
        p_x = float(data.count(x)) / len(data)
        entropy -= p_x * math.log(p_x, 2)
    return round(entropy, 2)

def classify_secret_kind(match_str: str, file_path: str, line_content: str) -> str:
    """Classify credential into placeholder, env ref, test credential, or suspected real."""
    lower_val = match_str.lower()
    lower_path = file_path.lower()
    lower_line = line_content.lower()

    if any(ph in lower_val or ph in lower_line for ph in EXPLICIT_PLACEHOLDERS):
        return "placeholder"

    if "process.env" in lower_line or "os.getenv" in lower_line or "env[" in lower_line:
        return "environment_variable"

    if "/test/" in lower_path or "/tests/" in lower_path or "test_" in lower_path or "mock" in lower_path:
        return "test_credential"

    entropy = calculate_shannon_entropy(match_str)
    if entropy > 3.2 and len(match_str) >= 16:
        return "suspected_real_credential"

    return "placeholder"

def redact_secret_string(val: str) -> str:
    """Redact secret string safely leaving only prefix/suffix for identification."""
    if len(val) <= 6:
        return "[REDACTED]"
    return val[:3] + "..." + val[-3:]

def scan_secrets(root_dir: str) -> dict:
    """Perform deterministic secret scan over repository files."""
    root = Path(root_dir).resolve()
    findings = []
    total_files_scanned = 0

    for file_path in root.glob("**/*"):
        if any(part in file_path.parts for part in ["node_modules", ".git", "venv", ".venv", "dist", "build"]):
            continue
        if file_path.is_file():
            # Skip large binary files
            if file_path.stat().st_size > 2 * 1024 * 1024:
                continue

            rel_p = str(file_path.relative_to(root)).replace("\\", "/")
            total_files_scanned += 1

            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                lines = content.splitlines()

                for idx, line in enumerate(lines, 1):
                    for pat in SECRET_PATTERNS:
                        matches = re.finditer(pat["pattern"], line)
                        for match in matches:
                            raw_val = match.group(1) if match.groups() else match.group(0)
                            kind = classify_secret_kind(raw_val, rel_p, line)
                            redacted = redact_secret_string(raw_val)

                            findings.append({
                                "finding_id": f"SEC-{len(findings)+1:03d}",
                                "secret_type": pat["type"],
                                "classification": kind,
                                "severity": pat["severity"] if kind == "suspected_real_credential" else "LOW",
                                "file_path": rel_p,
                                "line_number": idx,
                                "redacted_snippet": line.replace(raw_val, redacted).strip()[:150],
                                "redacted_value": redacted,
                                "entropy": calculate_shannon_entropy(raw_val),
                                "remediation": "Move secret value to an external secret manager or .env file."
                            })
            except Exception:
                continue

    suspected_real_count = sum(1 for f in findings if f["classification"] == "suspected_real_credential")

    return {
        "repository_root": str(root),
        "total_files_scanned": total_files_scanned,
        "total_findings": len(findings),
        "suspected_real_credentials_count": suspected_real_count,
        "findings": findings
    }

def main():
    parser = argparse.ArgumentParser(description="Scan for secrets safely with automatic redaction.")
    parser.add_argument("--root", required=True, help="Repository root directory")
    parser.add_argument("--output", help="Output JSON path")
    args = parser.parse_args()

    try:
        data = scan_secrets(args.root)
        out_json = json.dumps(data, indent=2, ensure_ascii=False)

        if args.output:
            out_p = Path(args.output)
            out_p.parent.mkdir(parents=True, exist_ok=True)
            out_p.write_text(out_json, encoding="utf-8")
            print(f"Secret audit results saved to {args.output}")
        else:
            print(out_json)

        if data["suspected_real_credentials_count"] > 0:
            sys.exit(2) # Non-zero exit when suspected real secrets found
    except Exception as e:
        print(f"Error executing detect_secrets_safely: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
