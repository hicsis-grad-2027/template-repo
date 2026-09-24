# Starter backlog

Edit this for the team's project, then run **Actions → Team setup**. Plan M1–M2 only; the team adds the rest as they learn.

Format: every issue starts with `## title`, then optional `labels:` and `milestone:` lines, then a blank line, then the description (Markdown). Labels must exist in `labels.tsv`; milestones must match `milestones.md` exactly.

## docs: rewrite the proposal as a scoped MVP
labels: type:docs, needs-supervisor
milestone: M1 Setup & scoped proposal

Pick ONE feature that works end to end first. Everything else is stretch or future work.

**Done when**
- [ ] `docs/proposal.md`: problem, users, MVP scope, what is explicitly OUT of scope
- [ ] 3–5 measurable success criteria
- [ ] Reviewed with the supervisor

## docs: architecture v0 and API contract draft
labels: type:docs, area:backend
milestone: M1 Setup & scoped proposal

Fill in `docs/architecture.md`: components, the main flow, and a first API contract table.

**Done when**
- [ ] Diagram + component table with an owner per component
- [ ] API contract agreed by frontend/mobile and backend owners
- [ ] ADR-0002 written for the main technology choice

## data: spike: main data source
labels: type:chore, area:data
milestone: M1 Setup & scoped proposal

Time box: 2 days. Find out what data the project really has access to.

**Done when**
- [ ] `docs/data/<source>.md` data card: source, fields, license/terms, rate limits, size, known gaps
- [ ] Recommendation: is it enough for the MVP?

## feat: app skeleton
labels: type:feature, area:mobile
milestone: M1 Setup & scoped proposal

- [ ] App project created (in `mobile/` or `frontend/`), runs locally
- [ ] One real screen, placeholder data
- [ ] API base URL read from config, not hardcoded
- [ ] CI green (format + analyze/lint)

## feat(backend): service skeleton with /health, config and Docker
labels: type:feature, area:backend, area:devops
milestone: M1 Setup & scoped proposal

- [ ] Backend in `backend/` with typed settings loaded from `.env` (fails at startup if a required value is missing)
- [ ] `GET /health` returns status and app version
- [ ] Dockerfile + `docker-compose.yml`: `docker compose up` starts it
- [ ] One test for `/health`; CI green

## feat: walking skeleton: one real flow end to end
labels: type:feature, area:backend, area:mobile
milestone: M2 Walking skeleton

The thinnest possible version of the main flow: app → backend → real data → back to the app. Ugly is fine; working is the point.

- [ ] Split into smaller issues (one per person) before starting
- [ ] Demo from `main` on a teammate's machine
