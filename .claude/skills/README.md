# Claude Code Skills

A curated collection of [Claude Code](https://claude.com/claude-code) skills. Drop them into your global `~/.claude/skills/` directory and Claude will pick them up automatically.

## Install

Clone this repo (or this branch) and copy the skills into your `~/.claude/skills/` folder:

```bash
git clone --branch claude-skills-share https://github.com/garg-aayush/handbook.git /tmp/claude-skills-share
mkdir -p ~/.claude/skills
cp -R /tmp/claude-skills-share/.claude/skills/* ~/.claude/skills/
```

Or, if you'd rather symlink so future updates flow through after a `git pull`:

```bash
for d in /path/to/handbook/.claude/skills/*/; do
  ln -s "$d" "$HOME/.claude/skills/$(basename "$d")"
done
```

Restart Claude Code (or start a new session) and the skills will be available.

## What's included

| Skill | What it does |
| --- | --- |
| `basic-image-editing` | Resize, rotate, flip, crop, pad, convert formats (JPEG/PNG/WebP/TIFF/HEIC), transparency ops, grayscale, auto-crop borders, optimize file size. |
| `convert-to-md` | Convert PDFs and office docs (DOCX/PPTX/XLSX/HTML/EPUB) to Markdown, via the LlamaParse API or a local PyMuPDF/markitdown engine. |
| `daily-log-checklist` | Turn a daily log's bullets into a structured checklist (checkbox, title, description, status), edited in place. |
| `deslop` | Remove AI-generated code slop (excess comments, over-defensive code, style mismatches) while preserving behavior. |
| `fetch-jira-ticket` | Fetch a Jira ticket via the Atlassian MCP plugin and extract key details into a structured summary. |
| `fireflies-format` | Reformat raw Fireflies notes into structured Markdown (Key Takeaways, timestamped notes, per-person action items). |
| `gemini-image` | Generate and edit images with Google's Gemini (Nano Banana) models via a bundled script, up to 4K with aspect-ratio control. |
| `grill-me` | Stress-test an implementation plan: challenge assumptions, probe edge cases, resolve each decision branch, update the plan. |
| `interview-me` | Interview you to surface intent, goals, and constraints for a new idea, then capture a structured brief for planning. |
| `meeting-notes` | Generate structured notes from a transcript, Slack summary, or call log, in the house meeting-note format. |
| `mermaid-diagram` | Create or improve a schematic (architecture, flow, sequence, ER, state) as a themed mermaid block, with render validation. |
| `playwright-cli` | Automate browser interactions for web testing, form filling, screenshots, and data extraction. |
| `repo-onboarding` | Generate an onboarding cheat-sheet for an unfamiliar repo (stack, architecture, local dev, deploy, DBs, gotchas). |
| `review-python-code` | Review Python with an ML/API/deployment lens (data leakage, tensor shapes, device placement, secrets, resource leaks). |
| `structure-prompt` | Restructure a raw prompt into a clean, XML-tagged prompt without changing its content. |

## Notes

- Some skills (`convert-to-md`, `gemini-image`) need API keys — see the individual `SKILL.md` files for setup.
- Each skill is a self-contained directory with its own `SKILL.md` (and optional `scripts/` or `references/`).
- Older, more prescriptive variants of some skills (`commit-message`, `debug-issue`, `explain-code`, `explain-issue`, `review-code`) live in `deprecated/skills/`: kept for smaller open-source models, not auto-loaded by Claude Code. See that folder's README.
