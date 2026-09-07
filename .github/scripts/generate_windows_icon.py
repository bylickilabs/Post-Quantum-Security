from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


ICON_SIZES = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]


def prepare_source(source: Path) -> Image.Image:
    with Image.open(source) as opened:
        image = opened.convert("RGBA")

    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    if bbox is None:
        raise RuntimeError("Icon source contains no visible pixels.")

    cropped = image.crop(bbox)
    side = max(cropped.size)
    margin = max(1, round(side * 0.045))
    canvas_side = side + (2 * margin)

    canvas = Image.new("RGBA", (canvas_side, canvas_side), (0, 0, 0, 0))
    x = (canvas_side - cropped.width) // 2
    y = (canvas_side - cropped.height) // 2
    canvas.alpha_composite(cropped, (x, y))

    return canvas.resize((1024, 1024), Image.Resampling.LANCZOS)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the official Windows application icon for Post Quantum Security.")
    parser.add_argument("--source", required=True, help="Transparent PNG source for the official PQS badge")
    parser.add_argument("--output", required=True, help="Destination .ico file")
    args = parser.parse_args()

    source = Path(args.source)
    output = Path(args.output)

    if not source.is_file():
        raise FileNotFoundError(f"Official icon source not found: {source}")

    output.parent.mkdir(parents=True, exist_ok=True)

    image = prepare_source(source)
    image.save(output, format="ICO", sizes=ICON_SIZES)

    with Image.open(output) as icon:
        sizes = set(icon.info.get("sizes", set()))
        if icon.format != "ICO":
            raise RuntimeError("Generated file is not a Windows ICO resource.")

    required = set(ICON_SIZES)
    if not required.issubset(sizes):
        missing = sorted(required - sizes)
        raise RuntimeError(f"Generated icon is missing required sizes: {missing}")

    print(f"Official PQS Windows icon written to {output}")
    print("Icon sizes:", ", ".join(f"{width}x{height}" for width, height in sorted(sizes)))


if __name__ == "__main__":
    main()
