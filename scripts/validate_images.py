#!/usr/bin/env python3
"""Validate local Markdown image references and repository image files."""

from __future__ import annotations

import re
import struct
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IMAGE_REF = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
ALLOWED_SUFFIXES = {".png", ".webp", ".jpg", ".jpeg"}


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        signature = handle.read(24)
    if len(signature) != 24 or signature[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("invalid PNG signature")
    return struct.unpack(">II", signature[16:24])


errors: list[str] = []
referenced: set[Path] = set()

for markdown in ROOT.rglob("*.md"):
    if ".git" in markdown.parts:
        continue
    text = markdown.read_text(encoding="utf-8")
    for match in IMAGE_REF.finditer(text):
        target = match.group(1).split("#", 1)[0].strip("<>")
        if target.startswith(("http://", "https://", "data:")):
            continue
        path = (markdown.parent / target).resolve()
        referenced.add(path)
        if not path.is_relative_to(ROOT):
            errors.append(f"{markdown.relative_to(ROOT)}: image escapes repository: {target}")
        elif not path.is_file():
            errors.append(f"{markdown.relative_to(ROOT)}: missing image: {target}")

for image in (ROOT / "assets").rglob("*"):
    if not image.is_file():
        continue
    if image.suffix.lower() not in ALLOWED_SUFFIXES:
        errors.append(f"unsupported image format: {image.relative_to(ROOT)}")
        continue
    if image.stat().st_size == 0:
        errors.append(f"empty image: {image.relative_to(ROOT)}")
    if image.suffix.lower() == ".png":
        try:
            width, height = png_size(image)
            if width < 320 or height < 240:
                errors.append(f"image is too small for portfolio review: {image.relative_to(ROOT)} ({width}x{height})")
        except ValueError as exc:
            errors.append(f"{image.relative_to(ROOT)}: {exc}")

if errors:
    print("Image validation failed:", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"Validated {len(referenced)} local Markdown image references.")

