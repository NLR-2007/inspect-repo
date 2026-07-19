# Repository Structure

## Baseline inventory

| Category | Files | Notes |
|---|---:|---|
| Documentation | 13 | README, skill/prompt/template/reference material |
| Source code | 6 | Independent Python CLIs under `scripts/` |
| Test | 1 | Custom end-to-end script runner |
| Configuration | 1 | Agent display/default-prompt YAML |
| Unknown | 1 | GPL license text |
| Total | 22 | 109.55 KiB; all text; no large samples |

`.git` was detected and pruned. `node_modules`, `target`, `venv`, `dist`, `build`, and other generated directories are in the scanner exclusion set but were not present in the baseline repository. The inventory exclusion implementation is in [inventory_repository.py](scripts/inventory_repository.py#L15).

```text
repository root
|-- SKILL.md, README.md, prompt.txt, LICENSE
|-- agents/openai.yaml
|-- assets/                         templates and reusable prompt
|-- references/                     eight workflow/reference guides
|-- scripts/                        six standalone Python CLIs
`-- test_inspect_repository_scripts.py
```

No application entry point was found. Each script instead exposes a `main()` CLI. The structure analyzer groups the six files under `scripts`; its route result is a false positive caused by synthetic text in the test fixture at [test_inspect_repository_scripts.py](test_inspect_repository_scripts.py#L83).

Inventory caveat: `large_files_sampled` is incremented for oversized files, but the inventory code does not actually sample their content; see [inventory_repository.py](scripts/inventory_repository.py#L178).
