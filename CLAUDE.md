# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal reference repo — notes, scripts, skills, and templates. Each subdirectory is self-contained by topic (agentic-ai, llms, opencv, etc.). Not a production system.

## Key tools

- **Python execution:** Use `uv` (not pip/python directly). Run scripts with `uv run script.py` or `uv run --with <pkg> script.py`
- **GitHub CLI:** Use `gh` for PRs and issues

## Git workflow

- **Branches:** Descriptive kebab-case feature branches (e.g., `courses/claude-code`, `dev-tips`)
- **Commits:** Present-tense, descriptive messages
- **Main branch:** Protected — requires PR with 1 approval, no force-push
- **prompt-library work:** All changes to `prompt-library/` must be done on the `prompt-library` branch and merged to main via PR

## Project structure

- No root-level build/test/lint commands — each subdirectory manages its own dependencies
- Markdown is the primary format for notes and documentation
- Image assets go in `images/` subdirectories alongside their markdown files
- Claude skills use `uv run` and live in `.claude/skills/`
