# Architecture Analysis & Module Mapping Guide

Guidelines for auditing software architecture, component boundaries, separation of concerns, and data flow.

---

## Architectural Patterns & Evaluation

### 1. Monolith vs Microservices vs Monorepo
- **Monolith**: Single codebase, shared domain models, unified deployment target.
- **Monorepo**: Workspace configuration (`pnpm-workspace.yaml`, `lerna.json`, `Cargo.toml [workspace]`), multiple sub-packages under `packages/` or `apps/`.
- **Microservices**: Multiple independent services with distinct entry points, Dockerfiles, and gRPC/REST inter-service communications.

### 2. Layered & Hexagonal Architecture
- **Presentation Layer**: Controllers, API routes, GraphQL resolvers, UI components.
- **Business Logic Layer**: Domain models, services, use cases, business rules.
- **Data Access Layer**: Repositories, ORM entities, database queries, migration scripts.
- **Infrastructure Layer**: Third-party API clients, message brokers, caching wrappers.

---

## Module Boundary Checklist

1. **Separation of Concerns**: Ensure UI logic is decoupled from database queries.
2. **Dependency Direction**: High-level modules should not depend directly on low-level infrastructure details.
3. **Circular Dependencies**: Scan imports for cyclical references across modules.
4. **Data Isolation**: Evaluate whether services access database tables directly or via public interfaces.
