# Deprecated skills

These skills are deprecated for frontier-model harnesses, but kept on purpose.

## Why they are here

Modern frontier models (Claude Sonnet/Opus class) do these tasks natively, and Claude Code ships built-in skills that supersede two of them (`review-code` is covered by the built-in `/code-review`; `commit-message` is native behavior). Keeping them in `.claude/skills/` would only add trigger noise for those harnesses, so they live outside `.claude/` where nothing auto-loads them.

They are NOT dead weight: **smaller open-source models (roughly 7B-30B) benefit from exactly the explicit scaffolding these skills provide**, numbered steps, output templates, and hard guardrails that a frontier model does not need. If you point an agent harness at a local or open-source model, these skills raise output quality noticeably.

## How to use with an open-source model

- Copy the skill folder into whatever skills directory your harness discovers (the SKILL.md format follows the open [Agent Skills](https://agentskills.io) standard), or paste the SKILL.md body into the system prompt.
- These files deliberately use only portable frontmatter (`name`, `description`). Claude Code extensions (`context: fork`, `model`, `effort`, `allowed-tools`) are omitted so nothing breaks in other harnesses.
- Bodies are intentionally more prescriptive and verbose than the main `.claude/skills/` tier: small models cannot fill gaps, so the steps do not leave any.

## Contents

| Skill | Task |
|---|---|
| `commit-message` | Generate commit messages for staged changes |
| `debug-issue` | Root-cause and fix an error from logs/stack traces |
| `explain-issue` | Explain an error without editing anything |
| `explain-code` | Explain how code works with analogies and diagrams |
| `review-code` | Correctness-focused code review report |
