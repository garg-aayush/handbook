# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal reference repo — notes, scripts, skills, and templates. Each subdirectory is self-contained by topic (llms, opencv-dip, prompt-library, etc.). Not a production system.

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
- Name sub-directory readmes `README.md` (uppercase), not `Readme.md`
- Claude skills use `uv run` and live in `.claude/skills/`; each has its own `SKILL.md`
- `.cursor/` mirrors a subset of the skills as Cursor slash-commands
- `deprecated/skills/` holds older, more prescriptive skill variants kept for smaller open-source models; they live outside `.claude/` on purpose so nothing auto-loads them
- `reading-list/` holds either atomic resource files (in category folders, with YAML frontmatter) or curated topic guides (root-level `.md` files); see its README
