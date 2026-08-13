#!/usr/bin/env python3
"""Generate GPU backgrounds and keep main-panel numbering/config in sync."""

import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
CONFIG = HERE / "config" / "dashboard.json"
W, H = 960, 376
BG, CARD, LINE = "#08111f", "#101d30", "#24344c"
TEXT, MUTED, BLUE, TEAL = "#edf4ff", "#8fa3bd", "#62a8ff", "#48d7c8"


def font(size, bold=False):
    names = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for name in names:
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    raise FileNotFoundError("DejaVu Sans or Arial is required")


def background(path, title, page, labels, detail=False):
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)
    draw.text((28, 18), title, font=font(26, True), fill=TEXT)
    if page:
        draw.text((930, 21), page, font=font(22, True), fill=MUTED, anchor="ra")
    draw.line((28, 58, 932, 58), fill=LINE, width=2)
    boxes = [
        (28, 76, 245, 188), (258, 76, 475, 188), (488, 76, 705, 188), (718, 76, 932, 188),
        (28, 200, 245, 312), (258, 200, 475, 312), (488, 200, 705, 312), (718, 200, 932, 312),
    ]
    for box, label in zip(boxes, labels):
        draw.rounded_rectangle(box, radius=14, fill=CARD, outline=LINE, width=2)
        draw.text((box[0] + 14, box[1] + 10), label, font=font(21, True), fill=TEAL if detail else BLUE)
    if detail:
        draw.text((932, 344), "HOLD  ·  BACK", font=font(26, True), fill=TEAL, anchor="ra")
    else:
        draw.text((932, 344), "HOLD  ·  DETAILS", font=font(26, True), fill=TEAL, anchor="ra")
    image.save(path)


def sensor(name, x, y, size=28, unit="", color=TEXT):
    return {
        "mode": 1, "type": 1, "name": name, "label": name,
        "x": x, "y": y, "width": 0, "height": 0,
        "textDirection": 0, "direction": 1, "value": "0",
        "fontFamily": "DejaVuSans", "fontSize": size, "fontColor": color,
        "fontWeight": "normal", "textAlign": "center",
        "integerDigits": -1, "decimalDigits": -1, "unit": unit,
        "minAngle": 0, "maxAngle": 180, "minValue": 0, "maxValue": 100,
        "pic": "", "xz_x": 0, "xz_y": 0,
    }


background(ASSETS / "gpu.png", "HOME LAB  /  GPU", "3/6",
           ["TEMPERATURE", "GPU LOAD", "VRAM (MiB)", "POWER (W)",
            "FAN", "TOP CUDA PROCESS", "DCGM", "HEALTH"])
background(ASSETS / "gpu-details.png", "GPU DETAILS", "",
           ["DRIVER / CUDA", "P-STATE", "GPU CLOCK", "MEM CLOCK",
            "PERSISTENCE", "ECC", "ECC ERRORS (C / U)", "XID ERRORS"], detail=True)

data = json.loads(CONFIG.read_text())
data["diy"] = [p for p in data["diy"] if p["name"] not in {"GPU", "GPU > Details"}]
actions = [p for p in data["diy"] if p["name"].startswith("System Actions")]
data["diy"] = [p for p in data["diy"] if not p["name"].startswith("System Actions")]

gpu = {
    "name": "GPU", "img": "img/gpu.png",
    "sensor": [
        sensor("lab_nvidia_name", 600, 34, 20),
        sensor("lab_nvidia_temp", 136, 132, 32, "°C"), sensor("lab_nvidia_util", 366, 132, 32, "%"),
        sensor("lab_nvidia_vram", 596, 132, 25), sensor("lab_nvidia_power", 825, 132, 25),
        sensor("lab_nvidia_fan", 136, 256, 30, "%"), sensor("lab_nvidia_process", 366, 256, 22),
        sensor("lab_nvidia_dcgm", 596, 256, 30),
        sensor("lab_nvidia_ok", 825, 256, 30, color="#48d7c8"),
        sensor("lab_nvidia_warning", 825, 256, 30, color="#ffad42"),
        sensor("lab_nvidia_critical", 825, 256, 30, color="#ff626f"),
    ],
}
details = {
    "name": "GPU > Details", "img": "img/gpu-details.png",
    "sensor": [
        sensor("lab_nvidia_driver_cuda", 136, 132, 24), sensor("lab_nvidia_pstate", 366, 132, 30),
        sensor("lab_nvidia_clock", 596, 132, 28, " MHz"), sensor("lab_nvidia_mem_clock", 825, 132, 28, " MHz"),
        sensor("lab_nvidia_persistence", 136, 256, 27), sensor("lab_nvidia_ecc", 366, 256, 27),
        sensor("lab_nvidia_ecc_errors", 596, 256, 28), sensor("lab_nvidia_xid", 825, 256, 30),
    ],
}
data["diy"].extend([gpu, details, *actions])
by_name = {panel["name"]: index for index, panel in enumerate(data["diy"], 1)}
data["mianban"] = [by_name[name] for name in ("Health", "Compute", "GPU", "Storage", "Network", "Services")]
CONFIG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

# Page counters are part of the static artwork.
page_numbers = {"health.png": "1/6", "compute.png": "2/6", "network.png": "5/6", "services.png": "6/6"}
page_numbers.update({path.name: "4/6" for path in ASSETS.glob("storage-??.png")})
for filename, page in page_numbers.items():
    path = ASSETS / filename
    image = Image.open(path).convert("RGB")
    draw = ImageDraw.Draw(image)
    draw.rectangle((865, 10, 950, 56), fill=BG)
    draw.text((930, 21), page, font=font(22, True), fill=MUTED, anchor="ra")
    image.save(path)

print(CONFIG)
