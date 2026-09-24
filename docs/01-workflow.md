# 01 — The team workflow

In most companies, work moves like this: **issue → branch → pull request → review → merge**. This repo is set up the same way, so you learn it here and not in your first job.

## The board

The GitHub Project board is the single source of truth for who is doing what. If it's not on the board, it isn't happening.

| Column | Meaning | Who moves it |
|---|---|---|
| **Backlog** | Known work, not yet clear enough to start | Anyone adds cards |
| **Ready** | Has acceptance criteria and a size. Anyone can pick it up | Team, in planning |
| **In progress** | Someone is actively working on it. Max **2** cards per person | You, when you start |
| **In review** | A PR is open and ready for review | You, when you mark the PR ready |
| **Done** | Merged to `main` | Automatic when the PR merges |

Fields on every card: **Assignee**, **Priority** (P0 must / P1 should / P2 nice), **Size** (S ≤ 1 day, M 2–3 days, L = split it), **Area**, **Milestone**.

> **Size L means "too big".** Split it before starting. A card that sits in "In progress" for two weeks is how projects die quietly.

## Issues

Every piece of work starts as an issue created from a template (feature, bug, task/spike). A good issue has:

- **A title that says the outcome**, not the activity: "Show fire detections on map", not "Work on map".
- **Acceptance criteria** — checkboxes someone else could verify.
- **One owner.** Pairing is fine, but one name is accountable.

## Branches: one per issue, short-lived

```
<type>/<issue-number>-<short-name>

feat/12-risk-endpoint
fix/31-map-crash-on-empty-bbox
ml/18-baseline-risk-model
docs/4-architecture-v0
```

**Why not one branch per person?** A personal branch lives for months, drifts away from `main`, and ends in a giant merge nobody can review. Short branches (1–3 days) merge cleanly and get real reviews.

### Keep your branch up to date

When `main` moves while you're working:

```bash
git fetch origin
git merge origin/main          # simplest and safe; resolve conflicts, commit, push
```

Rebase (`git rebase origin/main`) gives a cleaner history, but only do it **before** others have reviewed your branch, and push with `git push --force-with-lease` (never plain `--force`).

## Commits

Small commits, each with a message that explains *why* when the diff doesn't:

```
feat(backend): cache FIRMS responses for 15 minutes

FIRMS rate-limits at 5000 requests / 10 min; the map fires one request per pan.
```

Your individual commits get **squashed** into one when the PR merges, so they don't have to be perfect. The **PR title** becomes the final commit message on `main`, and that one does have to be good.

## Pull requests

1. **Open early as a Draft** so the team sees what you're doing and CI runs from the start.
2. **Fill in the template.** "How to test it" is the most important section.
3. **Review your own diff first.** You'll catch half the comments you'd otherwise get.
4. **Mark "Ready for review"** when CI is green, and move the card to *In review*.
5. **Keep it small.** Aim for under ~400 changed lines. CI warns above 600.
6. **Respond to every comment**: fix it, or reply with why not. Then resolve the thread.
7. **Don't merge your own PR** — you can't anyway. The approver or you merge after approval (squash merge).

### What CI checks on every PR

| Check | What it catches | Fix locally with |
|---|---|---|
| `pr-hygiene` | Title/branch format, missing `Closes #N` | Edit the PR title/description |
| `repo hygiene` | Committed `.env`, model files, files > 5 MB, leaked secrets | `git rm --cached <file>`, rotate the key |
| `python (dir)` | `ruff` lint + format, `pytest` | `ruff check --fix . && ruff format .` |
| `node (dir)` | lint, build, tests | `npm run lint && npm test` |
| `flutter (dir)` | `dart format`, `flutter analyze`, `flutter test` | `dart format . && flutter analyze` |

CI finds your code by looking for `pyproject.toml` / `requirements.txt`, `package.json`, or `pubspec.yaml`, so any folder layout works.

## If you committed a secret

Deleting the file in a new commit **does not** remove it — it's still in history, and CI will keep failing.

1. **Rotate the key immediately** (revoke it in the provider's dashboard and create a new one). This is the part that matters.
2. Remove the file: `git rm --cached .env`, commit, push.
3. Tell your supervisor. The history can be cleaned, or the old (now-revoked) finding can be marked as allowed in `.gitleaksignore`.

This happens in real companies too. What matters is how fast you respond, not that it happened.

## Releases

At each milestone the team tags a release from `main`:

```bash
git switch main && git pull
git tag -a v0.2.0 -m "Walking skeleton: map shows live detections"
git push origin v0.2.0
```

Then create a GitHub Release from the tag with short notes (GitHub can generate them from merged PRs). By graduation, the history of releases tells the story of how the project grew.
