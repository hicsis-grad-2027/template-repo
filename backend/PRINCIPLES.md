# 04 — Engineering principles

Frameworks change every few years. These habits don't. They apply to a FastAPI backend, a Node service, a Flutter app, or a data pipeline, so learn the habit and adapt the syntax.

Every rule a reviewer gives you is one of these five in disguise.

---

## 1. Fail loudly, fail early

Turn silent wrong behavior into an immediate, obvious error, as close to the cause as possible.

A typo in a string (`"hihg"`) fails silently, maybe weeks later. A typo in an enum (`RiskLevel.HIHG`) fails the moment the code loads. A missing environment variable read with a default of `None` crashes deep inside a request; a typed settings object crashes at startup and names the missing field.

```python
# ❌ silent: typo returns wrong result, nobody notices
if level == "hihg": send_alert()

# ✅ loud: typo is an error at import time
class RiskLevel(str, Enum):
    LOW = "low"; MEDIUM = "medium"; HIGH = "high"; VERY_HIGH = "very_high"

if level is RiskLevel.HIGH: send_alert()
```

```dart
// Same idea in Dart
enum RiskLevel { low, medium, high, veryHigh }
```

**Do:** enums for fixed sets of values, typed/validated config loaded at startup, validation on every input, explicit checks for empty results.

## 2. Single source of truth

Every fact the system depends on is written **exactly once**. Every copy is a future bug where someone updates one and forgets the other.

- Risk thresholds defined in the backend **and** hardcoded in the app → they drift. Put them in one place; have the app get them from the API.
- The DB name in three files → one settings object.
- Setup steps in the README **and** a different set in someone's head → the README is the truth; fix it when it's wrong.
- `.env.example` is the one list of every setting the system needs.

## 3. Separation of concerns

Each layer has one job and doesn't know how the others work inside.

```
Route / controller   → HTTP only: parse request, call logic, shape response
Service / logic      → the actual rules. No HTTP, no framework imports
Repository / model   → the only code that talks to the database
```

In Flutter/mobile the same shape: **widgets** draw, **state/controllers** decide, **repositories/services** fetch data.

Why it matters: logic you can call without a web server can be unit-tested, reused from a script or background job, and survives a framework or database change.

**Quick check:** does the service layer import the web framework? Does a route or widget run a DB query or build an HTTP request by hand? Either one means the layers are mixed.

## 4. Design for retry

Assume everything runs more than once: the server restarts, the user double-taps, the job re-runs after a crash, the network retries.

Ask of every state-changing operation: **"what happens if this runs twice?"** If the answer isn't "nothing bad", fix it.

- Creating a folder / collection / index → create-if-missing
- "Subscribe user to alerts for area X" → upsert, plus a unique constraint so the DB rejects duplicates
- Data ingestion job → processing the same day twice gives the same result, not double rows

## 5. Never trust input

Everything from outside (request bodies, query params, uploaded files, external APIs, even your own mobile app) is validated **at the boundary**, once. After that, the inside code can assume it's valid.

```python
class RiskQuery(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)
    days_ahead: int = Field(default=1, ge=1, le=7)
```

- Invalid input → clear 4xx error. Never a 500.
- Sanitize with an **allowlist** (what's permitted), never a blocklist (what's forbidden — you'll miss something).
- Treat file names and paths from users as hostile.
- Don't leak internals: stack traces go to logs, not to the client.

---

## The one question

When you're unsure whether code is good enough, ask:

> **"If this were wrong, when would I find out, and how hard would it be to trace?"**

Enums move the answer to *when the code loads*. Typed config: *at startup*. Boundary validation: *on the first bad request*. Magic strings and hardcoded values: *three weeks later, in the demo, with no error message*. Good design keeps the mistake close to the error it causes.

## Non-negotiables

These block a PR no matter how small it is:

- No magic strings for fixed value sets → enum
- No hardcoded config (URLs, keys, limits, paths) → environment / settings
- No DB calls in routes or widgets; no web-framework imports in business logic
- Validate input at the boundary, especially anything that becomes a file path or query
- Never commit `.env`, database files, datasets, or models
- In async code, stay async: no blocking calls (`requests`, `time.sleep`, sync DB drivers, sync file I/O) inside `async` functions

## Two-minute self-review before you request review

1. Any secret, `.env` or data file in the diff?
2. Any string that should be an enum? Any value that should be config?
3. Any DB/HTTP code in the wrong layer?
4. Any blocking call inside async code?
5. Is untrusted input validated before use?
6. Would a test fail if this code were broken?

---

*For Python/FastAPI teams: your supervisor can share the detailed backend boilerplate (settings, layering, base classes, health checks) that these principles come from.*
