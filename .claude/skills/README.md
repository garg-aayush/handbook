# Claude Code Skills

A curated collection of [Claude Code](https://claude.com/claude-code) skills. Drop them into your global `~/.claude/skills/` directory and Claude will pick them up automatically.

## Install

Clone this repo (or this branch) and copy the skills into your `~/.claude/skills/` folder:

```bash
git clone --branch claude-skills-share https://github.com/garg-aayush/tutorials.git /tmp/claude-skills-share
mkdir -p ~/.claude/skills
cp -R /tmp/claude-skills-share/.claude/skills/* ~/.claude/skills/
```

Or, if you'd rather symlink so future updates flow through after a `git pull`:

```bash
for d in /path/to/tutorials/.claude/skills/*/; do
  ln -s "$d" "$HOME/.claude/skills/$(basename "$d")"
done
```

Restart Claude Code (or start a new session) and the skills will be available.

## What's included

| Skill | What it does |
| --- | --- |
| `basic-image-editing` | Resize, rotate, crop, pad, convert formats (JPEG/PNG/WebP/TIFF/HEIC), handle transparency, auto-crop borders, optimize file size. |
| `commit-message` | Generate commit messages for staged git changes in the repo's existing style. |
| `debug-issue` | Debug errors using logs and stack traces. |
| `deslop` | Remove AI-generated code slop — excessive comments, defensive code, style inconsistencies. |
| `explain-code` | Explain code with visual diagrams and analogies. |
| `explain-issue` | Explain errors without editing files. |
| `fetch-jira-ticket` | Fetch a Jira ticket via the Atlassian MCP plugin and extract key details. |
| `fireflies-format` | Reformat raw Fireflies meeting notes into clean, structured Markdown. |
| `nano-banana-pro` | Generate and edit images using Google's Nano Banana Pro (Gemini 3 Pro Image) API. |
| `pdf-to-md` | Convert PDFs to Markdown using LlamaParse (cost-effective tier). |
| `playwright-cli` | Automate browser interactions for web testing, form filling, screenshots, and data extraction. |
| `review-code` | Analyze code for logical errors, runtime bugs, and edge cases. |
| `review-python-code` | Review Python code for ML, APIs, and deployment. |

## Notes

- Some skills (`pdf-to-md`, `nano-banana-pro`) need API keys — see the individual `SKILL.md` files for setup.
- Each skill is a self-contained directory with its own `SKILL.md` (and optional `scripts/` or `references/`).
