# Diagram Guidelines & Mermaid Standards

This guide specifies syntax, style, node labeling rules, and validation practices for producing evidence-based Mermaid diagrams.

---

## Mermaid Standard Rules

1. **Evidence-Based Nodes**: Every node in a diagram MUST correspond to an audited file, module, service, database, or external integration.
2. **Inferred Nodes**: If a node is inferred, clearly label it: `NodeName["Service Name (Inferred)"]`.
3. **No Decorative Diagrams**: Avoid clutter. Split large diagrams into concise sub-diagrams.
4. **Syntax Hygiene**:
   - Quote node labels containing special characters, brackets, or spaces: `id["Client App (React)"]`.
   - Never use raw HTML tags inside node text.
   - Use standard direction: `graph TD` or `graph LR`.
5. **No Secret Exposures**: Never include real passwords, tokens, or private credentials in diagram labels.

---

## Diagram Types & Templates

### 1. System Architecture Diagram

```mermaid
graph TD
    Client["Client Browser / Mobile"] -->|HTTPS / REST| Gateway["API Gateway (Express)"]
    Gateway -->|Auth Check| AuthService["Auth Service"]
    Gateway -->|Business Logic| AppService["Core Application Service"]
    AppService -->|SQL Queries| DB[("PostgreSQL Database")]
    AppService -->|Cache Lookups| Cache[("Redis Cache")]
```

### 2. Authentication & Authorization Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Frontend as Frontend App
    participant API as API Server
    participant DB as PostgreSQL DB

    User->>Frontend: Submit Login (Email / Password)
    Frontend->>API: POST /api/v1/auth/login
    API->>DB: Query User Record & Verify Hash
    DB-->>API: User Record
    API-->>Frontend: Return JWT Access Token
    Frontend-->>User: Redirect to Dashboard
```

### 3. Entity-Relationship (ER) Diagram

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : included_in

    USER {
        string id PK
        string email
        string password_hash
        datetime created_at
    }
    ORDER {
        string id PK
        string user_id FK
        decimal total_amount
        string status
    }
```
