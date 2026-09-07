from __future__ import annotations

import argparse
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


CANVAS_SIZE = 1024
ICON_SIZES = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

BACKGROUND = (8, 10, 14, 255)
PANEL = (12, 15, 20, 255)
GOLD = (207, 164, 74, 255)
GOLD_LIGHT = (245, 214, 132, 255)
GOLD_DARK = (100, 78, 34, 255)


def find_bold_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf",
        r"C:\Windows\Fonts\arialbd.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    ]
    for candidate in candidates:
        if os.path.isfile(candidate):
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def build_icon() -> Image.Image:
    image = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), BACKGROUND)
    draw = ImageDraw.Draw(image)

    center = CANVAS_SIZE // 2

    for radius in range(460, 40, -8):
        progress = (460 - radius) / 420
        shade = int(24 - (12 * progress))
        draw.ellipse(
            (center - radius, center - radius, center + radius, center + radius),
            fill=(shade, shade + 2, shade + 6, 255),
        )

    draw.rounded_rectangle((70, 70, 954, 954), radius=150, outline=GOLD, width=22)
    draw.rounded_rectangle((92, 92, 932, 932), radius=132, outline=GOLD_DARK, width=4)

    shield = [(512, 170), (760, 260), (728, 596), (512, 824), (296, 596), (264, 260)]
    draw.polygon(shield, fill=PANEL)
    draw.line(shield + [shield[0]], fill=GOLD_LIGHT, width=18, joint="curve")

    orbit_box = (320, 300, 704, 684)
    for angle in (0, 60, 120):
        layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
        layer_draw = ImageDraw.Draw(layer)
        layer_draw.ellipse(orbit_box, outline=GOLD, width=12)
        layer = layer.rotate(angle, center=(512, 492), resample=Image.Resampling.BICUBIC)
        image.alpha_composite(layer)

    draw = ImageDraw.Draw(image)
    draw.ellipse((474, 454, 550, 530), fill=GOLD_LIGHT)

    for x, y in ((512, 300), (664, 492), (360, 492)):
        draw.ellipse((x - 16, y - 16, x + 16, y + 16), fill=GOLD_LIGHT)

    draw.line((560, 560, 650, 650), fill=GOLD_LIGHT, width=20)

    font = find_bold_font(126)
    label = "PQS"
    box = draw.textbbox((0, 0), label, font=font)
    text_width = box[2] - box[0]
    draw.text(((CANVAS_SIZE - text_width) // 2, 700), label, font=font, fill=GOLD_LIGHT)

    return image


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the Windows application icon for Post Quantum Security.")
    parser.add_argument("--output", required=True, help="Destination .ico file")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    image = build_icon()
    image.save(output, format="ICO", sizes=ICON_SIZES)

    with Image.open(output) as icon:
        sizes = set(icon.info.get("sizes", set()))

    required = set(ICON_SIZES)
    if not required.issubset(sizes):
        missing = sorted(required - sizes)
        raise RuntimeError(f"Generated icon is missing required sizes: {missing}")

    print(f"Windows icon written to {output}")
    print("Icon sizes:", ", ".join(f"{width}x{height}" for width, height in sorted(sizes)))


if __name__ == "__main__":
    main()
