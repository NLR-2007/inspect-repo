# Evidence Ledger

Confidence meanings follow [technology-signatures.md](references/technology-signatures.md#L7). `Validated` means the referenced path and line were manually cross-checked during this audit; it does not mean the behavior is defect-free.

| ID | Technical claim | Evidence path and location | Confidence | Status |
|---|---|---|---|---|
| E-001 | The project is an `inspect-repository` agent skill. | [SKILL.md](SKILL.md#L1) | CONFIRMED | Validated |
| E-002 | Full audit mode promises a master report and modular docs. | [SKILL.md](SKILL.md#L12) | CONFIRMED | Validated |
| E-003 | The workflow invokes four deterministic scans before report validation. | [SKILL.md](SKILL.md#L41) | CONFIRMED | Validated |
| E-004 | Baseline support is documented as Python 3.8+. | [README.md](README.md#L4) | CONFIRMED | Validated |
| E-005 | Six Python source scripts implement the toolset. | [README.md](README.md#L51), [.inventory.json](project-documentation/.inventory.json) | CONFIRMED | Validated |
| E-006 | Inventory prunes common generated directories. | [inventory_repository.py](scripts/inventory_repository.py#L15) | CONFIRMED | Validated |
| E-007 | Inventory classifies manifests, locks, containers, CI, source, config, DB, docs, infra, and assets. | [inventory_repository.py](scripts/inventory_repository.py#L23) | CONFIRMED | Validated |
| E-008 | Baseline inventory analyzed 22 of 22 files with no binary/large-file exclusion. | [.inventory.json](project-documentation/.inventory.json) | CONFIRMED | Validated |
| E-009 | `.git` is the only ignored directory detected in the baseline. | [.inventory.json](project-documentation/.inventory.json) | CONFIRMED | Validated |
| E-010 | Large-file “sampling” is only a counter in current inventory logic. | [inventory_repository.py](scripts/inventory_repository.py#L178) | HIGH | Validated |
| E-011 | The technology signature catalog declares frontend, backend, AI/ML, DB, testing, container, orchestration, IaC, and CI signatures. | [detect_technology_stack.py](scripts/detect_technology_stack.py#L18) | CONFIRMED | Validated |
| E-012 | Import patterns are declared but not executed by detector orchestration. | [detect_technology_stack.py](scripts/detect_technology_stack.py#L171) | CONFIRMED | Validated |
| E-013 | Language detection is extension/count based and omits evidence line/path. | [detect_technology_stack.py](scripts/detect_technology_stack.py#L144) | CONFIRMED | Validated |
| E-014 | The generated stack result contains only Python and no pinned version. | [.tech_stack.json](project-documentation/.tech_stack.json) | CONFIRMED | Validated |
| E-015 | Entry-point detection is filename-pattern based. | [analyze_repository_structure.py](scripts/analyze_repository_structure.py#L16) | CONFIRMED | Validated |
| E-016 | Module detection is directory-name-pattern based. | [analyze_repository_structure.py](scripts/analyze_repository_structure.py#L27) | CONFIRMED | Validated |
| E-017 | Route detection scans Python/JS/TS/Go/Java lines with REST patterns. | [analyze_repository_structure.py](scripts/analyze_repository_structure.py#L40) | CONFIRMED | Validated |
| E-018 | The reported `/api/users` route is a fixture string, not a live endpoint. | [test file](test_inspect_repository_scripts.py#L77), [.structure.json](project-documentation/.structure.json) | CONFIRMED | Validated |
| E-019 | No application entry point was detected. | [.structure.json](project-documentation/.structure.json) | CONFIRMED | Validated |
| E-020 | Evidence extraction redacts selected secret patterns. | [collect_code_evidence.py](scripts/collect_code_evidence.py#L16) | CONFIRMED | Validated |
| E-021 | Evidence root containment uses a string-prefix comparison. | [collect_code_evidence.py](scripts/collect_code_evidence.py#L44) | CONFIRMED | Validated |
| E-022 | Secret scanning recognizes token, key, connection URL, and generic assignment patterns. | [detect_secrets_safely.py](scripts/detect_secrets_safely.py#L17) | CONFIRMED | Validated |
| E-023 | Secret classification uses placeholders, environment syntax, test paths, and entropy. | [detect_secrets_safely.py](scripts/detect_secrets_safely.py#L66) | CONFIRMED | Validated |
| E-024 | Secret output redacts only `match.group(1)` for patterns with groups. | [detect_secrets_safely.py](scripts/detect_secrets_safely.py#L114) | CONFIRMED | Validated |
| E-025 | The baseline scanner classified no finding as a suspected real credential. | [.secret_audit.json](project-documentation/.secret_audit.json) | CONFIRMED | Validated |
| E-026 | Report validation checks Markdown links and selected secret patterns. | [validate_report_evidence.py](scripts/validate_report_evidence.py#L16) | CONFIRMED | Validated |
| E-027 | Unsupported confirmed claims do not affect `is_valid`. | [validate_report_evidence.py](scripts/validate_report_evidence.py#L65) | CONFIRMED | Validated |
| E-028 | Validator traversal includes Markdown only. | [validate_report_evidence.py](scripts/validate_report_evidence.py#L87) | CONFIRMED | Validated |
| E-029 | The test runner invokes scripts as subprocess argument lists. | [test file](test_inspect_repository_scripts.py#L25) | CONFIRMED | Validated |
| E-030 | Tests cover all six scripts using temporary repositories. | [test file](test_inspect_repository_scripts.py#L32) | CONFIRMED | Validated |
| E-031 | The README documents one command for running tests. | [README.md](README.md#L99) | CONFIRMED | Validated |
| E-032 | README references an absent `quick_validate.py`. | [README.md](README.md#L107), [.inventory.json](project-documentation/.inventory.json) | CONFIRMED | Validated |
| E-033 | Agent metadata defines display name, description, and default prompt. | [agents/openai.yaml](agents/openai.yaml#L1) | CONFIRMED | Validated |
| E-034 | The repository is GPL-3.0 licensed. | [LICENSE](LICENSE), [README.md](README.md#L115) | CONFIRMED | Validated |
| E-035 | No dependency manifest, lock, container, infrastructure, DB, or CI file exists. | [.inventory.json](project-documentation/.inventory.json) | CONFIRMED | Validated |
