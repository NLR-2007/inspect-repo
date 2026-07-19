# Architecture

RepoLens uses a script-oriented pipeline architecture. The skill document selects phases and the agent invokes independent CLIs. Each CLI reads the local filesystem and emits JSON or stdout; an external agent composes Markdown; the validator then checks Markdown outputs.

![Editable system architecture](project-documentation/diagrams/system_architecture.mmd)

There is no layered business application, service mesh, domain model, or persistence layer. Separation of concerns is primarily by command. Public interfaces are Python functions plus command-line arguments. Cross-component dependencies are artifact-level: inventory/stack/structure/security/evidence JSON informs documentation, and documentation is consumed by the validator.

Strengths are small modules, deterministic local inputs, no third-party runtime dependency, and explicit redaction intent. Weaknesses are the missing orchestration layer, repeated full-tree walks, duplicated policy constants, weak shared contracts, and no schema version on JSON outputs.
