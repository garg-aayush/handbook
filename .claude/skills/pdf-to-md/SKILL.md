---
name: pdf-to-md
description: Convert PDF file(s) in this project to Markdown using LlamaParse (cost-effective tier) via the local parse_pdf.py script. Use when the user asks to parse, convert, extract, or "turn into markdown" one or more PDFs. Optionally extracts embedded images and structured layout.
---

# pdf-to-md

Convert PDFs to Markdown using the project's `parse_pdf.py` (LlamaParse v2, `cost_effective` tier — 3 credits/page).

## When to invoke

The user asks to convert / parse / extract markdown from one or more PDF files in this project. Examples:
- "convert this pdf to markdown"
- "parse foo.pdf"
- "turn ~/Downloads/*.pdf into md, save to ./md"
- "extract the images from bar.pdf as well"

Do **not** invoke for: non-PDF formats (DOCX, HTML, etc.), or for tasks that need a different tool (Marker, Docling). Mention those alternatives if asked.

## Preconditions

1. The project venv must exist at `./.venv` and contain `llama-cloud>=2.1`.
   - If missing, recreate with: `uv venv --python 3.12 && uv pip install "llama-cloud>=2.1"`
   - Per user's standing rule: always use `uv` or `venv`, never `conda`.
2. `LLAMA_CLOUD_API_KEY` must be set. It's exported in `~/.zshrc`, so each shell call should `source ~/.zshrc` first.

## How to run

Build a single command that activates the venv, sources the env, then calls `parse_pdf.py`:

```bash
source ~/.zshrc && source .venv/bin/activate && python parse_pdf.py <inputs...> [flags]
```

### Inputs
- Single file: `python parse_pdf.py /path/to/file.pdf`
- Glob: `python parse_pdf.py ~/Downloads/*.pdf`
- Directory (recursive): `python parse_pdf.py ./pdf/`

### Flags
- `--out DIR` — write markdown into `DIR` (default: alongside each input PDF). Use `./md` when the project has a `md/` folder, or whatever the user names.
- `--images` — also download embedded images to `<stem>_images/` next to the markdown. Use only when the user asks for images.
- `--layout` — request structured layout boxes (+3 credits/page → 6 credits/page total). Use only when the user explicitly asks for layout/bounding-box data; it does **not** improve markdown quality.

### Defaults to apply when the user is vague
- If the project already has separate `pdf/` and `md/` directories, default to `--out ./md`.
- Otherwise, omit `--out` so the markdown lands next to the source PDF.
- Do not pass `--layout` or `--images` unless asked.

## Cost notes

- Free tier: 10,000 credits/month. Cost-effective = 3 credits/page → ~3,300 pages/month free.
- Adding `--layout` doubles per-page cost.
- `--images` itself is free; it just downloads what was extracted.

## Known quirk

With cost-effective tier + `--images`, some markdown image references use placeholder names (e.g. `page_1_image_1_v2.jpg`) that don't always match the extracted image files (e.g. `img_p1_2.png`). Tell the user this if they care about exact in-markdown linking — the workaround is the `agentic` tier, but the script intentionally locks to cost-effective.

## After running

- Confirm the output path(s) and page count printed by the script.
- If `--images` was used, confirm the image directory and file count.
- Do not auto-open the markdown unless the user asks.
