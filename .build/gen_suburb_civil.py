#!/usr/bin/env python3
"""gen_suburb_civil.py - build Civil & Drainage x suburb landing pages.

Sibling of gen_suburb_excavation.py, same method: clone the service-level page
(services/civil-drainage.html) - keeping its header, footer, scripts, styles and
the generic service sections (capabilities, recent work, other services, CTA)
verbatim - then localise the head/schema, hero and overview, and add a suburb FAQ
(with FAQPage schema) plus an "Areas we service" mesh-linking section. Also patches
the parent service page with the same Areas section so the cluster is crawlable
from the hub, and adds every page to sitemap.xml.

Idempotent: re-running overwrites the generated pages, re-inserts the Areas section
on the parent only if missing, and skips sitemap URLs already listed. Output:
services/civil-drainage-<suburb>.html

House note: compiled-Tailwind site (styles.css). Only utility classes already in
the base page are reused; the Areas/FAQ blocks lean on the page's own scoped
classes (sub-card etc.), so nothing new needs compiling.

Coverage note: the filename must carry the clients.yaml term for this service
("drainage") plus the suburb slug, or Apps/seo-hq's coverage matrix will not
count the page. civil-drainage-<suburb> satisfies both.
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICES = os.path.join(ROOT, "services")
BASE = "https://charmexcavation.com.au"
PARENT = os.path.join(SERVICES, "civil-drainage.html")
SITEMAP = os.path.join(ROOT, "sitemap.xml")
LASTMOD = "2026-08-17"

# ── Per-suburb data ────────────────────────────────────────────────────────
# name/slug + localised copy. No fabricated past-project claims - framed as
# service-area capability + genuine local ground conditions and job types.
SUBURBS = [
    {
        "slug": "dandenong", "name": "Dandenong",
        "meta": "Civil works and drainage in Dandenong, SE Melbourne. Stormwater, pits, trenching, septic and crossovers, dug to plan and backfilled clean. Call 0431 529 254.",
        "hero": "From backyard stormwater on Dandenong's older blocks to industrial drainage runs down in Dandenong South, we dig to the plan and backfill clean.",
        "ov1": "Dandenong covers the full range of drainage work - stormwater pit and pipe on established residential blocks, through to bigger civil runs, yard drainage and crossovers across the commercial and industrial pockets.",
        "ov2": "We are based minutes away in Keysborough, so we can get onto a Dandenong job quickly, work to the engineer's levels, and leave the run compacted and tidy.",
        "local": "Much of Dandenong's older housing sits on reactive clay, which holds water rather than letting it soak away. That makes the fall, the pipe bedding and proper compaction the difference between a drain that works and one that surcharges in the first heavy storm.",
        "faqs": [
            ("Do you install stormwater drainage in Dandenong?", "Yes. Stormwater pipe and pit runs, trenching, the connection to your legal point of discharge and the backfill behind it are core work for us across Dandenong, Dandenong North and Dandenong South."),
            ("Can you do civil works on a commercial or industrial site?", "We can. Crossovers, verge cuts, industrial access and site drainage on commercial blocks are part of our civil scope, and we work in with the site manager so we are in and out without holding the build up."),
            ("How do you handle the clay ground around Dandenong?", "Carefully. Reactive clay does not drain on its own, so we cut the trench to the right fall, bed and surround the pipe properly and compact as we backfill, so the run does not settle or block later."),
        ],
    },
    {
        "slug": "cranbourne", "name": "Cranbourne",
        "meta": "Civil and drainage in Cranbourne. Stormwater, pits, agi drains and tank trenching for new estate builds, set out to plan. Owner-operated. Call 0431 529 254.",
        "hero": "Cranbourne's new estates need the drainage in before anything else goes up - stormwater runs, pits, agi lines and tank trenching, all set out to plan.",
        "ov1": "Across Cranbourne, Cranbourne West, East and North the work is mostly new-build drainage: stormwater pipe and pits, agricultural drains, service trenching and the excavation for detention or rainwater tanks on tight estate lots.",
        "ov2": "We set out off the drainage plan, dig to the fall, lay and backfill, then get off the block so the slab and the trades behind us are not left waiting.",
        "local": "Estate blocks around Cranbourne often run sand over clay, so water moves through the topsoil and then stops. Getting the depth, the fall and the pipe surround right is what keeps the yard dry once the landscaping goes in on top.",
        "faqs": [
            ("Do you do drainage for new builds in the Cranbourne estates?", "Yes. Stormwater, pits, agi drains and service trenching on new house-and-land blocks are everyday work for us across Cranbourne and the growth estates around it."),
            ("Can you dig for a detention or rainwater tank?", "We can. Tank excavation and the trenching that ties it into the stormwater run is part of the job, dug to the plan and backfilled properly."),
            ("How quickly can you get to a Cranbourne site?", "We are a short run from our Keysborough base, so we can usually slot Cranbourne jobs in around your build programme without a long wait."),
        ],
    },
    {
        "slug": "berwick", "name": "Berwick",
        "meta": "Civil and drainage in Berwick - stormwater, agi and subsoil drains, and runoff control on sloping hillside blocks. Owner-operated. Call 0431 529 254.",
        "hero": "Berwick's hills move water fast, so drainage here is about catching the runoff and getting it away before it finds its way under a slab.",
        "ov1": "Berwick mixes established homes with premium builds on sloping ground. That means surface runoff to control, agi drains behind retaining walls, stormwater runs following a fall, and getting water to the discharge point rather than into the neighbour's yard.",
        "ov2": "We plan the run around the fall of the block, dig to line and level, then lay, backfill and compact so nothing washes out the first time it rains hard.",
        "local": "On a sloping Berwick block, water is the thing that undoes the job. Subsoil drainage behind a retaining wall, a cut-off drain above the pad and a properly fallen stormwater run are what keep the ground stable and the wall standing.",
        "faqs": [
            ("Do you install agi and subsoil drains behind retaining walls in Berwick?", "Yes. On sloping Berwick blocks that drainage is what stops a wall failing, so the agi line, the aggregate behind it and the outlet all go in as part of the job."),
            ("Can you fix runoff coming down onto my block?", "Often, yes. A cut-off drain above the pad, sensible surface grading and a properly fallen stormwater run are the usual answer to water coming off higher ground."),
            ("Do you cover Berwick and Beaconsfield?", "We do. Berwick, Beaconsfield, Harkaway and the surrounding pockets are all part of our South East Melbourne service area."),
        ],
    },
    {
        "slug": "narre-warren", "name": "Narre Warren",
        "meta": "Civil and drainage in Narre Warren - backyard stormwater, agi drains, pits and side-access trenching on family blocks. Call Dylan on 0431 529 254.",
        "hero": "Soggy backyards, tired old runs and new stormwater for extensions and sheds - Narre Warren drainage on standard family blocks.",
        "ov1": "Narre Warren is established family housing, so the drainage work is backyard stormwater, agi lines through wet lawn, new pits, and runs for extensions, sheds and granny flats that need connecting back into the existing system.",
        "ov2": "We run compact machines that fit down a standard side gate, trench without wrecking the yard on the way through, and reinstate behind us as we go.",
        "local": "The usual Narre Warren job is water sitting in the back corner of a flat block long after the rain has stopped. That is a fall and a discharge-point problem, and it is fixed with an agi line and a pit run taken somewhere the water can actually get away.",
        "faqs": [
            ("Can you get a machine into my Narre Warren backyard?", "Usually yes. Our compact excavator is built for standard side-gate access, so most backyard drainage jobs are no trouble."),
            ("Why does my backyard hold water after rain?", "Most of the time it is a lack of fall, or nowhere for the water to discharge to. An agi drain and a stormwater run taken to a legal discharge point is the normal fix."),
            ("Do you cover Narre Warren South and North?", "Yes. Narre Warren, Narre Warren South, Narre Warren North and the Fountain Gate area are all part of our regular run."),
        ],
    },
    {
        "slug": "pakenham", "name": "Pakenham",
        "meta": "Civil and drainage in Pakenham - new-estate stormwater and pits, plus septic tank earthworks, table drains and culverts on rural blocks. Call 0431 529 254.",
        "hero": "Pakenham runs from new estates to acreage, so the drainage does too - stormwater and pits in town, septic earthworks, table drains and culverts out on the fringe.",
        "ov1": "In Pakenham's estates the work is new-build drainage: pit and pipe, agi lines, service trenching and tank excavation. Out on the rural blocks it shifts to septic tank and trench earthworks, table drains, culverts and getting water off an access track.",
        "ov2": "We bring the machine to suit, whether that is a tidy trench on an estate lot or a longer run across a paddock, and work to the plan either way.",
        "local": "Rural Pakenham blocks have to manage their own water and their own waste, so the earthworks have to be right the first time. In the estates it is the opposite problem: small lots, tight levels, and a discharge point that has to be hit exactly.",
        "faqs": [
            ("Do you do septic system earthworks on rural Pakenham properties?", "We do the excavation side - the tank hole, the trenching and the backfill that goes with a septic system on an acreage block, dug to the approved plan and left ready for the install."),
            ("Can you do table drains and culverts?", "Yes. Table drains, culvert pipes under an access track and general rural water management are all within our scope out on the Pakenham fringe."),
            ("Do you cover the Pakenham estates?", "Yes. Pakenham, Pakenham Upper, the Lakeside and Cardinia estates and the rural blocks around town are all in our service area."),
        ],
    },
    {
        "slug": "officer", "name": "Officer",
        "meta": "Civil and drainage in Officer - stormwater, pits, agi drains and crossover excavation for new estate builds, set out to plan. Call 0431 529 254.",
        "hero": "Officer's estates go up fast, and the drainage has to be in, connected and backfilled before the rest of the build can move.",
        "ov1": "Officer is largely new greenfield estates, so the work is new-build civil and drainage: stormwater pipe and pits, agi lines, service trenching, crossover excavation and tank holes on fresh blocks.",
        "ov2": "We work off the drainage plan, dig to the fall, connect to the discharge point and backfill compacted, so the block hands over ready for the next trade.",
        "local": "Greenfield blocks in Officer are a clean slate, which means the levels on the plan are the only thing to work to. Accurate setout and a properly compacted trench are what stop settlement showing up under a driveway a year later.",
        "faqs": [
            ("Do you service the new Officer estates?", "Yes. Officer and Officer South, including the newer estates, are part of our regular South East Melbourne run."),
            ("Can you do the stormwater for a new Officer build?", "That is core work for us out here - pit and pipe, agi drains and service trenching, set out off your plans and connected to the legal point of discharge."),
            ("Do you dig out driveway crossovers?", "We do the excavation and civil side of a crossover, cut to the levels your plan and the council require, ready for the concrete crew to follow."),
        ],
    },
    {
        "slug": "clyde", "name": "Clyde",
        "meta": "Civil and drainage in Clyde - stormwater, pits, agi drains and tank trenching on flat new estate blocks. Owner-operated, SE Melbourne. Call 0431 529 254.",
        "hero": "Clyde's flat, newly released blocks give water nowhere to go on its own, so the stormwater run has to do all of the work.",
        "ov1": "Clyde has gone from farmland to new estates in a few short years, and the drainage work has followed: stormwater pit and pipe, agi lines, service trenching and detention or rainwater tank excavation on new-build blocks.",
        "ov2": "We set out to the plan, hold the fall over the length of the run, and backfill and compact so nothing settles under the driveway or the slab.",
        "local": "Flat former-farmland blocks like Clyde's have very little natural fall, so every bit of grade in the pipe counts. Get it right and the yard drains on its own; get it lazy and the water just sits.",
        "faqs": [
            ("Do you cover the Clyde estates?", "Yes. Clyde and its newer estates are part of our core South East Melbourne service area."),
            ("Is your Clyde service any different to Clyde North?", "No. The two sit side by side in the growth corridor and we work right through both of them the same way."),
            ("Can you dig for a detention or water tank in Clyde?", "We can. Tank excavation and the trenching to tie it into the stormwater run is standard work for us on estate blocks out here."),
        ],
    },
    {
        "slug": "clyde-north", "name": "Clyde North",
        "meta": "Civil and drainage in Clyde North - fast, accurate stormwater, pits, agi drains and trenching for new estate builds. Owner-operated. Call 0431 529 254.",
        "hero": "Wall-to-wall new estates and tight build programmes - Clyde North drainage that goes in accurately and does not hold the job up.",
        "ov1": "Clyde North is one of the fastest-growing pockets in the state, and the drainage work runs at that pace: stormwater pit and pipe, agi drains, service trenches, crossover excavation and tank holes, block after block.",
        "ov2": "We come set up for estate work - in on time, dug to the plan, connected, backfilled and off, so the slab crew behind us is not left waiting.",
        "local": "With so many blocks going in at once, the pressure in Clyde North is turnaround without shortcuts. Accurate falls and proper compaction are the two things that will not forgive being rushed, so that is where the care goes.",
        "faqs": [
            ("Do you service all of Clyde North?", "Yes. Clyde North and its many new estates are a core part of our South East Melbourne service area."),
            ("Can you keep up with a tight new-build programme?", "That is what we are geared for - drainage in and backfilled to your dates, so the trades behind you can keep moving."),
            ("Do you do crossovers and driveway drainage?", "We do the excavation and civil side, cut to the levels on your plan and left ready for the concrete."),
        ],
    },
    {
        "slug": "frankston", "name": "Frankston",
        "meta": "Civil and drainage in Frankston - stormwater, agi drains and trenching on sandy bayside blocks and hillier ground inland. Call Dylan on 0431 529 254.",
        "hero": "Sandy near the bay, heavier ground inland - Frankston drainage is a different job depending on which side of town you are on.",
        "ov1": "Frankston runs from coastal blocks near the bay through to hillier ground inland, so the work spans stormwater and soakage on sand, agi drains through heavier clay, and runoff control on the sloping blocks behind town.",
        "ov2": "We read the ground first, then set the run up to suit it, because the depth, the fall, the pipe surround and the backfill all change with the soil.",
        "local": "Sandy coastal ground drains quickly but will not hold an open trench, while the firmer blocks inland hold water and need the fall taken seriously. Both turn up in Frankston, so we set the trench up for the soil in front of us rather than working to one recipe.",
        "faqs": [
            ("Do you cover Frankston South and Seaford?", "Yes. Frankston, Frankston South, Frankston North and Seaford are all within our service area."),
            ("Can you install drainage in sandy coastal ground?", "We can. Sandy trenches have to be dug and supported correctly and the pipe bedded so it cannot move, and that is something we plan for on every coastal job."),
            ("Do you handle runoff on Frankston's sloping blocks?", "Yes. A cut-off drain, a subsoil line and a properly fallen stormwater run are the usual answer to water coming down a slope, and that is routine work for us."),
        ],
    },
    {
        "slug": "hallam", "name": "Hallam",
        "meta": "Civil and drainage in Hallam - stormwater, pits, trenching and yard drainage across residential and light-industrial blocks. Call 0431 529 254.",
        "hero": "Residential stormwater through to light-industrial yard drainage - Hallam is on our doorstep and covered either way.",
        "ov1": "Hallam sits between Dandenong and Narre Warren and mixes established homes with light-industrial pockets, so the work runs from backyard stormwater and agi lines to yard drainage, swales and pit-and-pipe runs on commercial lots.",
        "ov2": "It is only minutes from our Keysborough base, so we can be on a Hallam job quickly with the right machine for the block.",
        "local": "A lot of Hallam sits low and flat, which means water hangs around rather than running off. On ground like that, the fall in the pipe and where the run actually discharges to matter more than anything else on the job.",
        "faqs": [
            ("Do you do commercial and industrial drainage in Hallam?", "Yes. Yard drainage, swales, pit-and-pipe runs and general site drainage on light-industrial lots are part of our civil scope."),
            ("Can you fix water pooling on a flat Hallam block?", "Usually. Pooling on flat ground comes down to fall and discharge point, and an agi and stormwater run set up properly is the normal fix."),
            ("How quickly can you get to a Hallam job?", "Very quickly. Hallam is right on our doorstep from Keysborough, so it is one of the fastest jobs for us to get to."),
        ],
    },
    {
        "slug": "hampton-park", "name": "Hampton Park",
        "meta": "Civil and drainage in Hampton Park - backyard stormwater, agi drains, pits and new runs for sheds and granny flats. Call Dylan on 0431 529 254.",
        "hero": "Backyard stormwater, agi drains and new runs for sheds, granny flats and extensions across Hampton Park's family blocks.",
        "ov1": "Hampton Park is settled suburban housing on mostly flat blocks, so the work is backyard drainage: agi lines through wet lawn, new pits, and stormwater runs for sheds, granny flats and extensions tying back into the existing system.",
        "ov2": "We bring a machine that fits through a standard side gate, protect the path on the way in, trench neatly and reinstate behind us.",
        "local": "On flat Hampton Park blocks the water has nowhere to go unless you give it somewhere. The fix is nearly always fall and a proper discharge point, not simply more pipe in the ground.",
        "faqs": [
            ("Do you cover Hampton Park?", "Yes. Hampton Park is a short drive from our Keysborough base and part of our regular South East Melbourne run."),
            ("Can you run drainage for a new shed or granny flat?", "We can. A new roofed structure needs its downpipes taken into the stormwater system, and we trench, lay and connect that run back into your existing pits."),
            ("Will a machine fit down the side of my house?", "Usually yes. Our compact excavator is sized for standard side-gate access, so most backyard drainage jobs are straightforward."),
        ],
    },
    {
        "slug": "endeavour-hills", "name": "Endeavour Hills",
        "meta": "Civil and drainage in Endeavour Hills - runoff control, agi drains behind retaining walls and stormwater runs on sloping blocks. Call 0431 529 254.",
        "hero": "Undulating ground means moving water, so Endeavour Hills drainage is about catching runoff up high and getting it away cleanly.",
        "ov1": "Endeavour Hills is built across undulating ground, so the work is runoff and subsoil drainage: agi lines behind retaining walls, cut-off drains above a pad, and stormwater runs that follow the fall down to a discharge point.",
        "ov2": "We plan the run with the slope rather than against it, dig to line and level, and backfill compacted so nothing washes out in the first heavy rain.",
        "local": "On a sloping block the drainage and the retaining are two halves of the one job. Water sitting behind a wall is what pushes it over, so the agi line, the aggregate and the outlet matter as much as the wall itself.",
        "faqs": [
            ("Do you install drainage behind retaining walls?", "Yes. Subsoil agi drainage, aggregate backfill and a proper outlet are standard on any retaining wall we are involved with, and they are what keep the wall standing."),
            ("Can you deal with runoff coming down onto my block?", "Often, yes. A cut-off drain above the pad and a stormwater run taken to a proper discharge point is the usual fix for water coming off higher ground."),
            ("Do you cover Endeavour Hills and Doveton?", "Yes. Endeavour Hills, Doveton and the surrounding pockets are all in our service area."),
        ],
    },
]

BY_SLUG = {s["slug"]: s for s in SUBURBS}


def rep(html, old, new, label, count=1):
    """Replace exactly `count` occurrences; raise if the anchor is missing."""
    n = html.count(old)
    if n < count:
        raise SystemExit(f"[{label}] anchor not found ({n} < {count}):\n  {old[:90]}...")
    return html.replace(old, new, count)


def strip_areas(html):
    """Remove an already-injected Areas section so a clean base can be re-cloned
    (keeps the generator idempotent whether or not the parent has been patched)."""
    m = '<section id="areas-we-service"'
    i = html.find(m)
    if i == -1:
        return html
    j = html.index('</section>', i) + len('</section>')
    if html[j:j + 1] == '\n':
        j += 1
    return html[:i] + html[j:]


def json_ld(sub):
    url = f"{BASE}/services/civil-drainage-{sub['slug']}.html"
    name = sub["name"]
    area = [
        {"@type": "City", "name": name},
        {"@type": "Place", "name": "South East Melbourne"},
    ]
    graph = [
        {
            "@type": "LocalBusiness",
            "@id": f"{BASE}/#business",
            "name": "Charm Excavation",
            "description": "Owner-operated earthmoving, excavation, civil, drainage, retaining walls, landscaping and rural earthworks across Melbourne's South East.",
            "image": f"{BASE}/Assets/Logo.png",
            "logo": f"{BASE}/Assets/Logo.png",
            "telephone": "+61431529254",
            "email": "Dylan@charmexcavation.com.au",
            "url": f"{BASE}/",
            "priceRange": "$$",
            "address": {"@type": "PostalAddress", "addressLocality": "Keysborough", "addressRegion": "VIC", "addressCountry": "AU"},
            "areaServed": [
                {"@type": "City", "name": "Keysborough"},
                {"@type": "City", "name": name},
                {"@type": "Place", "name": "South East Melbourne"},
            ],
            "sameAs": ["https://www.instagram.com/charmexcavation"],
        },
        {
            "@type": "Service",
            "serviceType": "Civil and Drainage",
            "name": f"Civil and Drainage in {name}",
            "url": url,
            "provider": {"@id": f"{BASE}/#business"},
            "areaServed": area,
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": f"Civil and Drainage Services in {name}",
                "itemListElement": [
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Civil Construction Services"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Drainage Installation"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Stormwater"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Site Drainage & Swales"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Septic Tank Earthworks"}},
                ],
            },
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": "Services", "item": f"{BASE}/services.html"},
                {"@type": "ListItem", "position": 3, "name": "Civil & Drainage", "item": f"{BASE}/services/civil-drainage.html"},
                {"@type": "ListItem", "position": 4, "name": name, "item": url},
            ],
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in sub["faqs"]
            ],
        },
    ]
    doc = {"@context": "https://schema.org", "@graph": graph}
    return '<script type="application/ld+json">\n' + json.dumps(doc, indent=2, ensure_ascii=False) + '\n</script>'


def faq_section(sub):
    cards = "\n".join(
        f'''      <article class="sub-card bg-char-900 rounded-sm overflow-hidden p-7">
        <h3 class="font-display text-xl uppercase text-cream leading-tight">{q}</h3>
        <p class="mt-3 text-sm text-cream/65 leading-relaxed">{a}</p>
      </article>'''
        for q, a in sub["faqs"]
    )
    return f'''<section id="faq" class="relative bg-char-950 overflow-hidden">
  <div class="max-w-7xl mx-auto px-6 lg:px-10 py-20 lg:py-24">
    <div class="max-w-2xl mb-12">
      <div class="flex items-center gap-3 mb-5"><span class="h-px w-10 bg-gold-400"></span><span class="font-sport text-xs tracking-[0.3em] uppercase text-gold-400">{sub['name']} questions</span></div>
      <h2 class="font-display text-4xl md:text-5xl uppercase leading-[0.92] text-cream">Common <span class="text-gold-400">questions.</span></h2>
    </div>
    <div class="grid md:grid-cols-3 gap-5 lg:gap-6">
{cards}
    </div>
  </div>
</section>
'''


def areas_section(active_slug=None):
    """Mesh-linking grid to every Civil & Drainage suburb page. The active suburb
    (on its own page) renders as a non-linked gold tile."""
    tiles = []
    for s in SUBURBS:
        href = f"/services/civil-drainage-{s['slug']}.html"
        if s["slug"] == active_slug:
            tiles.append(
                f'<span class="sub-card bg-char-900 rounded-sm px-5 py-4 font-sport text-sm tracking-[0.14em] uppercase text-gold-400 border-gold-400/40">{s["name"]}</span>'
            )
        else:
            tiles.append(
                f'<a href="{href}" class="sub-card bg-char-900 rounded-sm px-5 py-4 font-sport text-sm tracking-[0.14em] uppercase text-cream/80 hover:text-gold-400 block">{s["name"]}</a>'
            )
    grid = "\n      ".join(tiles)
    return f'''<section id="areas-we-service" class="relative bg-char-900 overflow-hidden">
  <div class="stripes h-3 w-full opacity-90"></div>
  <div class="max-w-7xl mx-auto px-6 lg:px-10 py-20 lg:py-24">
    <div class="max-w-2xl mb-10">
      <div class="flex items-center gap-3 mb-5"><span class="h-px w-10 bg-gold-400"></span><span class="font-sport text-xs tracking-[0.3em] uppercase text-gold-400">Where we work</span></div>
      <h2 class="font-display text-4xl md:text-5xl uppercase leading-[0.92] text-cream">Drainage across <span class="text-gold-400">South East Melbourne.</span></h2>
      <p class="mt-5 text-cream/70 leading-relaxed">Owner-operated civil and drainage from our Keysborough base. Pick your suburb for local detail, or call Dylan direct on <a href="tel:0431529254" class="text-gold-400 hover:text-gold-300 transition">0431 529 254</a>.</p>
    </div>
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3 lg:gap-4">
      {grid}
    </div>
  </div>
</section>
'''


# ── Build one suburb page ──────────────────────────────────────────────────
def build_page(sub):
    html = strip_areas(open(PARENT, encoding="utf-8").read())
    name = sub["name"]
    slug = sub["slug"]
    url = f"{BASE}/services/civil-drainage-{slug}.html"
    title = f"Civil Works & Drainage {name} | Charm Excavation"

    # Head lengths are audited (title 40-65, meta description 120-170 in
    # Apps/sutera-seo/checklist.py) - fail the build rather than ship a warn.
    if not 40 <= len(title) <= 65:
        raise SystemExit(f"[{slug}] title is {len(title)} chars (need 40-65): {title}")
    if not 120 <= len(sub["meta"]) <= 170:
        raise SystemExit(f"[{slug}] meta description is {len(sub['meta'])} chars (need 120-170)")

    # -- head --
    html = rep(html,
        "<title>Civil & Drainage - Charm Excavation, South East Melbourne</title>",
        f"<title>{title}</title>", "title")
    html = rep(html,
        '<meta name="description" content="Civil construction, stormwater, site drainage and septic installs across Melbourne\'s South East. Owner-operated, engineered to plan. Call Dylan for a quote." />',
        f'<meta name="description" content="{sub["meta"]}" />', "desc")
    html = rep(html,
        '<meta name="geo.placename" content="Melbourne">',
        f'<meta name="geo.placename" content="{name}">', "geo")
    html = rep(html,
        '<link rel="canonical" href="https://charmexcavation.com.au/services/civil-drainage.html">',
        f'<link rel="canonical" href="{url}">', "canonical")
    # open graph
    html = rep(html,
        '<meta property="og:title" content="Civil & Drainage - Charm Excavation, South East Melbourne">',
        f'<meta property="og:title" content="Civil & Drainage {name} - Charm Excavation">', "og:title")
    html = rep(html,
        '<meta property="og:description" content="Civil construction, stormwater, site drainage, septic installs and crossovers across Melbourne\'s South East. Built to the engineer\'s plan.">',
        f'<meta property="og:description" content="{sub["meta"]}">', "og:desc")
    html = rep(html,
        '<meta property="og:url" content="https://charmexcavation.com.au/services/civil-drainage.html">',
        f'<meta property="og:url" content="{url}">', "og:url")
    # twitter
    html = rep(html,
        '<meta name="twitter:title" content="Civil & Drainage - Charm Excavation, SE Melbourne">',
        f'<meta name="twitter:title" content="Civil & Drainage {name} - Charm Excavation">', "tw:title")
    html = rep(html,
        '<meta name="twitter:description" content="Civil works, stormwater, site drainage and septic installs across Melbourne\'s South East.">',
        f'<meta name="twitter:description" content="Civil works, stormwater and site drainage in {name}, South East Melbourne.">', "tw:desc")

    # -- json-ld: replace the first ld+json script block --
    ld_start = html.index('<script type="application/ld+json">')
    ld_end = html.index('</script>', ld_start) + len('</script>')
    html = html[:ld_start] + json_ld(sub) + html[ld_end:]

    # -- visible breadcrumb --
    html = rep(html,
        '''    <li><a href="/services.html" class="hover:text-gold-400">Services</a></li>
    <li aria-hidden="true">/</li>
    <li aria-current="page" class="text-cream/90">Civil & Drainage</li>''',
        f'''    <li><a href="/services.html" class="hover:text-gold-400">Services</a></li>
    <li aria-hidden="true">/</li>
    <li><a href="/services/civil-drainage.html" class="hover:text-gold-400">Civil & Drainage</a></li>
    <li aria-hidden="true">/</li>
    <li aria-current="page" class="text-cream/90">{name}</li>''', "breadcrumb")

    # -- hero eyebrow / label / h1 / paragraph --
    html = rep(html,
        '<div class="flex items-center gap-4 mb-6 text-xs font-sport tracking-[0.25em] uppercase text-cream/50"><a href="/services.html" class="hover:text-gold-400 transition">Services</a><span>/</span><span class="text-gold-400">Civil & Drainage</span></div>',
        f'<div class="flex items-center gap-4 mb-6 text-xs font-sport tracking-[0.25em] uppercase text-cream/50"><a href="/services/civil-drainage.html" class="hover:text-gold-400 transition">Civil & Drainage</a><span>/</span><span class="text-gold-400">{name}</span></div>', "hero-eyebrow")
    html = rep(html,
        '<span class="font-sport text-xs tracking-[0.3em] uppercase text-gold-400">Service</span>',
        f'<span class="font-sport text-xs tracking-[0.3em] uppercase text-gold-400">{name}, SE Melbourne</span>', "hero-label")
    html = rep(html,
        '<h1 class="font-display text-5xl md:text-6xl lg:text-[6rem] leading-[0.9] uppercase text-cream">Civil <br/>& <span class="text-gold-400">Drainage.</span></h1>',
        f'<h1 class="font-display text-5xl md:text-6xl lg:text-[6rem] leading-[0.9] uppercase text-cream">Civil & Drainage <br/>in <span class="text-gold-400">{name}.</span></h1>', "h1")
    html = rep(html,
        '<p class="mt-8 text-lg md:text-xl text-cream/80 max-w-2xl leading-relaxed">Civil works, stormwater and drainage runs. Built to plan, backfilled clean, signed off tidy.</p>',
        f'<p class="mt-8 text-lg md:text-xl text-cream/80 max-w-2xl leading-relaxed">{sub["hero"]}</p>', "hero-p")

    # -- overview heading + paragraphs (2 -> 3, incl local knowledge) --
    html = rep(html,
        '<h2 class="font-display text-4xl md:text-5xl uppercase leading-[0.92] text-cream">Clean lines. <br/><span class="text-burgundy-500">Tidy sign-off.</span></h2>',
        f'<h2 class="font-display text-4xl md:text-5xl uppercase leading-[0.92] text-cream">Drainage in <br/><span class="text-burgundy-500">{name}.</span></h2>', "ov-head")
    html = rep(html,
        '''        <p>Civil and drainage is less forgiving than most trades. Get a fall wrong and the whole run needs pulling up. We work to the engineer's plan, dig to the line, install, and backfill clean.</p>
        <p>Stormwater, swales, septic, crossovers, industrial runs - residential through to commercial pads. On the big jobs we coordinate with the site manager so we're in and out without holding up the programme.</p>''',
        f'''        <p>{sub["ov1"]}</p>
        <p>{sub["ov2"]}</p>
        <p>{sub["local"]}</p>''', "ov-body")

    # -- insert FAQ + Areas before the CTA section --
    cta = '<section class="relative bg-burgundy-800 overflow-hidden">'
    html = rep(html, cta, faq_section(sub) + "\n" + areas_section(slug) + "\n" + cta, "insert-faq-areas")

    out = os.path.join(SERVICES, f"civil-drainage-{slug}.html")
    open(out, "w", encoding="utf-8").write(html)
    return out


def patch_parent():
    """Add the Areas We Service mesh section to the hub service page (once)."""
    html = open(PARENT, encoding="utf-8").read()
    if 'id="areas-we-service"' in html:
        return "parent: areas section already present"
    cta = '<section class="relative bg-burgundy-800 overflow-hidden">'
    if html.count(cta) != 1:
        raise SystemExit("parent: CTA anchor not unique")
    html = html.replace(cta, areas_section(None) + "\n" + cta, 1)
    open(PARENT, "w", encoding="utf-8").write(html)
    return "parent: areas section inserted"


def patch_sitemap():
    """Add any missing suburb URLs, straight after the parent service entry."""
    xml = open(SITEMAP, encoding="utf-8").read()
    anchor = f"""  <url>
    <loc>{BASE}/services/civil-drainage.html</loc>"""
    if anchor not in xml:
        raise SystemExit("sitemap: parent civil-drainage entry not found")
    end = xml.index("</url>", xml.index(anchor)) + len("</url>\n")

    added = []
    block = ""
    for s in SUBURBS:
        loc = f"{BASE}/services/civil-drainage-{s['slug']}.html"
        if f"<loc>{loc}</loc>" in xml:
            continue
        added.append(s["slug"])
        block += f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{LASTMOD}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
"""
    if not block:
        return "sitemap: all suburb URLs already listed"
    open(SITEMAP, "w", encoding="utf-8").write(xml[:end] + block + xml[end:])
    return f"sitemap: added {len(added)} URLs"


def main():
    # Build suburb pages from the clean hub first, then patch the hub itself.
    for sub in SUBURBS:
        out = build_page(sub)
        print(f"  built {os.path.basename(out)}")
    print(patch_parent())
    print(patch_sitemap())
    print(f"\nDone. {len(SUBURBS)} pages. Idempotent.")


if __name__ == "__main__":
    main()
