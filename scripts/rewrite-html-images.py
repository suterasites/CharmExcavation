#!/usr/bin/env python3
"""
Rewrite <img> tags across the site to point at WebP twins and inject explicit
width/height attributes based on the actual source dimensions. Leaves
Open Graph / Twitter meta tags untouched (those still reference JPGs for
broader social platform compatibility).

Run from the project root:
  python3 scripts/rewrite-html-images.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "Assets"
HTML_GLOBS = ["*.html", "services/*.html", "projects/*.html"]

# Pre-compute dimensions for every image we might reference.
DIMENSIONS: dict[str, tuple[int, int]] = {}
for path in list(ASSETS.glob("*.jpg")) + list(ASSETS.glob("*.png")) + list(ASSETS.glob("*.webp")):
    try:
        with Image.open(path) as img:
            DIMENSIONS[path.name] = img.size
    except Exception:
        pass


# Match <img ... > tags. Non-greedy.
IMG_RE = re.compile(r"<img\b([^>]*?)/?>", re.IGNORECASE)
SRC_RE = re.compile(r'src\s*=\s*"([^"]*)"', re.IGNORECASE)
ATTR_WIDTH_RE = re.compile(r'\swidth\s*=\s*"[^"]*"', re.IGNORECASE)
ATTR_HEIGHT_RE = re.compile(r'\sheight\s*=\s*"[^"]*"', re.IGNORECASE)


def rewrite_img_tag(tag_text: str) -> str:
    """Mutate one <img ...> tag: jpg→webp, add width/height, swap Logo.png to Logo-small.png."""
    m = SRC_RE.search(tag_text)
    if not m:
        return tag_text
    src = m.group(1)

    # Strip width/height first; we will re-add canonical values.
    inner = ATTR_WIDTH_RE.sub("", tag_text)
    inner = ATTR_HEIGHT_RE.sub("", inner)

    new_src = src
    asset_name = None

    # Swap Logo.png references for the small navbar variant.
    # The footer/about page uses Logo-Stacked.svg which is fine (SVG is small).
    if src.endswith("/Assets/Logo.png") or src.endswith("Assets/Logo.png"):
        new_src = src.replace("Logo.png", "Logo-small.png")
        asset_name = "Logo-small.png"
    elif src.lower().endswith(".jpg") and "/Assets/" in src:
        new_src = src[:-4] + ".webp"
        asset_name = Path(new_src).name
    elif src.lower().endswith(".jpg") and "Assets/" in src:
        new_src = src[:-4] + ".webp"
        asset_name = Path(new_src).name

    inner = inner.replace(f'src="{src}"', f'src="{new_src}"')

    # Inject width/height after the src attribute.
    if asset_name and asset_name in DIMENSIONS:
        w, h = DIMENSIONS[asset_name]
        dim_attrs = f' width="{w}" height="{h}"'
        # Place dims right after src=
        new_src_attr = f'src="{new_src}"'
        if new_src_attr in inner and dim_attrs not in inner:
            inner = inner.replace(new_src_attr, new_src_attr + dim_attrs, 1)

    return inner


def process_file(path: Path) -> int:
    content = path.read_text(encoding="utf-8")
    new_content = IMG_RE.sub(lambda m: rewrite_img_tag(m.group(0)), content)
    if new_content != content:
        path.write_text(new_content, encoding="utf-8")
        # Count how many img tags were touched.
        return len(IMG_RE.findall(content))
    return 0


def main() -> int:
    files: list[Path] = []
    for pattern in HTML_GLOBS:
        files.extend(sorted(ROOT.glob(pattern)))
    print(f"Processing {len(files)} HTML files")
    for path in files:
        n = process_file(path)
        rel = path.relative_to(ROOT)
        print(f"  {str(rel):<60} {n if n else '-':>4} <img> tags scanned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
