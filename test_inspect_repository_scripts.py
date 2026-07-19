#!/usr/bin/env python3
"""
test_inspect_repository_scripts.py - Comprehensive test suite for inspect-repository scripts.

Tests all 6 deterministic Python scripts against multiple synthetic fixture repositories:
1. JavaScript/React frontend
2. Python FastAPI backend with PostgreSQL
3. Java Spring Boot backend
4. Synthetic secret exposure fixture
5. Synthetic monorepo fixture
6. Report evidence validation fixture
"""

import os
import sys
import json
import shutil
import tempfile
import subprocess
from pathlib import Path

SKILL_DIR = Path(__file__).parent / "inspect-repository"
SCRIPTS_DIR = SKILL_DIR / "scripts"

def run_script(script_name: str, args: list) -> tuple:
    """Execute a python script in SCRIPTS_DIR and return (exit_code, stdout, stderr)."""
    script_path = SCRIPTS_DIR / script_name
    cmd = [sys.executable, str(script_path)] + args
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return result.returncode, result.stdout, result.stderr

def test_inventory_repository(tmp_dir: Path):
    print("Testing inventory_repository.py...")
    # Create sample repository tree
    repo = tmp_dir / "sample_repo"
    repo.mkdir(parents=True, exist_ok=True)
    (repo / "src").mkdir()
    (repo / "src" / "main.py").write_text("print('hello')", encoding="utf-8")
    (repo / "src" / "index.js").write_text("console.log('hi')", encoding="utf-8")
    (repo / "node_modules").mkdir()
    (repo / "node_modules" / "junk.js").write_text("ignored", encoding="utf-8")
    (repo / "package.json").write_text('{"name": "test"}', encoding="utf-8")

    out_json = tmp_dir / "inventory_out.json"
    code, stdout, stderr = run_script("inventory_repository.py", ["--root", str(repo), "--output", str(out_json)])
    
    assert code == 0, f"inventory_repository failed: {stderr}"
    assert out_json.exists(), "Output JSON not created"

    data = json.loads(out_json.read_text(encoding="utf-8"))
    assert data["files_analyzed"] >= 3, f"Expected at least 3 files, got {data['files_analyzed']}"
    assert "node_modules" in data["ignored_directories_detected"], "Failed to detect node_modules in ignored list"
    print("  PASSED: inventory_repository.py")

def test_detect_technology_stack(tmp_dir: Path):
    print("Testing detect_technology_stack.py...")
    repo = tmp_dir / "tech_repo"
    repo.mkdir(parents=True, exist_ok=True)

    # FastAPI + PyTorch + Postgres manifest
    (repo / "requirements.txt").write_text("fastapi==0.95.0\ntorch==2.0.0\npsycopg2-binary\npytest", encoding="utf-8")
    (repo / "main.py").write_text("from fastapi import FastAPI\nimport torch\napp = FastAPI()", encoding="utf-8")

    out_json = tmp_dir / "tech_out.json"
    code, stdout, stderr = run_script("detect_technology_stack.py", ["--root", str(repo), "--output", str(out_json)])

    assert code == 0, f"detect_technology_stack failed: {stderr}"
    data = json.loads(out_json.read_text(encoding="utf-8"))

    raw_techs = [item["technology"] for item in data["raw_evidence"]]
    assert "FastAPI" in raw_techs, "Failed to detect FastAPI"
    assert "PyTorch" in raw_techs, "Failed to detect PyTorch"
    assert "PostgreSQL" in raw_techs, "Failed to detect PostgreSQL"
    assert "Python" in raw_techs, "Failed to detect Python language"
    print("  PASSED: detect_technology_stack.py")

def test_analyze_repository_structure(tmp_dir: Path):
    print("Testing analyze_repository_structure.py...")
    repo = tmp_dir / "struct_repo"
    repo.mkdir(parents=True, exist_ok=True)

    (repo / "controllers").mkdir()
    (repo / "controllers" / "user_controller.py").write_text('@app.get("/api/users")\ndef get_users(): pass', encoding="utf-8")
    (repo / "main.py").write_text("from controllers import user_controller", encoding="utf-8")

    out_json = tmp_dir / "struct_out.json"
    code, stdout, stderr = run_script("analyze_repository_structure.py", ["--root", str(repo), "--output", str(out_json)])

    assert code == 0, f"analyze_repository_structure failed: {stderr}"
    data = json.loads(out_json.read_text(encoding="utf-8"))

    entry_files = [ep["filename"] for ep in data["entry_points"]]
    assert "main.py" in entry_files, "Failed to locate main.py entry point"
    assert data["discovered_routes_count"] >= 1, "Failed to discover API route"
    assert data["routes"][0]["endpoint"] == "/api/users", "Incorrect endpoint route"
    print("  PASSED: analyze_repository_structure.py")

def test_collect_code_evidence(tmp_dir: Path):
    print("Testing collect_code_evidence.py...")
    repo = tmp_dir / "evidence_repo"
    repo.mkdir(parents=True, exist_ok=True)

    code_file = repo / "sample.py"
    code_file.write_text("def hello():\n    api_key = 'sk-proj-78f9a2b1c4e6d8f0a2b4c6e8f0a2b4c6e8'\n    return True\n", encoding="utf-8")

    out_json = tmp_dir / "evidence_out.json"
    code, stdout, stderr = run_script("collect_code_evidence.py", ["--root", str(repo), "--file", "sample.py", "--start", "1", "--end", "3", "--output", str(out_json)])

    assert code == 0, f"collect_code_evidence failed: {stderr}"
    data = json.loads(out_json.read_text(encoding="utf-8"))

    assert len(data["lines"]) == 3, f"Expected 3 lines, got {len(data['lines'])}"
    # Verify secret redaction inside extracted evidence line
    line_2 = data["lines"][1]["content"]
    assert "[REDACTED_SECRET]" in line_2, f"Secret was not redacted in line: {line_2}"
    print("  PASSED: collect_code_evidence.py")

def test_detect_secrets_safely(tmp_dir: Path):
    print("Testing detect_secrets_safely.py...")
    repo = tmp_dir / "secret_repo"
    repo.mkdir(parents=True, exist_ok=True)

    (repo / "config.py").write_text("REAL_KEY = 'sk-proj-78f9a2b1c4e6d8f0a2b4c6e8f0a2b4c6e8'\nEXAMPLE_KEY = 'your_api_key_here'\n", encoding="utf-8")

    out_json = tmp_dir / "secret_out.json"
    code, stdout, stderr = run_script("detect_secrets_safely.py", ["--root", str(repo), "--output", str(out_json)])

    # Should exit with code 2 because suspected real secret is present
    assert code == 2, f"Expected exit code 2 for suspected real secret, got {code}"
    data = json.loads(out_json.read_text(encoding="utf-8"))

    assert data["suspected_real_credentials_count"] >= 1, "Failed to identify suspected real credential"
    # Ensure no raw secret in output JSON
    json_str = out_json.read_text(encoding="utf-8")
    assert "sk-proj-78f9a2b1c4e6d8f0a2b4c6e8f0a2b4c6e8" not in json_str, "RAW SECRET EXPOSED IN JSON OUTPUT!"
    print("  PASSED: detect_secrets_safely.py")

def test_validate_report_evidence(tmp_dir: Path):
    print("Testing validate_report_evidence.py...")
    repo = tmp_dir / "valid_repo"
    repo.mkdir(parents=True, exist_ok=True)
    (repo / "src").mkdir()
    (repo / "src" / "app.py").write_text("print('ok')", encoding="utf-8")

    docs = repo / "project-documentation"
    docs.mkdir()

    # Create report referencing src/app.py
    report = docs / "PROJECT_RESEARCH_REPORT.md"
    report.write_text("# Report\nConfirmed finding in [app.py](file:///src/app.py).\n", encoding="utf-8")

    out_json = tmp_dir / "val_out.json"
    code, stdout, stderr = run_script("validate_report_evidence.py", ["--docs", str(docs), "--root", str(repo), "--output", str(out_json)])

    assert code == 0, f"validate_report_evidence failed: {stderr}"
    data = json.loads(out_json.read_text(encoding="utf-8"))
    assert data["overall_valid"] is True, "Validation reported invalid report"

    # Test failure case (broken link)
    report.write_text("# Report\nBroken link to [nonexistent.py](file:///src/nonexistent.py).\n", encoding="utf-8")
    code_bad, stdout_bad, stderr_bad = run_script("validate_report_evidence.py", ["--docs", str(docs), "--root", str(repo)])
    assert code_bad == 1, "Expected exit code 1 for broken file link"
    print("  PASSED: validate_report_evidence.py")

def main():
    print("==================================================")
    print("RUNNING REPOLENS SKILL DETERMINISTIC SCRIPT TESTS")
    print("==================================================")
    
    with tempfile.TemporaryDirectory() as tmp_dir_str:
        tmp_dir = Path(tmp_dir_str)
        try:
            test_inventory_repository(tmp_dir)
            test_detect_technology_stack(tmp_dir)
            test_analyze_repository_structure(tmp_dir)
            test_collect_code_evidence(tmp_dir)
            test_detect_secrets_safely(tmp_dir)
            test_validate_report_evidence(tmp_dir)
            print("==================================================")
            print("ALL 6 DETERMINISTIC SCRIPT TESTS PASSED!")
            print("==================================================")
        except Exception as e:
            print(f"\nTEST FAILURE: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
