# 02 — Definition of Done

"Production-ready" doesn't mean millions of users or Kubernetes. It means **someone who isn't you can run it, trust it, change it, and see what went wrong.** These lists turn that into checkboxes.

## A pull request is done when

- [ ] It does **one thing** and closes **one issue** (`Closes #N`)
- [ ] CI is green
- [ ] New behavior has at least one test (happy path + one failure case)
- [ ] No secrets, `.env`, datasets or model files in the diff
- [ ] Every new setting is read from the environment **and** added to `.env.example`
- [ ] Inputs from users or external APIs are validated at the boundary (see [the engineering principles](../backend/PRINCIPLES.md))
- [ ] Errors are handled: the user gets a clear message, the logs get the details
- [ ] README / docs updated if setup, API or behavior changed
- [ ] Approved by a code owner, all threads resolved

## A milestone is done when

- [ ] All P0 issues for the milestone are closed
- [ ] `main` builds and runs from a clean clone by following the README, **tested by a teammate who didn't write it**
- [ ] A release is tagged (`v0.x.0`) with notes
- [ ] A 2–3 minute demo was recorded or shown to the supervisor
- [ ] Open problems are issues on the board, not things people "remember"

## The project is production-ready (final release) when

**Runs anywhere**

- [ ] `git clone` → `cp .env.example .env` → **one command** (`docker compose up`) starts the backend and its dependencies
- [ ] Versions are pinned (lockfiles committed: `uv.lock`, `package-lock.json`, `pubspec.lock`)
- [ ] No hardcoded URLs, keys, paths or ports in code

**Trustworthy**

- [ ] Automated tests cover the core flows; CI runs them on every PR
- [ ] Inputs are validated; bad input gives a 4xx with a useful message, never a 500
- [ ] A `/health` endpoint (or equivalent) reports whether the service and its dependencies are up
- [ ] Logs are structured enough to answer "what happened to request X?"

**Understandable**

- [ ] README: problem, screenshot, architecture diagram, how to run, how to test, team
- [ ] `docs/architecture.md` is current, and big decisions have an ADR in `docs/adr/`
- [ ] API is documented (OpenAPI/Swagger for REST backends)
- [ ] If there's ML: a model card (what data, what metrics, known limits) — see [the AI concepts](../ai/AI-CONCEPTS.md)

**Presentable**

- [ ] `v1.0.0` release with notes
- [ ] Demo video (2–4 min) linked from the README
- [ ] License chosen; repo can be made public without embarrassment (no secrets in history, no junk files)
- [ ] Each team member can point to their own merged PRs and explain their design decisions

The last point matters most in interviews: "I built X" gets less attention than "here's the PR where I built X, and here's why I chose Y over Z."
