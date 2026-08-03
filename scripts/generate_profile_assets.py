#!/usr/bin/env python3
"""Generate portfolio banners from project screenshots."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

PROJECTS = [
    ("CHIPFASTENERS", ASSETS / "chipfasteners/portfolio-cover.png"),
    ("ICPROM", ASSETS / "icprom/portfolio-cover.jpg"),
    ("ELVN", ASSETS / "elvn/portfolio-cover.png"),
    ("ARMSENS ACADEMY", ASSETS / "armsens-academy/portfolio-cover.png"),
    ("PETERHOFAPART", ASSETS / "peterhofapart/portfolio-cover.png"),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def background(size: tuple[int, int]) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size, "#08110f")
    draw = ImageDraw.Draw(image)
    for x in range(0, width, max(64, width // 20)):
        draw.line((x, 0, x, height), fill="#12231f", width=1)
    for y in range(0, height, max(64, height // 10)):
        draw.line((0, y, width, y), fill="#12231f", width=1)
    draw.ellipse((width * 0.35, -height * 0.8, width * 1.15, height * 1.1), fill="#0b2520")
    return image


def fit_image(source: Path, size: tuple[int, int]) -> Image.Image:
    image = Image.open(source).convert("RGB")
    image.thumbnail(size, Image.Resampling.LANCZOS)
    frame = Image.new("RGB", size, "#111b19")
    frame.paste(image, ((size[0] - image.width) // 2, (size[1] - image.height) // 2))
    return frame


def card(canvas: Image.Image, label: str, source: Path, box: tuple[int, int, int, int], scale: float) -> None:
    draw = ImageDraw.Draw(canvas)
    x, y, width, height = box
    label_height = max(24, int(30 * scale))
    draw.rounded_rectangle((x, y, x + width, y + height), radius=max(8, int(12 * scale)), fill="#111917", outline="#49645d", width=max(1, int(2 * scale)))
    shot = fit_image(source, (width - int(12 * scale), height - label_height - int(12 * scale)))
    canvas.paste(shot, (x + int(6 * scale), y + label_height))
    draw.text((x + int(10 * scale), y + int(6 * scale)), label, font=font(max(10, int(12 * scale)), True), fill="#d8e3df")


def render_social() -> None:
    canvas = background((1280, 640))
    draw = ImageDraw.Draw(canvas)
    draw.text((58, 78), "Vitalii Kutepov", font=font(52, True), fill="#f4f7f6")
    draw.text((60, 145), "Senior Full-Stack Developer", font=font(24, True), fill="#7ee0bf")
    for index, line in enumerate(("High-Performance Web Platforms", "B2B Systems", "Product Engineering")):
        draw.text((60, 225 + index * 48), line, font=font(24, index == 0), fill="#f4f7f6")
    draw.text((60, 494), "Next.js   React   TypeScript   PHP   Docker   Nginx", font=font(15), fill="#adc0ba")
    positions = [(500, 42, 230, 250), (744, 42, 230, 250), (988, 42, 230, 250), (620, 314, 278, 250), (912, 314, 278, 250)]
    for (label, source), box in zip(PROJECTS, positions):
        card(canvas, label, source, box, 1.0)
    canvas.save(ASSETS / "profile/social-preview.png", optimize=True)


def render_github_cover() -> None:
    canvas = background((1280, 320))
    draw = ImageDraw.Draw(canvas)
    draw.text((48, 54), "Vitalii Kutepov", font=font(43, True), fill="#f4f7f6")
    draw.text((50, 116), "Senior Full-Stack Developer", font=font(23, True), fill="#7ee0bf")
    draw.text((50, 168), "High-Performance Web Platforms  ·  B2B Systems  ·  Product Engineering", font=font(17), fill="#d8e3df")
    positions = [(720, 25, 160, 255), (892, 25, 160, 255), (1064, 25, 160, 255)]
    for (label, source), box in zip(PROJECTS[:3], positions):
        card(canvas, label, source, box, 0.8)
    canvas.save(ASSETS / "profile/github-profile-cover.png", optimize=True)


def render_contra() -> None:
    canvas = background((2560, 1440))
    draw = ImageDraw.Draw(canvas)
    draw.text((120, 200), "Vitalii Kutepov", font=font(112, True), fill="#f4f7f6")
    draw.text((124, 345), "Senior Full-Stack Developer", font=font(52, True), fill="#7ee0bf")
    draw.text((124, 500), "High-Performance Web Platforms", font=font(50, True), fill="#f4f7f6")
    draw.text((124, 578), "B2B Systems", font=font(50), fill="#f4f7f6")
    draw.text((124, 656), "Product Engineering", font=font(50), fill="#f4f7f6")
    draw.text((124, 1200), "Next.js   React   TypeScript   PHP   Docker   Nginx", font=font(30), fill="#adc0ba")
    positions = [(1030, 100, 420, 520), (1480, 100, 420, 520), (1930, 100, 420, 520), (1260, 690, 500, 520), (1790, 690, 500, 520)]
    for (label, source), box in zip(PROJECTS, positions):
        card(canvas, label, source, box, 1.6)
    canvas.save(ASSETS / "profile/contra-cover.png", optimize=True)


if __name__ == "__main__":
    render_social()
    render_github_cover()
    render_contra()
