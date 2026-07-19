# Application Flows

## Full-audit flow

1. An operator asks an agent to load [SKILL.md](SKILL.md#L27).
2. The agent resolves a repository and records Git metadata.
3. Inventory, technology, structure, and secret scripts read the tree and write JSON artifacts.
4. Targeted evidence extraction reads selected line ranges with redaction.
5. The agent creates Markdown and Mermaid artifacts.
6. The report validator checks Markdown links and a narrow set of secret patterns.

## Local invocation and authentication applicability

![Editable request/auth sequence](project-documentation/diagrams/authentication_flow.mmd)

No application login, token issuance, RBAC, ABAC, session, or network request exists. Operating-system filesystem permissions and the invoking agent's authorization are the only effective access boundary. The sequence diagram states that limitation explicitly.
