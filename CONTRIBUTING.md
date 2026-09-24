# Contributing — how this team works

This repo runs like a real engineering team. The rules are few and they are enforced by GitHub, not by memory.

**Read in this order (about 30 minutes total):**

1. [docs/00-quickstart-ar.md](docs/00-quickstart-ar.md) — ملخص سريع بالعربي
2. [docs/01-workflow.md](docs/01-workflow.md) — issue → branch → PR → merge
3. [docs/02-definition-of-done.md](docs/02-definition-of-done.md) — what "done" and "production-ready" mean here
4. [docs/03-code-review.md](docs/03-code-review.md) — how to review and be reviewed
5. [docs/04-engineering-principles.md](docs/04-engineering-principles.md) — the five habits behind good backend code
6. [docs/05-ai-and-mlops-concepts.md](docs/05-ai-and-mlops-concepts.md) — only if the project has an AI/ML part

## The loop, in one screen

```bash
# 1. Pick an issue from the board's "Ready" column, assign yourself, move it to "In progress".

# 2. Branch from an up-to-date main. Name = type/issue-number-short-name
git switch main && git pull
git switch -c feat/12-risk-endpoint

# 3. Commit small and often.
git add -p
git commit -m "feat(backend): validate bbox query params"

# 4. Push and open a PR early (as Draft if not ready). Description must say "Closes #12".
git push -u origin feat/12-risk-endpoint
gh pr create --fill --draft        # or use the GitHub website

# 5. When CI is green and you've reviewed your own diff: "Ready for review".
# 6. Address review comments with new commits. Don't force-push during review.
# 7. It gets squash-merged. The branch is deleted. The issue closes. The card moves to Done.
```

## Rules GitHub enforces

| Rule | Enforced by |
|---|---|
| Nobody pushes to `main` directly — not even the team lead | Branch ruleset |
| Every PR needs an approving review from a code owner | `CODEOWNERS` + ruleset |
| CI must be green: lint, format, tests, secret scan, no committed `.env`/models/huge files | `ci.yml` → `ci-gate` |
| PR title like `feat(scope): ...`, branch like `feat/12-name`, description says `Closes #12` | `pr-hygiene.yml` |
| Review comments must be resolved before merge | Ruleset |

## Commit and PR title types

`feat` new behavior · `fix` bug fix · `docs` documentation · `refactor` no behavior change · `test` tests only · `ml` model/training work · `data` data pipeline · `chore` setup/tooling · `ci` workflows · `perf` performance · `style` formatting only

Scope (optional) is the area: `feat(mobile): ...`, `fix(backend): ...`, `ml(risk-model): ...`.

## Getting help

Stuck for more than an hour? Say so in the issue with what you tried. Blocked by someone else's work? Add the `blocked` label and mention them. Asking early is a production skill, not a weakness.
