#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = ["llama-cloud>=2.1"]
# ///
"""Convert PDF(s) to Markdown via LlamaParse (v2, cost-effective tier).

Tier is locked to ``cost_effective`` (3 credits/page). Free layout-preserving
flags are always on (``spatial_text`` for multi-column / alignment, and
markdown-formatted tables). The two opt-in flags below add credits or extra
work; everything else stays at the cost-effective default.

Inputs may be individual files, shell globs, or directories (searched
recursively for ``*.pdf``). One markdown file is written per input PDF;
multi-page PDFs are joined with ``---`` page separators. Per-file failures
do not abort the batch.

Usage:
    python parse_pdf.py <file_or_dir> [<file_or_dir> ...] [--out DIR]
                       [--layout] [--images]

Flags:
    --out DIR    Output directory (default: alongside each input PDF).
    --layout     Also request structured layout boxes (+3 credits/page).
    --images     Download embedded images to ``<stem>_images/`` next to the
                 markdown. Note: cost-effective tier sometimes uses
                 placeholder filenames in the markdown that don't match the
                 extracted image files. Use the agentic tier if exact
                 in-markdown image linking matters.

Examples:
    python parse_pdf.py ~/Downloads/report.pdf
    python parse_pdf.py ~/Downloads/*.pdf --out ./md
    python parse_pdf.py ./pdf/ --out ./md --images
    python parse_pdf.py ./report.pdf --layout              # +3 credits/page

Requires:
    - ``LLAMA_CLOUD_API_KEY`` in the environment (see https://cloud.llamaindex.ai/api-key).
    - The local venv with ``llama-cloud>=2.1`` installed: activate with
      ``source .venv/bin/activate``.

Free-tier budget: 10,000 credits/month. At 3 credits/page that's ~3,300
pages/month; with ``--layout`` it's 6 credits/page (~1,600 pages/month).
"""

from __future__ import annotations

import argparse
import os
import sys
import urllib.request
from pathlib import Path

from llama_cloud import LlamaCloud

TIER = "cost_effective"  # default; 3 credits/page
VERSION = "latest"

# Free, layout-preserving output flags (don't add credits).
OUTPUT_OPTIONS = {
    "spatial_text": {
        "preserve_layout_alignment_across_pages": True,
        "do_not_unroll_columns": True,
    },
    "markdown": {
        "tables": {"output_tables_as_markdown": True},
    },
}


def collect_pdfs(paths: list[str]) -> list[Path]:
    pdfs: list[Path] = []
    for p in paths:
        path = Path(p).expanduser()
        if path.is_dir():
            pdfs.extend(sorted(path.rglob("*.pdf")))
        elif path.is_file():
            pdfs.append(path)
        else:
            print(f"warning: not found: {path}", file=sys.stderr)
    return pdfs


def parse_one(
    client: LlamaCloud,
    pdf: Path,
    out_dir: Path,
    tier: str,
    with_layout: bool,
    with_images: bool,
) -> Path:
    expand = ["markdown"]
    if with_layout:
        expand.append("layout")  # +3 credits/page
    if with_images:
        expand.append("images_content_metadata")

    output_options = dict(OUTPUT_OPTIONS)
    if with_images:
        output_options["images_to_save"] = ["embedded"]

    print(f"  uploading {pdf.name} ...")
    file = client.files.create(file=str(pdf), purpose="parse")

    print(f"  parsing  {pdf.name} (tier={tier}, layout={with_layout}, images={with_images}) ...")
    result = client.parsing.parse(
        file_id=file.id,
        tier=tier,
        version=VERSION,
        output_options=output_options,
        expand=expand,
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{pdf.stem}.md"
    with out_path.open("w", encoding="utf-8") as f:
        for i, page in enumerate(result.markdown.pages, start=1):
            if i > 1:
                f.write("\n\n---\n\n")
            f.write(page.markdown)
    print(f"  wrote    {out_path}  ({len(result.markdown.pages)} pages)")

    if with_images:
        save_images(result, out_dir, pdf.stem)

    return out_path


def save_images(result, out_dir: Path, stem: str) -> None:
    meta = getattr(result, "images_content_metadata", None)
    if meta is None:
        return
    images = getattr(meta, "images", None) or []
    if not images:
        print("  (no images returned)")
        return

    img_dir = out_dir / f"{stem}_images"
    img_dir.mkdir(parents=True, exist_ok=True)
    for img in images:
        url = getattr(img, "presigned_url", None)
        name = getattr(img, "filename", None)
        if not url or not name:
            continue
        dest = img_dir / name
        urllib.request.urlretrieve(url, dest)
    print(f"  wrote    {len(images)} image(s) to {img_dir}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="PDF file(s) or directory(ies)")
    ap.add_argument("--out", type=Path, default=None, help="Output directory (default: alongside each input)")
    ap.add_argument(
        "--tier",
        choices=["fast", "cost_effective", "agentic", "agentic_plus"],
        default=TIER,
        help="Parse tier; credits/page: fast=1, cost_effective=3, agentic=10, agentic_plus=45",
    )
    ap.add_argument("--layout", action="store_true", help="Also request structured layout (+3 credits/page)")
    ap.add_argument("--images", action="store_true", help="Download embedded images alongside the markdown")
    args = ap.parse_args()

    if not os.environ.get("LLAMA_CLOUD_API_KEY"):
        print("error: LLAMA_CLOUD_API_KEY is not set", file=sys.stderr)
        return 2

    pdfs = collect_pdfs(args.inputs)
    if not pdfs:
        print("error: no PDFs found", file=sys.stderr)
        return 1

    client = LlamaCloud()
    print(f"parsing {len(pdfs)} file(s) with tier={args.tier}")

    failures: list[tuple[Path, Exception]] = []
    for pdf in pdfs:
        out_dir = args.out if args.out is not None else pdf.parent
        try:
            parse_one(client, pdf, out_dir, args.tier, args.layout, args.images)
        except Exception as e:
            print(f"  FAILED   {pdf.name}: {e}", file=sys.stderr)
            failures.append((pdf, e))

    if failures:
        print(f"\n{len(failures)} of {len(pdfs)} failed", file=sys.stderr)
        return 1
    print(f"\ndone — {len(pdfs)} file(s) parsed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
