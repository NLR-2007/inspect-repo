# Security Audit & Risk Assessment Guide

This reference details security evaluation rules, secret redaction, vulnerability classification, and OWASP alignment.

---

## Security Audit Checklist

1. **Secret Detection & Redaction**: Run `detect_secrets_safely.py` to inspect codebase for unredacted tokens, API keys, and connection strings.
2. **Dependency Vulnerability Assessment**: Check lockfiles for outdated or insecure package versions.
3. **Authentication Security**: Inspect JWT token expiration, password hashing algorithms (bcrypt/argon2 vs plain md5/sha1), session cookies (HttpOnly, Secure, SameSite).
4. **Input Validation & Injection Risks**: Inspect SQL queries for raw string formatting instead of parameterized queries. Check for XSS, CSRF, and command injection vulnerabilities.
5. **Authorization & Access Control**: Check RBAC/ABAC enforcement across routes and endpoints.
6. **Data Privacy**: Ensure sensitive PII and raw credentials are not printed to logs or stdout.

---

## Finding Severity Matrix

| Severity | Criteria | Example |
|----------|----------|---------|
| **CRITICAL** | Immediate exploit risk, real exposed secret, data loss | Hardcoded production private key in public code |
| **HIGH** | Significant vulnerability requiring remediation | SQL injection vulnerability in search endpoint |
| **MEDIUM** | Violation of security best practices | Missing HttpOnly flag on authentication cookies |
| **LOW** | Minor hardening improvement | Verbose server header leaking exact version |
| **INFORMATIONAL** | Informational recommendation | Suggesting migration to Argon2 |
