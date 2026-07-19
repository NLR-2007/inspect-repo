# Risks and Limitations

## Known limitations

- Technology results are heuristic and incomplete: `import_pattern` is unused, language evidence lacks source paths, versions are frequently `Unknown`/`Repo Standard`, and NOT FOUND rows are not generated.
- Route discovery handles only a narrow set of REST decorator/call patterns and scans tests, causing false positives. It does not implement GraphQL, gRPC, WebSocket, webhook, or consumer discovery.
- Module mapping is path-name based and does not construct an import/dependency graph, public-interface map, or circular-dependency analysis.
- Inventory counts large files as “sampled” without sampling content and suppresses some file errors.
- Secret scanning uses line-local regexes and unsafe capture-group assumptions; it is not a substitute for a mature secret scanner.
- Report validation checks only Markdown links and a narrow secret regex set. Unsupported high-confidence claims do not fail validation.
- No dependency/CVE audit is possible because the project has no dependency manifest or lock file.
- No database, API service, deployment environment, or infrastructure exists to load/performance-test.

## Technical debt

Policy constants and filesystem walking are duplicated across scripts. JSON outputs lack schemas and versions. CLI behavior lacks a shared error model. Tests use a custom runner and assertions rather than a discoverable framework. Documentation promises 28-category and import-level evidence that the implementation does not fully deliver.
