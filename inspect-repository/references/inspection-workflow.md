# Repository Inspection Workflow & Operating Modes

This guide defines the 26-step execution workflow for inspecting local folders, GitHub repositories, monorepos, and uploaded ZIP archives using the **RepoLens Research Inspector** (`inspect-repository`).

---

## Operating Modes

When invoked, select or confirm the appropriate operating mode based on user intent:

| Mode | Trigger / Best For | Deliverables |
|------|-------------------|--------------|
| **QUICK SCAN** | Overview requests, quick code exploration | Project overview, high-level stack, core modules, initial architecture summary, top risks |
| **FULL RESEARCH AUDIT** | Standard full audit, complete documentation | Complete 35-section `PROJECT_RESEARCH_REPORT.md` + full `project-documentation/` sub-documents |
| **DOCUMENTATION MODE** | Documentation generation only | Non-destructive `project-documentation/` suite without modifying application code |
| **UPDATE DOCUMENTATION MODE** | Re-inspection after recent code changes | Differential report updating stale markdown sections while preserving human custom notes |
| **SECURITY REVIEW MODE** | Security audit, vulnerability review | Secret scanning, dependency CVE review, auth analysis, OWASP Top 10 evaluation |
| **ARCHITECTURE MODE** | Design analysis, refactoring | System component maps, Mermaid diagrams, API flows, data pipeline & ER diagrams |

---

## 26-Step Comprehensive Inspection Process

1. **Location Resolution**: Determine input source (Local directory, GitHub URL, uploaded ZIP archive, or active workspace).
2. **Safety & Permission Check**: Prevent automatic code execution. Enforce path traversal bounds on ZIP extractions.
3. **Mode & Scope Selection**: Default to **FULL RESEARCH AUDIT** for full documentation requests, **QUICK SCAN** for simple queries.
4. **Instruction Inspection**: Check for repository agent instructions (e.g. `AGENTS.md`, `CONTRIBUTING.md`, `.github/copilot-instructions.md`).
5. **Git Metadata Capture**: Record branch name, commit SHA, tag, and working tree cleanliness when available.
6. **Deterministic Inventory Execution**: Run `python scripts/inventory_repository.py --root <path>` to build file category breakdown.
7. **Exclusion Pruning**: Identify generated folders (`node_modules`, `dist`, `build`, `target`, `venv`, `__pycache__`) for content-skipping.
8. **Technology Stack Detection**: Run `python scripts/detect_technology_stack.py --root <path>` across manifests, lock files, and imports.
9. **Entry Point Identification**: Locate application entry points (`main.py`, `app.ts`, `server.js`, `index.go`, `Application.java`).
10. **Module Architecture Mapping**: Run `python scripts/analyze_repository_structure.py --root <path>` to map services, routes, models, and controllers.
11. **API & Endpoint Inspection**: Document REST, GraphQL, gRPC, WebSockets, webhooks, and message queues with evidence file/line references.
12. **Database & Schema Analysis**: Inspect ORM models, migration scripts, SQL schemas, foreign key relationships, and query patterns.
13. **Auth & Access Control Inspection**: Trace authentication tokens, session management, OAuth flows, and authorization middleware.
14. **Testing Infrastructure Analysis**: Inventory unit, integration, and E2E tests; calculate file coverage ratio.
15. **Infrastructure & Containers**: Scan `Dockerfile`, `docker-compose.yml`, Terraform, Helm, and Kubernetes manifests.
16. **CI/CD Pipeline Analysis**: Analyze GitHub Actions workflows, GitLab CI, or Jenkins pipelines.
17. **Deterministic Secret Audit**: Run `python scripts/detect_secrets_safely.py --root <path>` to identify and redact sensitive credentials.
18. **Targeted Code Evidence Collection**: Use `python scripts/collect_code_evidence.py` to extract line ranges for key technical claims.
19. **Architecture Diagram Generation**: Construct editable Mermaid diagrams (System Context, Service, ER, Sequence, Auth).
20. **Quality & Production-Readiness Scoring**: Calculate 0-100 scores across 10 dimensions with technical rationale.
21. **Evidence Ledger Compilation**: Map every technical assertion to file path, line number, and confidence level (`CONFIRMED`, `HIGH`, `MEDIUM`, `LOW`, `NOT FOUND`).
22. **Documentation Suite Generation**: Output structured Markdown files into `project-documentation/`.
23. **Cross-Claim Verification**: Re-verify code vs config vs existing documentation.
24. **Report Validation Run**: Run `python scripts/validate_report_evidence.py --docs project-documentation --root <path>` to confirm zero broken links or raw secrets.
25. **Coverage Reporting**: Summarize files discovered, files analyzed, skipped binaries, and overall analysis percentage.
26. **Delivery & Briefing**: Present concise summary pointing to generated artifacts.
