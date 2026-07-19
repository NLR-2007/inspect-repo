# API Documentation

## Network APIs

No live REST, GraphQL, gRPC, WebSocket, webhook, message-consumer, or event-stream endpoint exists. Therefore there are no HTTP methods, auth requirements, request parameters, response schemas, or calling-code paths to document.

The generated structure artifact reports `GET /api/users` at test line 83. This is a synthetic string written into a temporary fixture by [test_inspect_repository_scripts.py](test_inspect_repository_scripts.py#L77), not a repository route. Reporting it as a live endpoint would be a false positive.

## Command-line APIs

| Script | Required inputs | Optional inputs | Exit behavior |
|---|---|---|---|
| Inventory | `--root` | `--output`, `--max-size-kb` | 0 success; 1 error |
| Technology detector | `--root` | `--output` | 0 success; 1 error |
| Structure analyzer | `--root` | `--output` | 0 success; 1 error |
| Evidence collector | `--root`, `--file` | `--start`, `--end`, `--output` | 0 success; 1 error |
| Secret scanner | `--root` | `--output` | 0 success; 2 suspected real credential; 1 error |
| Report validator | `--docs`, `--root` | `--output` | 0 valid; 1 invalid/error |

CLI declarations are visible in each script's `main()`, for example [inventory_repository.py](scripts/inventory_repository.py#L215) and [validate_report_evidence.py](scripts/validate_report_evidence.py#L120).
