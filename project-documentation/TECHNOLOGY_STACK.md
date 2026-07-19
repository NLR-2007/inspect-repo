# Technology Stack

## Detected technology

| Technology | Exact repository version | Runtime observed | Evidence | Confidence |
|---|---:|---:|---|---|
| Python | Supported baseline `3.8+`; no pinned interpreter | `3.11.9` during audit | [README.md](README.md#L4), Python sources in [scripts](scripts) | CONFIRMED |
| Python standard library | Interpreter-coupled; no package version | `3.11.9` | Imports in [inventory_repository.py](scripts/inventory_repository.py#L9) and peers | CONFIRMED |
| YAML agent metadata | Not versioned | Not applicable | [agents/openai.yaml](agents/openai.yaml#L1) | CONFIRMED |
| Markdown/Mermaid documentation | Not versioned | Not applicable | [SKILL.md](SKILL.md#L1), [diagram guidelines](references/diagram-guidelines.md#L1) | CONFIRMED |

There is no dependency manifest, lock file, package-manager declaration, or third-party runtime import. Therefore reproducibility depends on a compatible Python installation rather than a resolved environment.

## 28-category detection matrix

`NOT FOUND` means the category was explicitly searched in the complete 22-file baseline inventory.

| # | Category | Result/version | Evidence | Confidence |
|---:|---|---|---|---|
| 1 | Programming language | Python; repository says 3.8+ | [README.md](README.md#L4), [scripts](scripts) | CONFIRMED |
| 2 | Runtime | CPython-compatible; no pin | [README.md](README.md#L4) | HIGH |
| 3 | Package manager | Not found | [.inventory.json](project-documentation/.inventory.json) | NOT FOUND |
| 4 | Dependency manifest | Not found | [.inventory.json](project-documentation/.inventory.json) | NOT FOUND |
| 5 | Lock file | Not found | [.inventory.json](project-documentation/.inventory.json) | NOT FOUND |
| 6 | Frontend framework | Not found | [.tech_stack.json](project-documentation/.tech_stack.json) | NOT FOUND |
| 7 | Backend framework | Not found | [.tech_stack.json](project-documentation/.tech_stack.json) | NOT FOUND |
| 8 | CLI framework | `argparse` standard library | [inventory_repository.py](scripts/inventory_repository.py#L12) | CONFIRMED |
| 9 | UI/CSS/templating | Not found | [.inventory.json](project-documentation/.inventory.json) | NOT FOUND |
| 10 | Database engine | Not found | [.inventory.json](project-documentation/.inventory.json) | NOT FOUND |
| 11 | ORM/data access | Not found | [.tech_stack.json](project-documentation/.tech_stack.json) | NOT FOUND |
| 12 | Schema/migrations | Not found | [.inventory.json](project-documentation/.inventory.json) | NOT FOUND |
| 13 | Cache | Not found | [.tech_stack.json](project-documentation/.tech_stack.json) | NOT FOUND |
| 14 | Queue/background jobs | Not found | [.structure.json](project-documentation/.structure.json) | NOT FOUND |
| 15 | API protocols | No live REST, GraphQL, gRPC, WebSocket, or webhook API | [API_DOCUMENTATION.md](project-documentation/API_DOCUMENTATION.md) | NOT FOUND |
| 16 | Authentication/identity | Not found | [SECURITY_AUDIT.md](project-documentation/SECURITY_AUDIT.md) | NOT FOUND |
| 17 | Validation/serialization | Built-in `json`; manual argument parsing | [inventory_repository.py](scripts/inventory_repository.py#L11) | CONFIRMED |
| 18 | Test framework | Custom assertion-based runner; no third-party framework | [test file](test_inspect_repository_scripts.py#L25) | CONFIRMED |
| 19 | Lint/format tool | Not found | [.inventory.json](project-documentation/.inventory.json) | NOT FOUND |
| 20 | Static type checker | Not found | [.inventory.json](project-documentation/.inventory.json) | NOT FOUND |
| 21 | Build/package tool | Not found | [.inventory.json](project-documentation/.inventory.json) | NOT FOUND |
| 22 | Containers | Not found | [.inventory.json](project-documentation/.inventory.json) | NOT FOUND |
| 23 | Orchestration | Not found | [.tech_stack.json](project-documentation/.tech_stack.json) | NOT FOUND |
| 24 | Infrastructure as code | Not found | [.inventory.json](project-documentation/.inventory.json) | NOT FOUND |
| 25 | CI/CD | Not found | [.inventory.json](project-documentation/.inventory.json) | NOT FOUND |
| 26 | Observability | Plain stdout/stderr only; no library/platform | [inventory_repository.py](scripts/inventory_repository.py#L215) | LOW |
| 27 | Cloud/hosting | Not found | [.inventory.json](project-documentation/.inventory.json) | NOT FOUND |
| 28 | AI/ML SDK/framework | Not found; the repository is agent metadata/instructions only | [.tech_stack.json](project-documentation/.tech_stack.json) | NOT FOUND |

The generated detector reported only Python as `Repo Standard` and did not emit absent categories or evidence paths for language detection. Exact support and line evidence above were therefore cross-verified manually.
