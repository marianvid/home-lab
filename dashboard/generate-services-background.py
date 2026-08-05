#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 960, 376
BG = "#08111f"
CARD = "#101d30"
LINE = "#24344c"
TEXT = "#edf4ff"
MUTED = "#8fa3bd"
BLUE = "#62a8ff"

HERE = Path(__file__).resolve().parent
OUT = HERE / "assets" / "services.png"


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


image = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(image)
draw.text((28, 18), "MARIAN LAB  /  SERVICES", font=font(26, True), fill=TEXT)
draw.text((930, 21), "5/5", font=font(22, True), fill=MUTED, anchor="ra")
draw.line((28, 58, 932, 58), fill=LINE, width=2)

boxes = [
    (28, 76, 245, 188), (258, 76, 475, 188),
    (488, 76, 705, 188), (718, 76, 932, 188),
    (28, 200, 245, 312), (258, 200, 475, 312),
    (488, 200, 705, 312), (718, 200, 932, 312),
]
labels = [
    "PVE CORE", "LAB CORE", "VMs", "CONTAINERS",
    "PVE STORAGE", "FAILED UNITS", "SSH", "NODE",
]
for box, label in zip(boxes, labels):
    draw.rounded_rectangle(box, radius=14, fill=CARD, outline=LINE, width=2)
    draw.text((box[0] + 14, box[1] + 10), label.upper(),
              font=font(22, True), fill=BLUE)

image.save(OUT)
print(OUT)
