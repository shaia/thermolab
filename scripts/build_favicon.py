"""Draw the ThermoLab favicon (a thermometer) into theme/favicon.ico.

Both `myst.yml` files point `site.options.favicon` at the output. It has to be a real ICO,
not an SVG: the book theme serves whatever file that option names at the fixed address
`<base>/favicon.ico`, so SVG bytes would reach the browser labelled as an icon and browsers
do not sniff SVG. The output is committed, like the generated stylesheets, so a plain
`myst start` picks it up; re-run this script only when the design below changes.

The design is laid out on a 64-unit grid and drawn at 16x that, then downsampled per size,
which is what keeps the round shapes smooth at 16 px. Pillow comes in with matplotlib.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "theme" / "favicon.ico"
SIZES = [16, 24, 32, 48, 64, 128, 256]
SCALE = 16  # supersampling: grid units -> pixels

BACKGROUND = "#1f3b63"
GLASS = "#ffffff"
MERCURY = "#e5483a"


def draw() -> Image.Image:
    img = Image.new("RGBA", (64 * SCALE, 64 * SCALE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def box(x0: float, y0: float, x1: float, y1: float) -> list[float]:
        return [x0 * SCALE, y0 * SCALE, x1 * SCALE, y1 * SCALE]

    def circle(cx: float, cy: float, r: float, fill: str) -> None:
        d.ellipse(box(cx - r, cy - r, cx + r, cy + r), fill=fill)

    d.rounded_rectangle(box(0, 0, 64, 64), radius=14 * SCALE, fill=BACKGROUND)
    # Glass: stem and bulb.
    d.rounded_rectangle(box(25, 6, 39, 46), radius=7 * SCALE, fill=GLASS)
    circle(32, 46, 12, GLASS)
    # Mercury column rising out of the bulb.
    circle(32, 46, 8, MERCURY)
    d.rounded_rectangle(box(29, 22, 35, 48), radius=3 * SCALE, fill=MERCURY)
    # Scale ticks beside the stem.
    for y in (12, 21, 30):
        d.rounded_rectangle(box(44, y - 1.5, 50, y + 1.5), radius=1.5 * SCALE, fill=GLASS)
    return img


def generate() -> Path:
    master = draw()
    frames = [master.resize((s, s), Image.Resampling.LANCZOS) for s in SIZES]
    frames[-1].save(TARGET, format="ICO", sizes=[(s, s) for s in SIZES], append_images=frames[:-1])
    return TARGET


if __name__ == "__main__":
    print(f"[build_favicon] wrote {generate().relative_to(ROOT)}")
