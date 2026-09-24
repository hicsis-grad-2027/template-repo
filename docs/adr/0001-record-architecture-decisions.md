# ADR-0001: Record architecture decisions

**Status:** Accepted  
**Date:** YYYY-MM-DD  
**Deciders:** team + supervisor

## Context

Over a year-long project we'll make decisions (which database, which data source, how to split data, mobile framework, how the model is served) that later look arbitrary unless the reasons are written down. New teammates, reviewers, examiners and future employers will ask "why did you do it this way?"

## Decision

We record every significant decision as a short Architecture Decision Record (ADR) in `docs/adr/`, numbered in order, using [template.md](template.md). An ADR is added in the same PR as the change it describes. Once accepted, an ADR isn't edited. If we change our minds, we write a new ADR that supersedes it.

"Significant" = hard to reverse, affects more than one person's area, or we argued about it.

## Consequences

- Decisions are reviewable in PRs like code.
- The graduation defense can point to real reasoning, not memory.
- Small overhead: roughly 15 minutes per decision.
