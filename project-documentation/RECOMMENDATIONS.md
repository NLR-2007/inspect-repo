# Recommendations

## Prioritized roadmap

### P0 — correctness and secret safety

1. Refactor every secret pattern to identify the sensitive capture explicitly, redact the full serialized finding, and add regression fixtures for duplicate matches, connection URLs, multiline private keys, and token character variants.
2. Enforce resolved-path containment with `Path.relative_to()` across every file reader; define and test symlink behavior.
3. Make scanner read/parse failures explicit and include them in coverage metrics.

### P1 — evidence accuracy

4. Implement import scanning or remove the claim; emit evidence path/line/version source for every positive result and an explicit NOT FOUND result for all 28 declared categories.
5. Exclude tests/fixtures from live route results by default, tag source provenance, and add GraphQL/gRPC/WebSocket/webhook/consumer signatures.
6. Build a real module/import graph and report public functions, dependency directions, and cycles.
7. Make unsupported high-confidence claims validation-fatal and scan Markdown, JSON, Mermaid, and other text artifacts with the same secret rules.

### P2 — engineering system

8. Add `pyproject.toml`, a package/version, JSON Schemas, and backward-compatibility tests.
9. Adopt pytest, coverage thresholds, linting, formatting, type checking, and a Python-version CI matrix.
10. Add structured run metadata: tool version, duration, analyzed/skipped/error counts, and machine-readable diagnostics.
11. Correct README encoding, remove or add `quick_validate.py`, and reconcile feature claims with tested behavior.

### P3 — scale and release

12. Walk the tree once, cache file metadata/content hashes, stream large files, and benchmark representative monorepos.
13. Add signed/versioned releases and a documented support/security policy.
