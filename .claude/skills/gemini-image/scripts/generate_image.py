#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
Generate or edit images with Google's Gemini image models (Nano Banana family).

Usage:
    uv run generate_image.py --prompt "description" [--name slug] [--model flash|pro|lite]
                             [--resolution 1K|2K|4K] [--aspect square|portrait|16:9|...]
                             [--input-image PATH ...] [-n COUNT] [--format png|jpeg|webp]

Exit codes: 0 success, 1 API error or refusal, 2 bad arguments / missing API key.
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

MODEL_ALIASES = {
    "lite": "gemini-3.1-flash-lite-image",
    "flash": "gemini-3.1-flash-image",
    "pro": "gemini-3-pro-image-preview",
    "legacy": "gemini-2.5-flash-image",
}

ASPECT_SHORTCUTS = {
    "square": "1:1",
    "portrait": "3:4",
    "landscape": "4:3",
    "wide": "16:9",
    "tall": "9:16",
    "banner": "21:9",
}


def get_api_key(provided_key: str | None) -> str | None:
    """Get API key from argument first, then environment."""
    if provided_key:
        return provided_key
    return os.environ.get("GEMINI_API_KEY")


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Google's Gemini image models (Nano Banana family)"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Image description (generation) or editing instructions (with --input-image)"
    )
    parser.add_argument(
        "--filename", "-f",
        help="Output filename; overrides --name (e.g., sunset-mountains.png)"
    )
    parser.add_argument(
        "--name",
        help="Short descriptive slug; output becomes <timestamp>-<slug>.<ext>"
    )
    parser.add_argument(
        "--model", "-m",
        default="flash",
        help="Model alias (lite, flash, pro, legacy) or a raw Gemini model ID"
    )
    parser.add_argument(
        "--resolution", "-r",
        choices=["1K", "2K", "4K"],
        default="1K",
        help="Output resolution: 1K (default), 2K, or 4K"
    )
    parser.add_argument(
        "--aspect", "-a",
        help="Aspect ratio: shortcut (square, portrait, landscape, wide, tall, banner) or raw ratio like 3:2"
    )
    parser.add_argument(
        "--input-image", "-i",
        action="append",
        help="Input image path for editing/composition; repeat for multiple references"
    )
    parser.add_argument(
        "-n", "--count",
        type=int,
        default=1,
        help="Number of images to generate (suffixes _0, _1, ... when > 1)"
    )
    parser.add_argument(
        "--format",
        choices=["png", "jpeg", "webp"],
        default="png",
        help="Output format (default: png)"
    )
    parser.add_argument(
        "--compression",
        type=int,
        help="Quality 0-100 for jpeg/webp output (default 90); ignored for png"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="Gemini API key (overrides GEMINI_API_KEY env var)"
    )

    args = parser.parse_args()

    api_key = get_api_key(args.api_key)
    if not api_key:
        print("error: no API key. Provide --api-key or set GEMINI_API_KEY.", file=sys.stderr)
        sys.exit(2)

    model = MODEL_ALIASES.get(args.model, args.model)

    # Pre-flight: validate inputs before spending a request
    input_paths = args.input_image or []
    for p in input_paths:
        if not Path(p).is_file():
            print(f"error: input image not found: {p}", file=sys.stderr)
            sys.exit(2)
    if args.count < 1:
        print("error: -n must be >= 1", file=sys.stderr)
        sys.exit(2)

    resolution = args.resolution
    if model == MODEL_ALIASES["lite"] and resolution != "1K":
        # lite is 1K-only; degrade locally instead of letting the API reject
        print(f"note: {model} supports 1K only; using 1K instead of {resolution}", file=sys.stderr)
        resolution = "1K"

    aspect = ASPECT_SHORTCUTS.get(args.aspect, args.aspect) if args.aspect else None

    # Import here after arg/key checks to avoid slow import on error
    from google import genai
    from google.genai import types
    from PIL import Image as PILImage

    client = genai.Client(api_key=api_key)

    # Output path; the script stamps the time itself so callers
    # never need to know the current clock
    ext = "jpg" if args.format == "jpeg" else args.format
    if args.filename:
        base_path = Path(args.filename)
    else:
        stamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        base_path = Path(f"{stamp}-{args.name or 'image'}.{ext}")
    base_path.parent.mkdir(parents=True, exist_ok=True)

    # Load input images; auto-bump resolution to match the largest input
    # unless the user set one explicitly
    input_images = []
    for p in input_paths:
        try:
            input_images.append(PILImage.open(p))
        except Exception as e:
            print(f"error: cannot open input image {p}: {e}", file=sys.stderr)
            sys.exit(2)
    if input_images and args.resolution == "1K" and model != MODEL_ALIASES["lite"]:
        max_dim = max(max(im.size) for im in input_images)
        if max_dim >= 3000:
            resolution = "4K"
        elif max_dim >= 1500:
            resolution = "2K"
        if resolution != "1K":
            print(f"Auto-detected resolution: {resolution} (largest input dimension {max_dim}px)")

    contents = [*input_images, args.prompt] if input_images else args.prompt

    image_config_kwargs = {"image_size": resolution}
    if aspect:
        image_config_kwargs["aspect_ratio"] = aspect
    config = types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        image_config=types.ImageConfig(**image_config_kwargs),
    )

    mode = "Editing" if input_images else "Generating"
    print(f"{mode} with model={model}, resolution={resolution}"
          + (f", aspect={aspect}" if aspect else "")
          + (f", count={args.count}" if args.count > 1 else ""))

    def out_path_for(i: int) -> Path:
        if args.count == 1:
            return base_path
        return base_path.with_stem(f"{base_path.stem}_{i}")

    def save_image(data: bytes, path: Path) -> None:
        from io import BytesIO
        image = PILImage.open(BytesIO(data))
        if args.format == "jpeg":
            if image.mode in ("RGBA", "P", "LA"):
                rgb = PILImage.new("RGB", image.size, (255, 255, 255))
                rgb.paste(image, mask=image.convert("RGBA").split()[3])
                image = rgb
            image.save(str(path), "JPEG", quality=args.compression or 90)
        elif args.format == "webp":
            image.save(str(path), "WEBP", quality=args.compression or 90)
        else:
            image.save(str(path), "PNG")

    saved = 0
    for i in range(args.count):
        try:
            response = client.models.generate_content(model=model, contents=contents, config=config)
        except Exception as e:
            print(f"error: {type(e).__name__}: {e}", file=sys.stderr)
            sys.exit(1)

        image_saved = False
        for part in response.parts:
            if part.text is not None:
                print(f"Model response: {part.text}")
            elif part.inline_data is not None:
                data = part.inline_data.data
                if isinstance(data, str):
                    import base64
                    data = base64.b64decode(data)
                path = out_path_for(i)
                save_image(data, path)
                print(f"Saved: {path.resolve()}")
                image_saved = True
                saved += 1
                break
        if not image_saved:
            print("error: no image returned (request may have been refused; see model response above)",
                  file=sys.stderr)
            sys.exit(1)

    print(f"done: {saved} image(s)")
    sys.exit(0)


if __name__ == "__main__":
    main()
