#!/usr/bin/env python3
"""Apply the permanent HOME LAB LCD title to active dashboard backgrounds."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BG = "#08111f"
TEXT = "#edf4ff"
HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
             "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else
             "/System/Library/Fonts/Supplemental/Arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    raise FileNotFoundError("Install DejaVu Sans or Arial to render assets")


titles = {
    "health.png": "HOME LAB  /  HEALTH",
    "compute.png": "HOME LAB  /  COMPUTE",
    "gpu.png": "HOME LAB  /  GPU",
    "network.png": "HOME LAB  /  NETWORK",
    "services.png": "HOME LAB  /  SERVICES",
    "system-actions-reboot.png": "HOME LAB  /  SYSTEM ACTIONS",
    "system-actions-shutdown.png": "HOME LAB  /  SYSTEM ACTIONS",
}
for path in ASSETS.glob("storage-??.png"):
    titles[path.name] = "HOME LAB  /  STORAGE"

for filename, title in titles.items():
    path = ASSETS / filename
    image = Image.open(path).convert("RGB")
    draw = ImageDraw.Draw(image)
    draw.rectangle((20, 10, 700, 56), fill=BG)
    draw.text((28, 18), title, font=font(26, True), fill=TEXT)
    image.save(path)
    print(path)
