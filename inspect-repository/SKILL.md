---
name: inspect-repository
description: Inspect local project folders, public or private GitHub repositories, uploaded project ZIP files, monorepos, and multi-service applications. Automatically detect the complete technology stack with line-level evidence, analyze architecture, map modules and data flows, document APIs and databases, create Mermaid architecture diagrams and application flowcharts, audit code quality and security without exposing secrets, evaluate production readiness, generate complete project documentation into project-documentation/, and update documentation after code changes.
---

# RepoLens Research Inspector (`inspect-repository`)

Perform deterministic, evidence-based repository analysis, technology stack identification, architecture mapping, security auditing, and comprehensive documentation generation.

---

## Quick Reference & Operating Modes

Select the operating mode based on user intent (defaults to **FULL RESEARCH AUDIT** for complete documentation, **QUICK SCAN** for brief inspection):

| Operating Mode | Primary Purpose | Key Deliverables |
|----------------|-----------------|------------------|
| **QUICK SCAN** | Rapid exploration of unfamiliar codebase | High-level architecture, stack summary, core modules, key risks |
| **FULL RESEARCH AUDIT** | Complete technical research report & docs | Full 35-section `PROJECT_RESEARCH_REPORT.md` + 16 sub-documents in `project-documentation/` |
| **DOCUMENTATION MODE** | Generate doc suite without touching code | Standardized markdown documentation suite & Mermaid diagrams |
| **UPDATE DOCUMENTATION MODE** | Sync existing docs with recent code changes | Differential section update preserving human custom notes |
| **SECURITY REVIEW MODE** | Security audit & secret risk evaluation | Secret audit, auth analysis, dependency review, OWASP evaluation |
| **ARCHITECTURE MODE** | System architecture & data flow design | Module mapping, component boundaries, API flows, ER & sequence diagrams |

---

## Imperative Execution Workflow

Execute the following 26 sequential phases when invoked:

### Phase 1: Input Resolution & Operating Mode Selection
1. Resolve the repository target location (Local path, active workspace, public/private GitHub URL, or uploaded ZIP archive).
2. For uploaded ZIP archives, extract safely into a sandboxed temporary folder, ensuring path-traversal protection (`..` prevention). Never automatically execute extracted code.
3. Determine the operating mode (Quick Scan, Full Research Audit, Documentation Mode, Update Documentation Mode, Security Review, Architecture Mode).
4. Confirm target output directory (default: `project-documentation/`).

### Phase 2: Repository Preparation & Instructions Check
5. Check for repository instructions in `AGENTS.md`, `CONTRIBUTING.md`, or `.github/copilot-instructions.md`.
6. Record Git metadata (branch name, commit SHA, clean vs dirty status) when available.

### Phase 3: Deterministic Repository Inventory
7. Run the inventory script:
   ```bash
   python scripts/inventory_repository.py --root <REPO_PATH> --output project-documentation/.inventory.json
   ```
8. Review the generated inventory JSON. Identify file categories and verify content-skipping of generated folders (`node_modules`, `.git`, `dist`, `build`, `target`, `venv`, `__pycache__`).

### Phase 4: Evidence-Based Technology Stack Detection
9. Run the technology detection script:
   ```bash
   python scripts/detect_technology_stack.py --root <REPO_PATH> --output project-documentation/.tech_stack.json
   ```
10. Categorize findings across all 28 tech categories. Ensure every technology is tagged with evidence file, line number, version source, and confidence level (`CONFIRMED`, `HIGH`, `MEDIUM`, `LOW`, `NOT FOUND`).

### Phase 5: Architecture & Module Analysis
11. Run the structure analysis script:
    ```bash
    python scripts/analyze_repository_structure.py --root <REPO_PATH> --output project-documentation/.structure.json
    ```
12. Identify application entry points, services, controllers, domain models, database schemas, background workers, and test organization. Refer to [references/architecture-analysis.md](references/architecture-analysis.md) and [references/framework-analysis.md](references/framework-analysis.md).

### Phase 6: API, Database & Security Inspection
13. Inspect REST, GraphQL, gRPC, WebSocket endpoints, and message consumers.
14. Inspect database engines, ORM entities, schemas, relationships, and migration scripts.
15. Run the deterministic secret scanner:
    ```bash
    python scripts/detect_secrets_safely.py --root <REPO_PATH> --output project-documentation/.secret_audit.json
    ```
    *Critical Rule*: Never print raw secret strings in responses, reports, or terminal output. Ensure secret redaction. Refer to [references/security-review.md](references/security-review.md).

### Phase 7: Code Evidence Collection & Diagram Generation
16. Collect line-level evidence snippets for technical assertions using:
    ```bash
    python scripts/collect_code_evidence.py --root <REPO_PATH> --file <REL_PATH> --start <START_LINE> --end <END_LINE>
    ```
17. Construct evidence-backed Mermaid diagrams for system context, authentication flows, data pipelines, and database ER models. Refer to [references/diagram-guidelines.md](references/diagram-guidelines.md).

### Phase 8: Quality Scoring & Documentation Suite Creation
18. Evaluate the project across 10 dimensions (0-100 scores) following [references/quality-scoring.md](references/quality-scoring.md).
19. Compile the complete `PROJECT_RESEARCH_REPORT.md` (containing all 35 required sections) and modular sub-documents in `project-documentation/` using templates from [assets/report-template.md](assets/report-template.md) and [references/documentation-template.md](references/documentation-template.md).
20. In **UPDATE DOCUMENTATION MODE**, preserve valid existing manual documentation, updating only outdated technical sections.

### Phase 9: Verification & Validation
21. Build an evidence ledger mapping every technical claim to file, line, and confidence rating.
22. Run the report validation script:
    ```bash
    python scripts/validate_report_evidence.py --docs project-documentation --root <REPO_PATH>
    ```
    Ensure exit code is `0`. If broken links or unredacted secrets are flagged, fix them immediately.

### Phase 10: Final Briefing & Summary Delivery
23. Calculate and report inspection coverage (total files discovered, analyzed, excluded binaries, sampled large files, net coverage percentage).
24. Provide a concise executive briefing in chat with clickable file links to generated markdown artifacts in `project-documentation/`.

---

## Detailed References & Resources

Progressive disclosure guides available in `references/`:
- **[references/inspection-workflow.md](references/inspection-workflow.md)**: 26-step deep-dive inspection procedures.
- **[references/technology-signatures.md](references/technology-signatures.md)**: 28 tech stack categories, manifests, and import signatures.
- **[references/architecture-analysis.md](references/architecture-analysis.md)**: Monolith, microservice, monorepo, and clean architecture evaluation.
- **[references/diagram-guidelines.md](references/diagram-guidelines.md)**: Mermaid diagram standards, syntax rules, and templates.
- **[references/documentation-template.md](references/documentation-template.md)**: 35-section report specification and modular doc templates.
- **[references/security-review.md](references/security-review.md)**: Secret redaction rules, OWASP evaluation, and vulnerability severities.
- **[references/quality-scoring.md](references/quality-scoring.md)**: 10-dimension production readiness evaluation formula.
- **[references/framework-analysis.md](references/framework-analysis.md)**: Node.js, Python, Go, Java, Rust ecosystem specific patterns.
