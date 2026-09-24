#!/usr/bin/env python3
"""Team setup: labels, milestones, starter issues, and one onboarding issue per student.

Run by .github/workflows/team-setup.yml (Actions tab → Team setup → Run workflow).
Reads the three editable files next to this script:
    labels.tsv      label <TAB> color <TAB> description   (rarely edited)
    milestones.md   - Title | YYYY-MM-DD
    backlog.md      one "## title" section per issue (see the file for the format)

Safe to run again: existing labels are updated, existing milestones and issues
(matched by exact title) are skipped. Everything is validated before anything is
created, so a typo fails the run instead of leaving half a backlog.
Standard library only.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
USERNAME_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$")
MILESTONE_RE = re.compile(r"^-\s*(?P<title>.+?)\s*\|\s*(?P<due>\d{4}-\d{2}-\d{2})\s*$")


@dataclass
class Issue:
    title: str
    labels: list[str] = field(default_factory=list)
    milestone: str = ""
    body: str = ""


def fail(message: str) -> None:
    print(f"::error::{message}")
    sys.exit(1)


def gh(*args: str) -> str:
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode != 0:
        fail(f"gh {' '.join(args[:2])} failed: {result.stderr.strip()}")
    return result.stdout


# ── Parsing (pure, no side effects) ─────────────────────────────────────────


def parse_students(raw: str) -> list[str]:
    names = [n.lstrip("@") for n in raw.replace(",", " ").split()]
    bad = [n for n in names if not USERNAME_RE.match(n)]
    if bad:
        fail(f"Not valid GitHub usernames: {', '.join(bad)}")
    if not names:
        fail("Enter at least one student username.")
    return list(dict.fromkeys(names))  # dedupe, keep order


def parse_labels(text: str) -> list[tuple[str, str, str]]:
    labels = []
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 3 or not re.fullmatch(r"[0-9a-fA-F]{6}", parts[1]):
            fail(f"labels.tsv line {n}: expected 'name<TAB>hexcolor<TAB>description'")
        labels.append((parts[0].strip(), parts[1], parts[2].strip()))
    return labels


def parse_milestones(text: str) -> list[tuple[str, str]]:
    milestones = []
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip().startswith("-"):
            continue
        m = MILESTONE_RE.match(line.strip())
        if not m:
            fail(f"milestones.md line {n}: expected '- Title | YYYY-MM-DD', got '{line.strip()}'")
        try:
            dt.date.fromisoformat(m["due"])
        except ValueError:
            fail(f"milestones.md line {n}: '{m['due']}' is not a real date")
        milestones.append((m["title"], m["due"]))
    return milestones


def parse_backlog(text: str) -> list[Issue]:
    issues: list[Issue] = []
    current: Issue | None = None
    in_header = False
    body: list[str] = []

    def close() -> None:
        if current is not None:
            current.body = "\n".join(body).strip()
            issues.append(current)

    for line in text.splitlines():
        if line.startswith("## "):
            close()
            current, in_header, body = Issue(title=line[3:].strip()), True, []
            continue
        if current is None:
            continue  # intro text before the first issue
        key, _, value = line.partition(":")
        if in_header and key.strip().lower() == "labels":
            current.labels = [x.strip() for x in value.split(",") if x.strip()]
        elif in_header and key.strip().lower() == "milestone":
            current.milestone = value.strip()
        else:
            if line.strip():
                in_header = False
            if not in_header:
                body.append(line)
    close()
    return issues


def validate(issues: list[Issue], label_names: set[str], milestone_titles: set[str]) -> None:
    problems = []
    seen = set()
    for issue in issues:
        if issue.title in seen:
            problems.append(f"duplicate title: '{issue.title}'")
        seen.add(issue.title)
        for label in issue.labels:
            if label not in label_names:
                problems.append(f"'{issue.title}': unknown label '{label}' (add it to labels.tsv)")
        if issue.milestone and issue.milestone not in milestone_titles:
            problems.append(f"'{issue.title}': unknown milestone '{issue.milestone}' (check milestones.md)")
    if problems:
        fail("backlog.md has problems:\n  " + "\n  ".join(problems))


def onboarding_issue(student: str, milestone: str) -> Issue:
    return Issue(
        title=f"docs: add @{student} to the team table",
        labels=["good first issue", "type:docs"],
        milestone=milestone,
        body=f"""Hi @{student} 👋 This is your first task. It's small on purpose, so you can practice the whole workflow once.

- [ ] Assign this issue to yourself and move the card to **In progress**
- [ ] Create a branch named `docs/<this-issue-number>-add-{student}`
- [ ] Add your row to the **Team** table in `README.md` (name, GitHub handle, the areas you want to own)
- [ ] Open a PR titled `docs: add {student} to team table` with `Closes #<this-issue-number>` in the description
- [ ] Get it approved and merged

Read `docs/00-quickstart-ar.md` and `docs/01-workflow.md` first.""",
    )


# ── Side effects ────────────────────────────────────────────────────────────


def main() -> None:
    repo = os.environ.get("REPO") or fail("REPO is not set")
    students = parse_students(os.environ.get("STUDENTS", ""))

    labels = parse_labels((HERE / "labels.tsv").read_text(encoding="utf-8"))
    milestones = parse_milestones((HERE / "milestones.md").read_text(encoding="utf-8"))
    backlog = parse_backlog((HERE / "backlog.md").read_text(encoding="utf-8"))
    first_milestone = milestones[0][0] if milestones else ""
    issues = backlog + [onboarding_issue(s, first_milestone) for s in students]
    validate(issues, {name for name, _, _ in labels}, {t for t, _ in milestones})
    print(f"Validated: {len(labels)} labels, {len(milestones)} milestones, {len(issues)} issues.")

    for name, color, desc in labels:
        gh("label", "create", name, "--color", color, "--description", desc, "--force", "-R", repo)
    print(f"✓ {len(labels)} labels synced")

    existing_ms = set(json.loads(gh("api", f"repos/{repo}/milestones?state=all&per_page=100", "--jq", "[.[].title]")))
    for title, due in milestones:
        if title in existing_ms:
            print(f"· milestone exists: {title}")
            continue
        gh("api", f"repos/{repo}/milestones", "-f", f"title={title}", "-f", f"due_on={due}T23:59:59Z")
        print(f"✓ milestone created: {title} (due {due})")

    existing = set(json.loads(gh("issue", "list", "-R", repo, "--state", "all", "--limit", "1000",
                                 "--json", "title", "--jq", "[.[].title]")))
    created = 0
    for issue in issues:
        if issue.title in existing:
            print(f"· issue exists: {issue.title}")
            continue
        args = ["issue", "create", "-R", repo, "--title", issue.title, "--body", issue.body or " "]
        if issue.labels:
            args += ["--label", ",".join(issue.labels)]
        if issue.milestone:
            args += ["--milestone", issue.milestone]
        print(f"✓ {gh(*args).strip()}  {issue.title}")
        created += 1
    print(f"Done: {created} issues created, {len(issues) - created} already existed.")


if __name__ == "__main__":
    main()
