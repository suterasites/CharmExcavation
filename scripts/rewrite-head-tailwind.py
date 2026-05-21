#!/usr/bin/env python3
"""
Replace the Tailwind CDN script + Google Fonts external requests + inline
tailwind.config <script> block across all HTML files with a single static
stylesheet link.

Run from the project root:
  python3 scripts/rewrite-head-tailwind.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML_GLOBS = ["*.html", "services/*.html", "projects/*.html"]

# Match from <script src="https://cdn.tailwindcss.com"...></script> through
# the closing </script> of the tailwind.config inline script. Captures the
# Google Fonts preconnect + stylesheet links that sit between them.
PATTERN = re.compile(
    r'<script\s+src="https://cdn\.tailwindcss\.com"[^>]*></script>'
    r'.*?'
    r'<script>\s*tailwind\.config\s*=\s*\{.*?\}\s*;?\s*</script>',
    re.DOTALL,
)

REPLACEMENT = '<link rel="stylesheet" href="/styles.css">'


def process_file(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    new_content, n = PATTERN.subn(REPLACEMENT, content)
    if n == 0:
        return False
    if n > 1:
        print(f"WARN: matched {n} times in {path}", file=sys.stderr)
    path.write_text(new_content, encoding="utf-8")
    return True


def main() -> int:
    files: list[Path] = []
    for pattern in HTML_GLOBS:
        files.extend(sorted(ROOT.glob(pattern)))
    touched = 0
    for path in files:
        ok = process_file(path)
        marker = "rewritten" if ok else "skipped (no match)"
        print(f"  {str(path.relative_to(ROOT)):<55} {marker}")
        if ok:
            touched += 1
    print(f"\n{touched}/{len(files)} files rewritten")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
