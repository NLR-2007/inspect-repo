# Project Overview

RepoLens Research Inspector is an agent-skill repository, not a hosted application. Its public contract is the workflow in [SKILL.md](SKILL.md#L27), supported by six standalone Python command-line scripts under `scripts/`. The scripts inventory repositories, detect technology signatures, map structure and route-like declarations, collect redacted evidence, scan for secret-like values, and validate Markdown reports.

The intended users are AI-agent operators and engineers auditing unfamiliar repositories. The supported operating modes and promised deliverables are defined in [SKILL.md](SKILL.md#L12). The packaged agent display metadata is in [agents/openai.yaml](agents/openai.yaml#L1).

Audit scope: branch `main`, commit `84cd5ed6be3dcc22b9e3347034246bc5a505f99c`, clean before documentation generation, audited on 2026-07-19. The baseline inventory found 22 files, 109.55 KiB total, 22 text files analyzed, no binaries, no large files, and `.git` as the only detected ignored directory. See [REPOSITORY_STRUCTURE.md](project-documentation/REPOSITORY_STRUCTURE.md).

The repository contains no live web service, database, application authentication layer, infrastructure-as-code, container, or CI/CD workflow. Test strings that resemble routes and credentials are fixtures, not deployed behavior.
