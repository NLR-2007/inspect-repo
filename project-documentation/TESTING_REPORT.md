# Testing Report

## Existing strategy

`test_inspect_repository_scripts.py` is a custom executable test runner. It builds temporary repositories and invokes all six scripts as subprocesses. It covers inventory exclusions, FastAPI/PyTorch/PostgreSQL signatures, entry point and route detection, evidence redaction, secret-scan exit status/redaction, and report-link validation. The suite definition is documented at [test_inspect_repository_scripts.py](test_inspect_repository_scripts.py#L1).

Audit execution on Python 3.11.9:

- All six scripted tests passed.
- All six source scripts and the test runner passed `py_compile`.
- No coverage tool, unit-test framework configuration, test matrix, or CI workflow exists.

## Coverage gaps

- Generic keyword and database-URL redaction output are not asserted end to end.
- Prefix-collision, symlink, and path-traversal cases are absent.
- Import-pattern scanning is not tested because it is not implemented.
- Fixture false positives, GraphQL/gRPC/WebSocket discovery, unreadable files, encodings, large files, and malformed manifests are not covered.
- The test runner catches only `Exception`; failed `assert` still works because `AssertionError` is an exception, but optimized Python (`-O`) would remove assertions.
- No quantitative statement/branch coverage is available.

Testing score: **58/100**. The six happy-path integration tests are useful, but security and negative-path coverage are insufficient for a production audit tool.
