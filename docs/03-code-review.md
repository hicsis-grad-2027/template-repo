# 03 — Code review

Code review is where most learning happens on a real team. You'll review more code than you write, so it's worth doing well.

## Why we review

1. **Catch bugs** before users do.
2. **Share knowledge.** At least two people understand every part of the system, so the project survives someone being sick during exams.
3. **Keep one standard.** The codebase should look like one team wrote it.

It is **not** about proving who's smarter. Review the code, not the person.

## As the author

- **Make it easy to review.** Small PR, clear description, exact "how to test" steps, screenshots for UI.
- **Review your own diff first** on GitHub's "Files changed" tab. Remove debug prints, commented-out code, unrelated changes.
- **Don't take comments personally.** "This will crash on empty input" is a gift, not an insult.
- **Answer every comment.** Fix it, or explain why not, then resolve the thread. "Done" is a fine reply.
- **Push fixes as new commits** during review so reviewers see what changed. It's all squashed at merge anyway.

## As a reviewer

Review within **24 hours** of being requested (48h max around exams). A PR waiting for days blocks a teammate.

### What to look at, in order

1. **Does it do what the issue asked?** Read the issue's acceptance criteria first.
2. **Is it correct?** Edge cases: empty input, `None`/`null`, network failure, duplicate requests, timezones.
3. **Is it safe?** Secrets, unvalidated input, user input used in file paths or queries.
4. **Is it in the right place?** Routes don't talk to the DB directly; UI widgets don't contain business logic. See [04](04-engineering-principles.md).
5. **Is it tested?** Would the tests fail if the code were wrong?
6. **Is it readable?** Names, size of functions, comments that explain *why*.

Formatting and lint are CI's job. Don't spend review comments on them.

### Label your comments

Prefix comments so the author knows what's required:

| Prefix | Meaning |
|---|---|
| `blocking:` | Must change before merge (bug, security, wrong behavior) |
| `suggestion:` | Better way, author decides |
| `question:` | I don't understand; explain (maybe in a code comment) |
| `nit:` | Tiny, optional |
| `praise:` | Something done well — say it, it teaches as much as criticism |

Example:

> **blocking:** if `bbox` is missing this raises `KeyError` and returns 500. Validate it in the request schema so the client gets a 422.

> **suggestion:** this list of risk thresholds appears here and in `alerts.py`. Move it to one config/enum so they can't drift apart.

### Approve, comment, or request changes

- **Approve** — good to merge (maybe with nits).
- **Comment** — questions, no decision yet.
- **Request changes** — at least one `blocking:` item.

## What the supervisor looks for

The supervisor's approval is the final gate. Things that most often block a PR:

- Secrets or config hardcoded in code
- No input validation at the API boundary
- Business logic inside route handlers or UI widgets
- No test for the new behavior
- Model or data files committed; model loaded from a hardcoded path
- PR mixes several unrelated changes
- Description doesn't explain how to test it
