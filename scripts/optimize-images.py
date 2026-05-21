#!/usr/bin/env python3
"""
Resize all JPGs in Assets/ to max 1200px wide (preserving aspect) and re-encode
at q82 progressive in place. Also emit a WebP twin at q80. Resize Logo.png to
a small navbar variant. Records original vs new size to optimize-report.txt.

Run from the project root:
  python3 scripts/optimize-images.py
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageOps

ASSETS = Path(__file__).resolve().parent.parent / "Assets"
MAX_WIDTH = 1200
JPEG_QUALITY = 82
WEBP_QUALITY = 80


def fmt_kib(n: int) -> str:
    return f"{n / 1024:.1f} KiB"


def process_jpg(path: Path) -> tuple[int, int, int, int]:
    original_bytes = path.stat().st_size
    with Image.open(path) as img:
        img = ImageOps.exif_transpose(img)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        w, h = img.size
        if w > MAX_WIDTH:
            new_h = int(h * MAX_WIDTH / w)
            img = img.resize((MAX_WIDTH, new_h), Image.LANCZOS)
        new_w, new_h = img.size

        img.save(
            path,
            "JPEG",
            quality=JPEG_QUALITY,
            optimize=True,
            progressive=True,
        )

        webp_path = path.with_suffix(".webp")
        img.save(webp_path, "WEBP", quality=WEBP_QUALITY, method=6)
        webp_bytes = webp_path.stat().st_size

    new_bytes = path.stat().st_size
    return original_bytes, new_bytes, webp_bytes, new_w


def process_logo() -> tuple[int, int]:
    logo = ASSETS / "Logo.png"
    if not logo.exists():
        return 0, 0
    original_bytes = logo.stat().st_size
    small = ASSETS / "Logo-small.png"
    small_webp = ASSETS / "Logo-small.webp"
    with Image.open(logo) as img:
        img = ImageOps.exif_transpose(img)
        # Display size on mobile is 90x56; emit a 200x125 variant for crisp 2x DPI.
        target_w = 200
        w, h = img.size
        new_h = int(h * target_w / w)
        small_img = img.resize((target_w, new_h), Image.LANCZOS)
        small_img.save(small, "PNG", optimize=True)
        small_img_rgba = small_img if small_img.mode == "RGBA" else small_img.convert("RGBA")
        small_img_rgba.save(small_webp, "WEBP", quality=90, method=6)
    return original_bytes, small.stat().st_size


def main() -> int:
    if not ASSETS.exists():
        print(f"Assets folder not found at {ASSETS}", file=sys.stderr)
        return 1

    jpgs = sorted(ASSETS.glob("*.jpg"))
    print(f"Found {len(jpgs)} JPGs in {ASSETS}")
    print()

    total_before = 0
    total_after_jpg = 0
    total_webp = 0
    rows: list[tuple[str, int, int, int, int]] = []

    for path in jpgs:
        before, after, webp, w = process_jpg(path)
        total_before += before
        total_after_jpg += after
        total_webp += webp
        rows.append((path.name, before, after, webp, w))

    print(f"{'File':<46} {'Before':>12} {'After JPG':>12} {'WebP':>10} {'W':>5}")
    print("-" * 95)
    for name, before, after, webp, w in rows:
        print(f"{name:<46} {fmt_kib(before):>12} {fmt_kib(after):>12} {fmt_kib(webp):>10} {w:>5}")
    print("-" * 95)
    print(
        f"{'TOTAL':<46} {fmt_kib(total_before):>12} {fmt_kib(total_after_jpg):>12} {fmt_kib(total_webp):>10}"
    )
    saved_jpg = total_before - total_after_jpg
    saved_webp = total_before - total_webp
    print()
    print(f"JPG-only savings:  {fmt_kib(saved_jpg)} ({saved_jpg / total_before * 100:.1f}%)")
    print(f"WebP-vs-original:  {fmt_kib(saved_webp)} ({saved_webp / total_before * 100:.1f}%)")
    print()

    logo_before, logo_after = process_logo()
    if logo_before:
        print(f"Logo.png:          {fmt_kib(logo_before)}  ->  Logo-small.png {fmt_kib(logo_after)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
