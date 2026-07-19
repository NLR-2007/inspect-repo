# Technology Signatures & Evidence Guide

This reference outlines signature patterns and confidence criteria across 28 tech stack categories.

---

## 28 Technology Categories & Confidence Criteria

### Confidence Levels

- **CONFIRMED**: Explicit manifest dependency, active configuration, or executable code imports verified by file/line.
- **HIGH**: Strong indirect evidence across multiple repository files.
- **MEDIUM**: Framework naming conventions or standard directory structures.
- **LOW**: Inferred from comments, documentation, or optional dependencies.
- **NOT FOUND**: Searched explicitly but not present in repository.

---

## Signature Catalog

### 1. Programming Languages
- **Python**: `pyproject.toml`, `requirements.txt`, `Pipfile`, `.py` files.
- **TypeScript / JavaScript**: `package.json`, `tsconfig.json`, `.ts`, `.tsx`, `.js`, `.jsx`.
- **Go**: `go.mod`, `go.sum`, `.go` files.
- **Java / Kotlin**: `pom.xml`, `build.gradle`, `.java`, `.kt` files.
- **Rust**: `Cargo.toml`, `Cargo.lock`, `.rs` files.
- **C# / .NET**: `*.csproj`, `*.sln`, `.cs` files.

### 2. Frontend Frameworks
- **React**: `package.json` -> `"react"`, import `react`, JSX/TSX syntax.
- **Next.js**: `package.json` -> `"next"`, `next.config.js`, `app/` or `pages/` directory.
- **Vue / Nuxt**: `package.json` -> `"vue"` or `"nuxt"`, `.vue` single-file components.
- **Angular**: `package.json` -> `"@angular/core"`, `angular.json`.

### 3. Backend Frameworks
- **FastAPI**: `requirements.txt` -> `fastapi`, `from fastapi import FastAPI`.
- **Django**: `manage.py`, `settings.py`, `urls.py`, `django` manifest entry.
- **Express / NestJS**: `package.json` -> `"express"` or `"@nestjs/core"`.
- **Spring Boot**: `pom.xml` -> `spring-boot-starter-web`, `@SpringBootApplication`.

### 4. Databases & Storage
- **PostgreSQL**: `psycopg2`, `asyncpg`, `pg`, `docker-compose.yml` service `postgres`.
- **MongoDB**: `pymongo`, `mongoose`, `mongodb://` URI patterns.
- **Redis**: `redis-py`, `ioredis`, `REDIS_URL` env variable.
- **SQLite**: `.sqlite`, `.db` files, `sqlite3` module imports.

### 5. AI / ML Frameworks
- **PyTorch / TensorFlow**: `torch`, `tensorflow` imports and manifest dependencies.
- **OpenAI / Anthropic**: `openai`, `@anthropic-ai/sdk` imports.
- **LangChain / LlamaIndex**: `langchain`, `llamaindex` dependencies.
- **HuggingFace**: `transformers`, `diffusers`, `datasets`.

### 6. Containers & CI/CD
- **Docker**: `Dockerfile`, `docker-compose.yml`, `.dockerignore`.
- **Kubernetes**: `deployment.yaml`, `service.yaml`, Helm charts in `charts/`.
- **GitHub Actions**: `.github/workflows/*.yml`.
- **Terraform**: `*.tf`, `terraform.tfstate`.
