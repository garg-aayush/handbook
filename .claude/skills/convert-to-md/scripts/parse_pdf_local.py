#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = ["pymupdf4llm"]
# ///
"""Convert PDF(s) to Markdown locally with PyMuPDF (no API, no credits).

Best for digitally-born PDFs. For scanned documents or complex layouts
(multi-column, charts), prefer parse_pdf.py (LlamaParse).

Usage:
    uv run parse_pdf_local.py <inputs...> [--out DIR] [--images]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pymupdf4llm


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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="PDF file(s) or directory(ies)")
    ap.add_argument("--out", type=Path, default=None, help="Output directory (default: alongside each input)")
    ap.add_argument("--images", action="store_true", help="Extract embedded images to <stem>_images/")
    args = ap.parse_args()

    pdfs = collect_pdfs(args.inputs)
    if not pdfs:
        print("error: no PDFs found", file=sys.stderr)
        return 1

    failures = 0
    for pdf in pdfs:
        out_dir = args.out if args.out is not None else pdf.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{pdf.stem}.md"
        try:
            kwargs = {}
            if args.images:
                img_dir = out_dir / f"{pdf.stem}_images"
                img_dir.mkdir(parents=True, exist_ok=True)
                kwargs = {"write_images": True, "image_path": str(img_dir)}
            md = pymupdf4llm.to_markdown(str(pdf), **kwargs)
            out_path.write_text(md, encoding="utf-8")
            print(f"  wrote    {out_path}")
        except Exception as e:
            print(f"  FAILED   {pdf.name}: {e}", file=sys.stderr)
            failures += 1

    if failures:
        print(f"\n{failures} of {len(pdfs)} failed", file=sys.stderr)
        return 1
    print(f"\ndone: {len(pdfs)} file(s) converted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
