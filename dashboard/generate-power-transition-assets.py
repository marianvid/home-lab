#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 960, 376
BG, LINE = "#08111f", "#24344c"
TEXT, MUTED, TEAL = "#edf4ff", "#8fa3bd", "#48d7c8"
HERE = Path(__file__).resolve().parent


def font(size: int, bold: bool = False):
    candidates = [
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    raise FileNotFoundError("DejaVu Sans or Arial is required")


def render(filename: str, title: str):
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)
    draw.text((28, 18), "HOME LAB  /  SYSTEM", font=font(26, True), fill=TEXT)
    draw.line((28, 58, 932, 58), fill=LINE, width=2)
    draw.text((480, 112), title, font=font(52, True), fill=TEAL, anchor="ma")
    image.save(HERE / "assets" / filename)


render("system-rebooting.png", "REBOOTING")
render("system-shutting-down.png", "SHUTTING DOWN")
render("system-starting.png", "SYSTEM STARTING")
