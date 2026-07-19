# 🔍 RepoLens Research Inspector (`inspect-repository`)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Skill Status](https://img.shields.io/badge/Skill%20Status-Validated-success.svg)](#-skill-validation)
[![Architecture](https://img.shields.io/badge/Architecture-Agentic%20Skill-orange.svg)](#-architecture)

> **RepoLens Research Inspector** is an expert, production-grade agentic skill designed for deterministic, evidence-backed codebase analysis, technology stack identification, security auditing, architecture mapping, and complete project documentation generation.

---

## 🌟 Key Features

- 🔎 **Deterministic File Inventory**: Classifies files across 22 categories, intelligently ignoring generated folders (`node_modules`, `.git`, `dist`, `target`, `venv`, `__pycache__`) while tracking total file counts and size metrics.
- ⚡ **28-Category Technology Stack Detection**: Scans manifests (`package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`, `pom.xml`), lock files, Dockerfiles, and source imports with line-level evidence and confidence levels (`CONFIRMED`, `HIGH`, `MEDIUM`, `LOW`, `NOT FOUND`).
- 🔐 **Safe Secret Audit & Redaction**: Scans for API keys, private keys, database connection strings, and tokens without ever exposing raw secrets in terminal output, logs, or documentation.
- 📊 **Editable Mermaid Architecture Diagrams**: Automatically generates evidence-backed Mermaid diagrams for System Architecture, Request/Auth Flow Sequences, and Database ER Models.
- 🎯 **10-Dimension Senior Quality Scoring**: Scores projects from 0 to 100 across 10 evaluation dimensions with technical rationale.
- 📄 **Complete 35-Section Documentation Suite**: Outputs `PROJECT_RESEARCH_REPORT.md` and 16 modular sub-documents into `project-documentation/`.
- 🔗 **Anti-Hallucination & Link Validation**: Built-in evidence ledger cross-validates every claim against existing repository files before delivery.

---

## 📁 Repository & Skill Structure

```text
inspect-repo/
├── README.md                      # GitHub Repository Presentation
├── LICENSE                        # GNU General Public License v3.0
├── test_inspect_repository_scripts.py # Deterministic Script Test Suite
└── inspect-repository/            # Production Agentic Skill Directory
    ├── SKILL.md                   # Skill Core & 26-Step Execution Workflow
    ├── prompt.txt                 # Master Default User Prompt
    ├── LICENSE                    # Skill GPL-3.0 License
    ├── agents/
    │   └── openai.yaml            # Agent Metadata & Display Configuration
    ├── scripts/
    │   ├── inventory_repository.py         # File Categorization & Ignore Scanner
    │   ├── detect_technology_stack.py      # Manifest & Import Evidence Scanner
    │   ├── analyze_repository_structure.py # Entry Points & Route Mapper
    │   ├── collect_code_evidence.py        # Safe Line Evidence Extractor
    │   ├── detect_secrets_safely.py        # Safe Secret Auditor & Redactor
    │   └── validate_report_evidence.py     # Markdown Evidence & Link Validator
    ├── references/
    │   ├── inspection-workflow.md          # 26-Step Inspection Operating Procedure
    │   ├── technology-signatures.md        # 28 Tech Categories & Signature Catalog
    │   ├── architecture-analysis.md        # Architectural Boundary Checklist
    │   ├── diagram-guidelines.md           # Mermaid Syntax & Diagram Templates
    │   ├── documentation-template.md       # 35-Section Document Suite Spec
    │   ├── security-review.md              # OWASP Evaluation & Vulnerability Matrix
    │   ├── quality-scoring.md              # 0-100 Production Readiness Methodology
    │   └── framework-analysis.md           # Ecosystem Framework Inspection Patterns
    └── assets/
        ├── prompt.txt                      # Master Default Prompt Asset
        └── report-template.md              # Markdown Report Template
```

---

## ⚡ Quick Start

### 1. Installation

Copy the `inspect-repository` directory into your personal agent skills path:

```bash
# Personal Skills Directory
cp -r inspect-repository ~/.gemini/skills/inspect-repository

# Antigravity Skills Directory
cp -r inspect-repository ~/.gemini/antigravity/skills/inspect-repository
```

### 2. Master Trigger Prompt

Use the included master prompt from [`prompt.txt`](inspect-repository/prompt.txt) to perform an exhaustive audit on any codebase:

```text
Perform an exhaustive, senior-level Full Research Audit of this repository using inspect-repository (RepoLens Research Inspector).

Your objective is to thoroughly inspect every file, directory, module, framework, database schema, API route, infrastructure configuration, and CI/CD pipeline in this project folder, and generate a production-grade documentation suite inside project-documentation/.
```

---

## 🛠️ Operating Modes

| Mode | Purpose | Key Deliverables |
|------|---------|------------------|
| **QUICK SCAN** | Rapid exploration of unfamiliar codebases | High-level architecture, stack summary, core modules, key risks |
| **FULL RESEARCH AUDIT** | Complete technical research report & docs | Full 35-section `PROJECT_RESEARCH_REPORT.md` + 16 sub-documents in `project-documentation/` |
| **DOCUMENTATION MODE** | Generate doc suite without touching code | Standardized markdown documentation suite & Mermaid diagrams |
| **UPDATE DOCUMENTATION MODE** | Sync existing docs with recent code changes | Differential section update preserving human custom notes |
| **SECURITY REVIEW MODE** | Security audit & secret risk evaluation | Secret audit, auth analysis, dependency review, OWASP evaluation |
| **ARCHITECTURE MODE** | System architecture & data flow design | Module mapping, component boundaries, API flows, ER & sequence diagrams |

---

## 🧪 Testing & Validation

All 6 deterministic Python scripts are covered by automated unit tests:

```bash
python test_inspect_repository_scripts.py
```

Validating skill structure:

```bash
python quick_validate.py inspect-repository
```

---

## 📜 License

This project and skill are released under the **[GNU General Public License v3.0 (GPL-3.0)](LICENSE)**.
