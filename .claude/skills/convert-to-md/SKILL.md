---
name: convert-to-md
description: Convert documents to Markdown. PDFs go through the LlamaParse API (best quality, costs credits, tier selectable) or a local PyMuPDF engine (free, offline, no API key); other formats (DOCX, PPTX, XLSX, HTML, EPUB) are converted locally with markitdown.
when_to_use: Use when the user asks to parse, convert, extract, or "turn into markdown" PDFs or office documents (DOCX, PPTX, XLSX, HTML), including "locally", "for free", or "without the API".
argument-hint: [file(s) or folder] [--out dir]
context: fork
agent: general-purpose
model: sonnet
effort: high
allowed-tools: Bash(uv run ${CLAUDE_SKILL_DIR}/*), Bash(uvx markitdown*)
---

# convert-to-md

Convert documents to Markdown. The bundled PDF scripts carry PEP 723 inline metadata, so uv handles the Python environment automatically; no venv needed.

## Choosing an engine

- **PDF, best quality (`parse_pdf.py`)**: default for PDFs. Strongest on scanned pages, tables, multi-column, and complex layouts. Needs `LLAMA_CLOUD_API_KEY` and consumes credits.
- **PDF, local (`parse_pdf_local.py`)**: use when the user says "free", "local", "offline", "without the API", when the document is sensitive and must not leave the machine, or when credits are a concern. Good on digitally-born PDFs; weaker on scans (no OCR) and complex layouts.
- **Non-PDF formats (markitdown)**: DOCX, PPTX, XLSX, HTML, EPUB, and more, converted locally. Basic conversion quality; fine for text-centric documents.

## Preconditions

LlamaParse engine only: `LLAMA_CLOUD_API_KEY` must be set. It is exported from `~/.zshrc`, which the shell inherits automatically. If the script reports a missing key, ask the user to check that export. The local engines need nothing.

## How to run

```bash
# PDF via LlamaParse (default for PDFs)
uv run ${CLAUDE_SKILL_DIR}/scripts/parse_pdf.py <inputs...> [flags]

# PDF locally, free, offline
uv run ${CLAUDE_SKILL_DIR}/scripts/parse_pdf_local.py <inputs...> [--out DIR] [--images]

# Non-PDF formats
uvx markitdown input.docx -o output.md
```

### Inputs (PDF scripts)

- Single file: `.../parse_pdf.py /path/to/file.pdf`
- Glob: `.../parse_pdf.py ~/Downloads/*.pdf`
- Directory (recursive): `.../parse_pdf.py ./pdf/`

markitdown takes one input file per call; loop over files for batches.

### Flags (LlamaParse engine)

- `--out DIR`: write markdown into `DIR` (default: alongside each input PDF).
- `--tier`: `fast` (1 credit/page), `cost_effective` (3, default), `agentic` (10), `agentic_plus` (45). Escalate above cost_effective only when the user asks for higher quality or a complex document parses poorly.
- `--images`: also download embedded images to `<stem>_images/` next to the markdown. Use only when the user asks for images.
- `--layout`: request structured layout boxes (+3 credits/page). Use only when the user explicitly asks for layout or bounding-box data; it does NOT improve markdown quality.

### Defaults to apply when the user is vague

- If the working project has separate `pdf/` and `md/` directories, default to `--out ./md`.
- Otherwise omit `--out` so the markdown lands next to the source file.
- Do not pass `--layout` or `--images` unless asked.

## Cost notes (LlamaParse engine)

- Free plan: 10,000 credits/month. Cost-effective = 3 credits/page, roughly 3,300 pages/month free.
- Adding `--layout` costs +3 credits/page on top of the tier.
- `--images` itself is free; it just downloads what was extracted.
- The local engines cost nothing regardless of volume.

## Known quirk

With cost-effective tier + `--images`, some markdown image references use placeholder names (e.g. `page_1_image_1_v2.jpg`) that don't always match the extracted image files (e.g. `img_p1_2.png`). Tell the user this if they care about exact in-markdown linking; the workaround is rerunning with `--tier agentic`.

## After running

- Confirm the output path(s) and, for the LlamaParse engine, the page count printed by the script.
- If `--images` was used, confirm the image directory and file count.
- Do not auto-open the markdown unless the user asks.
