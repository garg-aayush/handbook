---
name: gemini-image
description: Generate and edit images with Google's Gemini image models (Nano Banana family) via a bundled script. Text-to-image, image editing, and multi-reference composition at 1K/2K/4K with aspect-ratio control across lite/flash/pro model tiers. Do NOT read image files and do NOT write new image-generation code; always call the bundled script, passing image paths via --input-image.
when_to_use: Use when the user asks to generate, create, edit, modify, change, alter, or update images, including when they reference existing image files ("change the background", "replace X with Y", "combine these images", "make it look like a watercolor").
argument-hint: [prompt]
context: fork
agent: general-purpose
allowed-tools: Bash(uv run ${CLAUDE_SKILL_DIR}/*)
---

# Gemini Image Generation & Editing (Nano Banana family)

Generate new images or edit existing ones with Google's Gemini image models. Runs non-interactively in a fork: generate, save, and report the path(s) back.

## Operating loop

1. Classify the request: generate, edit (one input image), or multi-reference composition (several input images).
2. For crafted output (posters, text-heavy images, product renders, diagrams, photorealism) read the relevant section of `references/craft.md` first; load the smallest useful slice.
3. Pick model, resolution, and aspect from the policy tables below.
4. Pre-flight: input image paths exist; run from the user's working directory so output lands where they work.
5. Run the script, then report the `Saved:` path(s) plus one concrete refinement suggestion.
6. If the request is ambiguous AND expensive (4K, pro model, or a big batch), do not spend the credits: return 1-3 proposed directions with the flags you would use, and let the caller pick.

## Usage

```bash
# Generate
uv run ${CLAUDE_SKILL_DIR}/scripts/generate_image.py --prompt "description" --name "short-slug"

# Edit an existing image
uv run ${CLAUDE_SKILL_DIR}/scripts/generate_image.py --prompt "editing instructions" --name "slug" --input-image path/to/input.png

# Multi-reference composition (repeat --input-image; index them in the prompt)
uv run ${CLAUDE_SKILL_DIR}/scripts/generate_image.py --prompt "Put the product from Image 1 into the scene from Image 2" -i product.png -i scene.jpg --name "composite"

# Variants
uv run ${CLAUDE_SKILL_DIR}/scripts/generate_image.py --prompt "..." --name "logo-ideas" -n 4
```

## Model policy

| Alias | Model ID | Use for |
|---|---|---|
| `flash` (default) | gemini-3.1-flash-image | Everything unless stated otherwise; 4K-capable generalist, up to 14 reference images |
| `pro` | gemini-3-pro-image-preview | Final assets, dense/accurate text rendering, brand precision, complex multi-step edits, or when the user asks for top quality |
| `lite` | gemini-3.1-flash-lite-image | Bulk drafts and thumbnails; 1K only (script auto-degrades) |
| `legacy` | gemini-2.5-flash-image | Only if the user explicitly asks |

`--model` also accepts raw model IDs, so new models work without a script change. If the API returns model-not-found, the preview alias likely graduated: check https://ai.google.dev/gemini-api/docs/models and pass the current ID directly.

## Resolution and aspect policy

Resolution (`--resolution`, uppercase K): default 1K; "2K/2048/medium" gets 2K; "high-res/4K/ultra" gets 4K. When editing, the script auto-matches the largest input image unless the user set a resolution explicitly. Draft at 1K, finalize at 2K/4K.

Aspect (`--aspect`): omit for the model default. Shortcuts: `square` (1:1, social/avatars), `portrait` (3:4, posters/phone), `landscape` (4:3), `wide` (16:9, hero images/slides), `tall` (9:16, stories/mobile), `banner` (21:9). Raw ratios like `3:2` pass through.

## Filename handling

Omit `--filename`; the script stamps the current time itself and writes `<yyyy-mm-dd-hh-mm-ss>-<slug>.<ext>`.

- `--name`: short descriptive slug, 1-5 lowercase hyphen-separated words from the user's prompt (e.g. "A serene Japanese garden" gets `--name japanese-garden`). Defaults to `image`.
- `--filename`: only when the user explicitly names the output file (overrides `--name`).
- `--format png|jpeg|webp` (+ `--compression 0-100` for jpeg/webp) when the user wants a specific format or smaller files.
- With `-n N` variants, files get `_0`, `_1`, ... suffixes.

## Editing

Pass editing instructions in `--prompt` with the input via `--input-image`. State the transformation first, then pin the invariants: "change only X; keep everything else exactly the same". Repeat the invariants on every iteration; make one change per iteration. See `references/craft.md` for the full pattern.

## API key

Resolution order: `--api-key` argument, then `GEMINI_API_KEY` env var. Missing key exits with code 2 and instructions; relay them and suggest exporting `GEMINI_API_KEY` in `~/.zshrc`. Never print the key value.

## Output and exit codes

- Saved paths are printed as `Saved: <absolute path>`; report these verbatim. Do not read the image back.
- Exit 0 = success; 1 = API error or refusal (stderr has the verbatim error; surface it, especially moderation refusals on real-person edits); 2 = bad arguments or missing key (fix and retry, no credits were spent).

## References

Load only the section needed; never all files by default.

- `references/craft.md`: battle-tested prompt patterns, posters/text, product renders, photorealism, diagrams, UI mockups, edit invariants, multi-reference composition.
- `references/gemini-guide.md`: Google's official fill-in-the-blank prompt templates (7 categories) and editing patterns.
- `references/gallery.md`: 20 curated, attributed community prompts across 8 categories, each with suggested flags and the reusable pattern it demonstrates.
