# Module Documentation

| Module | Public interface | Responsibility | Key dependencies |
|---|---|---|---|
| `inventory_repository.py` | `inventory_repository(root_dir, max_file_size_kb)`, CLI | Walk, classify, size, and exclude repository files | `os`, `pathlib`, `json`, `argparse` |
| `detect_technology_stack.py` | `detect_technology_stack(root_dir)`, CLI | Manifest/file-signature and language-extension detection | `re`, `pathlib`, `json`, `argparse` |
| `analyze_repository_structure.py` | `analyze_repository_structure(root_dir)`, CLI | Entry-point, module-path, and route-pattern discovery | `re`, `pathlib`, `json`, `argparse` |
| `collect_code_evidence.py` | `collect_code_evidence(...)`, CLI | Bounded line extraction with redaction | `re`, `pathlib`, `json`, `argparse` |
| `detect_secrets_safely.py` | `scan_secrets(root_dir)`, CLI | Secret-pattern classification and redacted JSON output | `re`, `math`, `pathlib`, `json` |
| `validate_report_evidence.py` | `validate_all_reports(docs_dir, repo_root)`, CLI | Validate Markdown links and selected secret patterns | `re`, `pathlib`, `json` |

The modules are operationally independent. Coordination exists only in the prose workflow in [SKILL.md](SKILL.md#L27); there is no Python orchestrator or shared library. This keeps invocation simple but duplicates exclusion/redaction/path logic and allows behavior to drift.

Key boundary issues:

- The technology signature declarations include `import_pattern`, but the detector never runs an import scan; compare [signature declarations](scripts/detect_technology_stack.py#L18) with [detector orchestration](scripts/detect_technology_stack.py#L171).
- The structure scanner applies route regexes to every supported source file, including tests, so fixture strings can become reported endpoints; see [analyze_repository_structure.py](scripts/analyze_repository_structure.py#L88).
- Evidence containment uses string-prefix comparison instead of a path-relative containment operation; see [collect_code_evidence.py](scripts/collect_code_evidence.py#L44).
- The Markdown validator treats unsupported confirmed claims as advisory and excludes them from validity; see [validate_report_evidence.py](scripts/validate_report_evidence.py#L65).
