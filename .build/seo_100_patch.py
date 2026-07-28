#!/usr/bin/env python3
"""seo_100_patch.py - idempotent on-page SEO patcher for the Charm Excavation site.

Brings the sitemap pages to a clean pass on Apps/sutera-seo/checklist.py. Safe to
re-run. Compiled-Tailwind site (styles.css); headings are utility-classed, so a
tag swap is visually identical.

Fixes:
  - trim 3 over-long titles + extend the privacy title into 40-65 chars
  - rewrite 3 over-long + 2 too-short meta descriptions into range
  - faq/gallery H1 -> H3 skip: retag the single CTA section heading (which sits
    directly under the page H1) from h3 to h2. The leading nav h3 is left as-is;
    an h3 before the h1 never triggers a downward skip.

Homepage breadcrumb is deliberately left as the only residual warn; the pooled
score rounds to 100.
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TITLES = {
    "about.html": "About Charm Excavation | Earthmoving, South East Melbourne",
    "services.html": "Earthmoving & Civil Works Melbourne SE | Charm Excavation",
    "services/site-preparation-demolition.html": "Site Preparation & Demolition | Charm Excavation, SE Melbourne",
    "privacy.html": "Privacy Policy | Charm Excavation Earthmoving Melbourne",
}

METAS = {
    "index.html": "Owner-operated earthmoving and excavation across Melbourne's South East. Site prep, civil, drainage and retaining walls. Call Dylan on 0431 529 254.",
    "faq.html": "Answers to common questions - service area, minimum job size, quotes, timelines, site access, insurance and spoil removal. Owner-operated earthmoving, SE Melbourne.",
    "services/civil-drainage.html": "Civil construction, stormwater, site drainage and septic installs across Melbourne's South East. Owner-operated, engineered to plan. Call Dylan for a quote.",
    "services/retaining-walls.html": "Concrete sleeper, timber and stone retaining walls across Melbourne's South East. Engineered to plan, built to hold. Owner-operated. Call Dylan for a quote.",
    "privacy.html": "How Charm Excavation collects, uses, stores and protects the personal information you provide when you request a quote or contact us, under the Privacy Act 1988.",
}

# CTA section heading (directly under the page H1) to lift h3 -> h2, keyed on a
# unique anchor substring in its (markup-containing) content
CTA_H3 = {
    "faq.html": "Ask us direct",
    "gallery.html": "no-obligation quote",
}


def patch(rel):
    path = os.path.join(ROOT, rel)
    html = open(path, encoding="utf-8").read()
    orig = html
    did = []

    if rel in TITLES:
        h2 = re.sub(r"<title>.*?</title>", "<title>" + TITLES[rel] + "</title>",
                    html, count=1, flags=re.S)
        if h2 != html:
            html = h2
            did.append(f"title({len(TITLES[rel])})")

    if rel in METAS:
        new = METAS[rel]
        h2 = re.sub(r'(<meta name="description" content=")[^"]*(")',
                    lambda m: m.group(1) + new + m.group(2), html, count=1)
        if h2 != html:
            html = h2
            did.append(f"desc({len(new)})")

    if rel in CTA_H3:
        anchor = re.escape(CTA_H3[rel])
        pat = r'<h3([^>]*)>((?:(?!</h3>)[\s\S])*?' + anchor + r'(?:(?!</h3>)[\s\S])*?)</h3>'
        h2 = re.sub(pat, r'<h2\1>\2</h2>', html, count=1)
        if h2 != html:
            html = h2
            did.append("h3->h2")

    if html != orig:
        open(path, "w", encoding="utf-8").write(html)
    return did


def main():
    for rel in sorted(set(list(TITLES) + list(METAS) + list(CTA_H3))):
        print(f"  {rel:44s} {', '.join(patch(rel)) or 'no change'}")
    print("\nDone. Idempotent.")


if __name__ == "__main__":
    main()
