#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "openai>=1.50.0,<2",
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
Generate and edit images using either:
  - OpenAI GPT Image 1.5 (generation + edits, optional mask inpainting), or
  - Gemini 3 Pro Image (Nano Banana Pro) (generation + image-to-image edits).

Examples:
  # Auto provider selection (uses OPENAI_API_KEY if present, else GEMINI_API_KEY)
  uv run scripts/generate_image.py --prompt "A cozy cabin in the snow" --filename "out.png"

  # Force provider
  uv run scripts/generate_image.py --provider openai --prompt "..." --filename "out.png"
  uv run scripts/generate_image.py --provider gemini --prompt "..." --filename "out.png"

  # Edit
  uv run scripts/generate_image.py --prompt "Make it look like a watercolor" --filename "out.png" --input-image "in.png"

  # Masked inpainting (OpenAI only)
  uv run scripts/generate_image.py --provider openai --prompt "A red balloon" --filename "out.png" --input-image "in.png" --mask "mask.png"
"""

from __future__ import annotations

import argparse
import base64
import os
import sys
from io import BytesIO
from pathlib import Path
from typing import Literal, cast


Provider = Literal["auto", "openai", "gemini"]
ResolvedProvider = Literal["openai", "gemini"]


def _eprint(message: str) -> None:
    print(message, file=sys.stderr)


def _env(key: str) -> str | None:
    value = os.environ.get(key)
    return value if value else None


def _existing_file(path: str | None, flag_name: str) -> Path | None:
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"{flag_name} not found: {path}")
    if not p.is_file():
        raise FileNotFoundError(f"{flag_name} is not a file: {path}")
    return p


def _create_full_transparent_mask_bytes(image_path: Path) -> bytes:
    from PIL import Image

    with Image.open(image_path) as img:
        width, height = img.size

    mask = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    buf = BytesIO()
    mask.save(buf, format="PNG")
    return buf.getvalue()


def _resolve_provider(
    provider: Provider,
    api_key: str | None,
    openai_api_key: str | None,
    gemini_api_key: str | None,
) -> tuple[ResolvedProvider, str]:
    if api_key and provider == "auto":
        raise ValueError("`--api-key` requires `--provider openai` or `--provider gemini` (not auto).")

    resolved_openai_key = api_key if provider == "openai" else openai_api_key
    resolved_gemini_key = api_key if provider == "gemini" else gemini_api_key

    if provider == "openai":
        if not resolved_openai_key:
            raise ValueError("No OpenAI key: provide `--api-key`/`--openai-api-key` or set `OPENAI_API_KEY`.")
        return "openai", resolved_openai_key

    if provider == "gemini":
        if not resolved_gemini_key:
            raise ValueError("No Gemini key: provide `--api-key`/`--gemini-api-key` or set `GEMINI_API_KEY`.")
        return "gemini", resolved_gemini_key

    # provider == "auto"
    if openai_api_key:
        return "openai", openai_api_key
    if gemini_api_key:
        return "gemini", gemini_api_key

    raise ValueError(
        "No API key found. Set `OPENAI_API_KEY` or `GEMINI_API_KEY`, or pass `--provider ... --api-key ...`."
    )


def _openai_generate(
    api_key: str,
    prompt: str,
    quality: Literal["low", "medium", "high"],
    size: Literal["1024x1024", "1024x1536", "1536x1024", "auto"],
    background: Literal["transparent", "opaque", "auto"],
) -> bytes:
    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    tool_config: dict[str, object] = {"type": "image_generation", "quality": quality}
    if size != "auto":
        tool_config["size"] = size
    if background != "auto":
        tool_config["background"] = background

    response = client.responses.create(
        model="gpt-4.1",  # orchestrates the image generation tool
        input=prompt,
        tools=[tool_config],
    )

    for output in response.output:
        if output.type == "image_generation_call":
            return base64.b64decode(cast(str, output.result))

    raise RuntimeError("OpenAI: no image was generated in the response.")


def _openai_edit(
    api_key: str,
    prompt: str,
    input_image: Path,
    mask: Path | None,
    size: Literal["1024x1024", "1024x1536", "1536x1024", "auto"],
) -> bytes:
    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    if mask is not None:
        mask_file = open(mask, "rb")
    else:
        mask_bytes = _create_full_transparent_mask_bytes(input_image)
        mask_file = BytesIO(mask_bytes)
        mask_file.name = "mask.png"

    try:
        result = client.images.edit(
            model="gpt-image-1.5",
            image=open(input_image, "rb"),
            mask=mask_file,
            prompt=prompt,
            size=size if size != "auto" else "1024x1024",
        )
        image_base64 = result.data[0].b64_json
        return base64.b64decode(image_base64)
    finally:
        if mask is not None:
            mask_file.close()


def _infer_gemini_resolution_from_input(input_image: Path) -> Literal["1K", "2K", "4K"]:
    from PIL import Image as PILImage

    with PILImage.open(input_image) as img:
        width, height = img.size
    max_dim = max(width, height)
    if max_dim >= 3000:
        return "4K"
    if max_dim >= 1500:
        return "2K"
    return "1K"


def _gemini_generate_or_edit(
    api_key: str,
    prompt: str,
    resolution: Literal["1K", "2K", "4K"],
    input_image: Path | None,
) -> bytes:
    from google import genai
    from google.genai import types
    from PIL import Image as PILImage

    client = genai.Client(api_key=api_key)

    if input_image is not None:
        image = PILImage.open(input_image)
        contents: object = [image, prompt]
    else:
        contents = prompt

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(image_size=resolution),
        ),
    )

    # Prefer the first image part; still print text parts for debugging/context.
    image_bytes: bytes | None = None
    for part in getattr(response, "parts", []):
        if getattr(part, "text", None) is not None:
            print(f"Model response: {part.text}")
            continue
        inline = getattr(part, "inline_data", None)
        if inline is not None and getattr(inline, "data", None) is not None and image_bytes is None:
            data = inline.data
            if isinstance(data, bytes):
                image_bytes = data
            elif isinstance(data, str):
                image_bytes = base64.b64decode(data)

    if image_bytes is None:
        raise RuntimeError("Gemini: no image was generated in the response.")
    return image_bytes


def _save_png(
    image_bytes: bytes,
    output_path: Path,
    *,
    preserve_alpha: bool,
) -> None:
    from PIL import Image

    output_path.parent.mkdir(parents=True, exist_ok=True)

    image = Image.open(BytesIO(image_bytes))

    if preserve_alpha:
        # Preserve transparency if present/possible.
        if image.mode != "RGBA":
            try:
                image = image.convert("RGBA")
            except Exception:
                pass
        image.save(str(output_path), "PNG")
        return

    # Flatten onto white background.
    if image.mode == "RGBA":
        rgb_image = Image.new("RGB", image.size, (255, 255, 255))
        rgb_image.paste(image, mask=image.split()[3])
        rgb_image.save(str(output_path), "PNG")
    else:
        image.convert("RGB").save(str(output_path), "PNG")


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Image Tools (OpenAI GPT Image 1.5 + Gemini Nano Banana Pro)")
    parser.add_argument("--prompt", "-p", required=True, help="Image description or editing instructions")
    parser.add_argument("--filename", "-f", required=True, help="Output filename (PNG recommended)")
    parser.add_argument(
        "--provider",
        choices=["auto", "openai", "gemini"],
        default="auto",
        help="Provider: auto (default), openai, or gemini",
    )

    parser.add_argument("--input-image", "-i", help="Optional input image path for editing/modification")
    parser.add_argument(
        "--mask",
        "-m",
        help="Optional mask image path for precise inpainting (OpenAI only; PNG with transparent areas to edit)",
    )

    # OpenAI-only controls
    parser.add_argument("--quality", "-q", choices=["low", "medium", "high"], default="medium")
    parser.add_argument("--size", "-s", choices=["1024x1024", "1024x1536", "1536x1024", "auto"], default="1024x1024")
    parser.add_argument("--background", "-b", choices=["transparent", "opaque", "auto"], default="auto")

    # Gemini-only controls
    parser.add_argument(
        "--resolution",
        "-r",
        choices=["1K", "2K", "4K"],
        default=None,
        help="Gemini output resolution (default: 1K, or inferred from input image size when editing)",
    )

    # API keys
    parser.add_argument("--api-key", "-k", help="API key for the chosen provider (requires --provider openai|gemini)")
    parser.add_argument("--openai-api-key", help="OpenAI API key (overrides OPENAI_API_KEY)")
    parser.add_argument("--gemini-api-key", help="Gemini API key (overrides GEMINI_API_KEY)")

    args = parser.parse_args()

    try:
        input_image = _existing_file(args.input_image, "--input-image")
        mask = _existing_file(args.mask, "--mask")
    except FileNotFoundError as e:
        _eprint(f"Error: {e}")
        sys.exit(1)

    openai_key = args.openai_api_key or _env("OPENAI_API_KEY")
    gemini_key = args.gemini_api_key or _env("GEMINI_API_KEY")

    try:
        provider, provider_key = _resolve_provider(
            cast(Provider, args.provider),
            args.api_key,
            openai_key,
            gemini_key,
        )
    except ValueError as e:
        _eprint(f"Error: {e}")
        sys.exit(1)

    output_path = Path(args.filename)

    try:
        if provider == "openai":
            if args.resolution is not None:
                raise ValueError("`--resolution` is Gemini-only. Use `--size`/`--quality`/`--background` for OpenAI.")

            if input_image is not None:
                if mask is not None:
                    print("OpenAI: editing (mask inpainting)...")
                else:
                    print("OpenAI: editing (full-image edit)...")
                image_bytes = _openai_edit(
                    provider_key,
                    args.prompt,
                    input_image,
                    mask,
                    cast(Literal["1024x1024", "1024x1536", "1536x1024", "auto"], args.size),
                )
            else:
                if mask is not None:
                    raise ValueError("`--mask` requires `--input-image`.")
                print("OpenAI: generating...")
                image_bytes = _openai_generate(
                    provider_key,
                    args.prompt,
                    cast(Literal["low", "medium", "high"], args.quality),
                    cast(Literal["1024x1024", "1024x1536", "1536x1024", "auto"], args.size),
                    cast(Literal["transparent", "opaque", "auto"], args.background),
                )

            preserve_alpha = args.background == "transparent"
            _save_png(image_bytes, output_path, preserve_alpha=preserve_alpha)

        else:
            # provider == "gemini"
            if args.quality != "medium" or args.size != "1024x1024" or args.background != "auto":
                raise ValueError(
                    "OpenAI-only flags detected (`--quality/--size/--background`). For Gemini use `--resolution`."
                )
            if mask is not None:
                raise ValueError("`--mask` is OpenAI-only.")

            resolution = cast(Literal["1K", "2K", "4K"], args.resolution) if args.resolution else None
            if resolution is None:
                if input_image is not None:
                    resolution = _infer_gemini_resolution_from_input(input_image)
                    print(f"Gemini: inferred resolution {resolution} from input image.")
                else:
                    resolution = "1K"

            print("Gemini: generating..." if input_image is None else f"Gemini: editing (resolution {resolution})...")
            image_bytes = _gemini_generate_or_edit(provider_key, args.prompt, resolution, input_image)
            _save_png(image_bytes, output_path, preserve_alpha=False)

        print(f"\nImage saved: {output_path.resolve()}")

    except Exception as e:
        _eprint(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
