# Ecosystem Framework Deep Dive Guide

Specific inspection patterns for major language ecosystems and web frameworks.

---

## Ecosystem Analysis Strategies

### 1. Node.js / TypeScript Ecosystem
- **Package Manager**: Inspect `package.json`, differentiate `dependencies` vs `devDependencies`.
- **Module System**: Check ESM (`"type": "module"`, `import`) vs CommonJS (`require`).
- **Framework Patterns**:
  - **Express**: App routes in `app.js` or `routes/`.
  - **Next.js**: App Router (`app/page.tsx`, `app/api/...`) vs Pages Router (`pages/api/...`).
  - **NestJS**: Controller (`@Controller`), Module (`@Module`), Service (`@Injectable`).

### 2. Python Ecosystem
- **Dependencies**: `pyproject.toml` (Poetry/Flit/Setuptools) or `requirements.txt`.
- **Framework Patterns**:
  - **FastAPI**: `FastAPI()` instance, APIRouter, Pydantic schemas in `schemas/`.
  - **Django**: `settings.py`, `urls.py`, `models.py`, `views.py` per app.
  - **Flask**: `Flask(__name__)`, route decorators `@app.route()`.

### 3. Go Ecosystem
- **Dependencies**: `go.mod`, `go.sum`.
- **Structure**: Standard layout (`cmd/` for entry points, `pkg/` or `internal/` for logic).

### 4. Java / Kotlin Ecosystem
- **Build Tool**: `pom.xml` (Maven) or `build.gradle` (Gradle).
- **Spring Boot**: `@RestController`, `@Service`, `@Repository`, `@Entity`.
