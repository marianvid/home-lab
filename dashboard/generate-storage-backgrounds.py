#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 960, 376
BG, CARD, LINE = "#08111f", "#101d30", "#24344c"
TEXT, MUTED = "#edf4ff", "#8fa3bd"
BLUE, TEAL = "#62a8ff", "#48d7c8"
HERE = Path(__file__).resolve().parent


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


def render(filename: str, title: str, accent: str, labels=None) -> None:
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)
    draw.text((28, 18), title, font=font(26, True), fill=TEXT)
    draw.line((28, 58, 932, 58), fill=LINE, width=2)
    boxes = [
        (28, 76, 245, 188), (258, 76, 475, 188),
        (488, 76, 705, 188), (718, 76, 932, 188),
        (28, 200, 245, 312), (258, 200, 475, 312),
        (488, 200, 705, 312), (718, 200, 932, 312),
    ]
    labels = labels or [
        "TEMPERATURE", "SPACE USED", "SMART", "WEAR",
        "DATA WRITTEN", "POWER-ON", "AVL / CAP", "MEDIA ERRORS",
    ]
    for box, label in zip(boxes, labels):
        draw.rounded_rectangle(box, radius=14, fill=CARD, outline=LINE, width=2)
        draw.text((box[0] + 14, box[1] + 10), label,
                  font=font(22, True), fill=accent)
    draw.text((932, 344), "HOLD  ·  BACK", font=font(26, True),
              fill=accent, anchor="ra")
    image.save(HERE / "assets" / filename)


render("lexar.png", "STORAGE  /  LEXAR NM790", BLUE)
render("lexar2.png", "STORAGE  /  LEXAR 2", BLUE)
render("corsair.png", "STORAGE  /  CORSAIR EX400U USB4", TEAL)
render(
    "external-device.png",
    "STORAGE  /  EXTERNAL SATA",
    TEAL,
    [
        "TEMPERATURE", "SPACE USED", "SMART", "CONNECTION",
        "POWER-ON", "FIRMWARE", "AVL / CAP", "REALLOC / PEND / UNC",
    ],
)
