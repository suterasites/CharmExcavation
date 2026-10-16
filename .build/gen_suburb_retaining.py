#!/usr/bin/env python3
"""gen_suburb_retaining.py - build Retaining Walls x suburb pages.

Fourth sibling of gen_suburb_excavation.py / gen_suburb_civil.py /
gen_suburb_siteprep.py, same method: clone the service-level page
(services/retaining-walls.html) - keeping header, footer, scripts, styles and the
generic service sections verbatim - then localise the head/schema, hero and
overview, and add an "On the ground" section, a suburb FAQ (with FAQPage schema)
and an "Areas we service" section. Also patches the parent service page with the
same Areas section, adds a "Retaining walls" link to that suburb's card in the
homepage and services-index "Where we work" grids, and adds every page to
sitemap.xml.

Idempotent: re-running overwrites the generated pages, re-inserts the Areas section
on the parent only if missing, skips grid links and sitemap URLs already present.
Output: services/retaining-walls-<suburb>.html

Why these suburbs first (2026-10-16, WP HQ Next move "suburb"): Officer and Clyde
North were the two target suburbs with no Search Console visibility for ANY service,
although each already had three indexed suburb pages. Retaining Walls carries the
most impressions of Charm's five services (71 of 326 in the 28 days to 2026-10-12)
and had no suburb pages at all, so a fourth page in each opens the service the site
is actually being found for. Endeavour Hills is the third because it is where the
site already takes retaining-wall impressions with no page to serve them (10 at
#36). Pages are built in batches of at most three (WP HQ paces one substantial
change per client per 4 weeks); the next window adds suburbs to SUBURBS.

Depth: every page carries the DEEP-style "On the ground" section from day one.
Google passed on this site's thin suburb pages (~450 words, ~43% shared with
siblings) and indexed the deepened ones (~930 words, ~26% shared), so a page built
thin is a page built to be refused. Copy rule as the rest of the site: real ground,
real housing stock, real process and paperwork - no invented jobs, no claimed
credentials, no fabricated locations.

House note: compiled-Tailwind site (styles.css). Only utility classes already in
the compiled CSS are used; the blocks lean on the page's own scoped classes
(sub-card etc.), so nothing new needs compiling.

Coverage note: the filename must carry the clients.yaml term for this service
("retaining wall") plus the suburb slug, or Apps/seo-hq's coverage matrix will not
count the page. retaining-walls-<suburb> contains "retaining-wall", and no other
Charm service term ("excavation", "drainage", "demolition", "landscaping") is a
substring of it, so the cell lights for this service only.

URL note: Cloudflare Pages 308-redirects /page.html to /page, so every canonical,
sitemap <loc> and internal href on this site is written WITHOUT the .html extension.
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICES = os.path.join(ROOT, "services")
BASE = "https://charmexcavation.com.au"
PARENT = os.path.join(SERVICES, "retaining-walls.html")
SITEMAP = os.path.join(ROOT, "sitemap.xml")
GRID_PAGES = [os.path.join(ROOT, "index.html"), os.path.join(ROOT, "services.html")]
LASTMOD = "2026-10-16"

# ── Per-suburb data ────────────────────────────────────────────────────────
# "deep" = intro + three (heading, paragraphs) cards for the On the ground block.
SUBURBS = [
    {
        "slug": "officer", "name": "Officer",
        "meta": "Retaining walls in Officer. Concrete sleeper boundary and site-cut walls for new estate builds, drained and backfilled. Call Dylan on 0431 529 254.",
        "hero": "On a new Officer estate lot the ground rarely finishes level with the neighbours, and the step between them needs a wall that drains and holds.",
        "ov1": "Officer is mostly new estates, so the retaining work comes straight out of the build: a boundary wall where one lot sits higher than the next, a wall across the back of the pad where the site cut left a face, and the lower garden walls that turn a sloping yard into a usable one.",
        "ov2": "We dig the footings, stand galvanised posts, drop the concrete sleepers in and put drainage aggregate behind before the backfill. One crew does the dig and the wall, so nobody is waiting on a second trade.",
        "local": "What decides an Officer wall is what it is holding back. A metre of the developer's fill behind a boundary is a different job to a low garden edge, so the height, the soil report and anything sitting above the wall get worked out before the posts go in.",
        "faqs": [
            ("Do you build boundary retaining walls on new Officer estates?", "Yes. Boundary walls between estate lots are one of the most common jobs out here, across Officer and Officer South. We excavate the footing line, stand the wall and backfill it with drainage behind."),
            ("When should the retaining wall go in on a new build?", "It depends on what the wall is doing. Where it holds up ground beside the slab or the driveway, the builder will usually want it in early, once the site cut is done. A garden wall can wait until after handover. We can work in with either."),
            ("Do I need a permit for a retaining wall in Officer?", "In Victoria a wall of around a metre or more, or one holding up a driveway, a building or a neighbour's ground, generally needs an engineer's design and a building permit. Your building surveyor makes that call, and we build to the engineer's spec."),
            ("What kind of wall suits an estate lot?", "Concrete sleepers between galvanised steel posts are the usual choice. They are slim, they sit neatly on a boundary line, and they do not rot the way timber does in wet ground. Timber and stone are both options where the look matters more."),
        ],
        "deep": {
            "intro": "Officer has filled up fast. Former farmland became estates, and the estates became streets of new homes, often several going up side by side at once. Almost every lot has had its levels set by the developer's earthworks before the owner ever stands on it, so the question is rarely whether a wall is needed. It is where the wall starts, how high it gets and what it is holding back.",
            "cards": [
                ("The step between lots", [
                    "When an estate is graded, each lot is set to suit the road and the stormwater rather than the lot beside it, so the ground often steps up or down at a side or rear boundary. Once the builder cuts the pad, that step can become a face of dirt along the fence line. A sleeper wall on the line is the tidy fix, and it is far easier to build before fences, paving and turf are in the way.",
                    "If the wall sits on the boundary, the neighbour will want to know about it. Sorting that out before the dig saves a conversation over a half-built wall.",
                ]),
                ("How the wall goes together", [
                    "Most walls on Officer estates are concrete sleepers between galvanised steel posts. The post holes are dug to the depth the height calls for, the posts are set plumb in concrete, and the sleepers drop in from above. Behind the wall goes slotted agi pipe in drainage aggregate, run to a proper outlet, then clean backfill.",
                    "Water is what pushes a wall over. Soil that cannot drain gets heavy after rain, and a wall with nowhere for that water to go is carrying far more than the dirt alone. The drainage is not an extra, it is half the wall.",
                ]),
                ("Before the posts go in", [
                    "Three things get checked first. The height and what sits above the wall, because a wall of around a metre or more, or one carrying a driveway, a slab or a neighbour's ground, generally needs an engineer's design and a building permit. The services, located through Before You Dig Australia, because gas, water and power often run close to the boundary on a new lot. And the estate's design guidelines, which on many estates cover what can face the street.",
                    "After that it is the dig, the wall and the drainage, all from one crew, with the spoil carted and the site cleaned down.",
                ]),
            ],
        },
    },
    {
        "slug": "clyde-north", "name": "Clyde North",
        "meta": "Retaining walls in Clyde North. Concrete sleeper walls for estate lots on reactive clay, with agi drainage and clean backfill. Call 0431 529 254.",
        "hero": "Clyde North lots are cut out of reactive clay and the developer's fill, so a wall here has to hold back ground that swells, shrinks and holds water.",
        "ov1": "Clyde North is almost entirely new estate building, and the retaining jobs come with it: a boundary wall where the lot next door was filled higher, a wall at the back of a cut pad, a low wall to square off a front garden, or a step in the side yard to make a level path down the side of the house.",
        "ov2": "We do the dig and the wall in one go: footings to depth, galvanised posts set in concrete, concrete sleepers stacked tight, agi drainage and aggregate behind, then backfill. The site is cleaned up before we leave.",
        "local": "Clyde North soil reports routinely come back Class H1 or H2, which means heavy reactive clay. That clay holds water, and water behind a wall is the load that tips it, so the drainage behind a Clyde North wall gets as much attention as the posts.",
        "faqs": [
            ("Do you build retaining walls across Clyde North?", "Yes. Clyde North and its estates are a regular part of our South East Melbourne run, from boundary walls between new lots to garden walls after handover."),
            ("My soil report says Class H. Does that change the wall?", "It changes what the wall has to cope with. Reactive clay swells when it is wet and holds water behind the wall, so the posts go to the depth the engineer or the sleeper supplier's tables call for, and the agi drain and aggregate behind it are not optional."),
            ("Can a fence go on top of the retaining wall?", "It can, but it has to be allowed for. A fence on top of a wall catches the wind and adds load to it, so tell us upfront and it goes into the design rather than being bolted on afterwards."),
            ("Should the wall go in before the fence and the landscaping?", "That is the best order. A boundary wall goes in far more easily with open access, before the fence, paving and turf are down, and the backfill can be left graded for the landscaper to follow."),
        ],
        "deep": {
            "intro": "Clyde North is the growth corridor at full stretch, with new streets running off Thompsons Road, Berwick-Cranbourne Road and Pound Road and homes going up on every side. Each lot comes off the developer with its levels already set, and because an estate is graded to suit its roads and drains rather than its neighbours, plenty of lots end up a step above or below the one beside them.",
            "cards": [
                ("Fill, cut and the lot next door", [
                    "One lot might sit on a metre of placed fill and the next on natural ground, which is how a face of dirt ends up along a side fence. From the higher lot it is a drop; from the lower one it is a bank. A sleeper wall on or near the line sorts both, and it is far easier to build while the lots either side are still open.",
                    "Where the wall is on a shared boundary, talk to the neighbour before the dig. On a street where everyone is building at once, they are usually thinking about the same thing.",
                ]),
                ("Clay and water", [
                    "The ground out here is heavy reactive clay. It swells when it is wet, shrinks when it dries and drains slowly, so after a wet week the soil behind a wall is heavy and full of water. That pressure is what leans a wall over, not the dirt on its own.",
                    "So every wall gets slotted agi pipe at the base in drainage aggregate, taken to a proper outlet, with clean backfill above it. On Class H ground that is the difference between a wall that stands and one that starts to lean after a few winters.",
                ]),
                ("Estate rules and paperwork", [
                    "New estates come with rules of their own. Many have design guidelines covering what faces the street, the City of Casey wants an asset protection permit in place before building works start, and services along a new boundary are worth locating through Before You Dig Australia before the first post hole.",
                    "Height is the other check. In Victoria a wall of around a metre or more, or one holding up a driveway, a slab or a neighbour's ground, generally needs an engineer's design and a building permit. Your building surveyor decides, and we build to the engineer's spec.",
                ]),
            ],
        },
    },
    {
        "slug": "endeavour-hills", "name": "Endeavour Hills",
        "meta": "Retaining walls in Endeavour Hills. Sloping-block walls, terraced yards and tired timber sleeper walls rebuilt in concrete. Call 0431 529 254.",
        "hero": "Endeavour Hills is built across a rise, so a lot of its back yards are held up by retaining walls, and plenty of those walls are getting old.",
        "ov1": "Endeavour Hills is established housing on undulating ground. The wall jobs here are replacing timber sleeper walls that have started to lean or rot, terracing a sloping back yard into flat levels, and building a wall behind a new pad where an extension, a shed or a pool has been cut into the slope.",
        "ov2": "Compact machines get down the side of the house, we protect the garden that is staying, and the old sleepers and spoil leave with us. Then it is footings to depth, galvanised posts in concrete, concrete sleepers, drainage and backfill.",
        "local": "On a slope a wall holds up more than the dirt directly behind it. Everything above it pushes down too, the rest of the yard, a path, a driveway, so the height and what sits above the wall decide how deep the posts go.",
        "faqs": [
            ("Can you replace an old timber retaining wall in Endeavour Hills?", "Yes. Taking out a tired timber sleeper wall and rebuilding it in concrete sleepers on galvanised posts is common work up here. The old timber is removed and carted away, and the new wall gets proper drainage behind it."),
            ("Can you terrace a sloping back yard?", "We can. Tiered walls step a slope down into flat levels you can actually use, with drainage between the tiers so water does not build up behind the upper wall."),
            ("Can you get a machine into an established Endeavour Hills yard?", "Usually. Our compact excavator is sized for standard side-gate access, and we plan the route in around the trees and garden beds that are staying."),
            ("Why do retaining walls lean?", "Mostly water. Soil behind a wall that cannot drain gets heavy after rain, and timber that has sat wet for years rots at the posts. A leaning wall usually means the drainage behind it is not doing its job, which is why a rebuild starts with the drainage, not just new sleepers."),
        ],
        "deep": {
            "intro": "Endeavour Hills is a suburb of slopes. Streets climb and curve, back yards fall away from the house or rise up behind it, and a lot of those yards were made usable years ago with timber sleeper walls. Many are still standing. Plenty are leaning, bowing or soft at the posts, and those are the ones that turn into a phone call.",
            "cards": [
                ("Old walls, new walls", [
                    "A timber wall that has been in the ground for a long time usually goes at the posts first, where the wood stays wet. It shows as a lean, a bulge, or sleepers pulling apart. Replacing it is a dig-out as much as a build: the old wall and the soil behind it come out, the line is reset, and the new wall goes in with drainage behind it, which older walls often go without.",
                    "Concrete sleepers on galvanised steel posts are the usual replacement. They will not rot, and the slim profile means the new wall takes up little more room than the old one.",
                ]),
                ("Terracing a slope", [
                    "Where a yard falls away from the house, one tall wall is rarely the best answer. Two or three lower walls stepped down the slope give you flat levels to use, and each carries less load than a single big wall would. Drainage runs behind every tier so water is not passed down the hill into the next wall.",
                    "On sloping ground the dig and the retaining are the one job. The levels are set before the first post hole, so each terrace comes out flat and the walls line up.",
                ]),
                ("Working in an established yard", [
                    "Endeavour Hills yards come with mature trees, garden beds, paths and fences, and most of it is staying. The side access decides the machine size, and the route in and where the spoil goes are planned before we start. Underground services are located through Before You Dig Australia, because an older yard can hide a stormwater or sewer line where nobody expects it.",
                    "Height matters on a replacement as much as a new wall. In Victoria a wall of around a metre or more, or one holding up a driveway, a building or a neighbour's ground, generally needs an engineer's design and a building permit, so check with a building surveyor before the old wall comes out.",
                ]),
            ],
        },
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
    # Take every newline after it: the insert adds a separator line, and leaving
    # one behind made each re-run grow the hub by a blank line.
    while html[j:j + 1] == '\n':
        j += 1
    return html[:i] + html[j:]


def json_ld(sub):
    url = f"{BASE}/services/retaining-walls-{sub['slug']}"
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
            "serviceType": "Retaining Wall Construction",
            "name": f"Retaining Walls in {name}",
            "url": url,
            "provider": {"@id": f"{BASE}/#business"},
            "areaServed": area,
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": f"Retaining Wall Services in {name}",
                "itemListElement": [
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Concrete Sleeper Retaining Walls"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Timber Retaining Walls"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Stone Retaining Walls"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Tiered and Slope Walls"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Retaining Wall Drainage and Backfill"}},
                ],
            },
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": "Services", "item": f"{BASE}/services"},
                {"@type": "ListItem", "position": 3, "name": "Retaining Walls", "item": f"{BASE}/services/retaining-walls"},
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
    grid_cls = "grid md:grid-cols-2 lg:grid-cols-4 gap-5 lg:gap-6" if len(sub["faqs"]) == 4 else "grid md:grid-cols-3 gap-5 lg:gap-6"
    return f'''<section id="faq" class="relative bg-char-950 overflow-hidden">
  <div class="max-w-7xl mx-auto px-6 lg:px-10 py-20 lg:py-24">
    <div class="max-w-2xl mb-12">
      <div class="flex items-center gap-3 mb-5"><span class="h-px w-10 bg-gold-400"></span><span class="font-sport text-xs tracking-[0.3em] uppercase text-gold-400">{sub['name']} questions</span></div>
      <h2 class="font-display text-4xl md:text-5xl uppercase leading-[0.92] text-cream">Common <span class="text-gold-400">questions.</span></h2>
    </div>
    <div class="{grid_cls}">
{cards}
    </div>
  </div>
</section>
'''


def deep_section(sub):
    """Suburb-specific depth block. Sits between Other services (char-950) and the
    FAQ (char-950), on char-900 so the background alternation holds."""
    d = sub["deep"]
    name, slug = sub["name"], sub["slug"]
    cards = []
    for i, (h, paras) in enumerate(d["cards"], 1):
        body = "\n".join(f'        <p class="mt-3 text-sm text-cream/65 leading-relaxed">{p}</p>' for p in paras)
        cards.append(f'''      <article class="sub-card bg-char-950 rounded-sm overflow-hidden p-7">
        <div class="font-sport text-xs tracking-[0.25em] uppercase text-gold-400 mb-3">{i:02d}</div>
        <h3 class="font-display text-2xl uppercase text-cream leading-tight">{h}</h3>
{body}
      </article>''')
    grid = "\n".join(cards)
    exc = f"/services/excavation-earthmoving-{slug}"
    civ = f"/services/civil-drainage-{slug}"
    prep = f"/services/site-preparation-demolition-{slug}"
    return f'''<section id="on-the-ground" class="relative bg-char-900 overflow-hidden">
  <div class="max-w-7xl mx-auto px-6 lg:px-10 py-20 lg:py-24">
    <div class="max-w-3xl mb-12">
      <div class="flex items-center gap-3 mb-5"><span class="h-px w-10 bg-gold-400"></span><span class="font-sport text-xs tracking-[0.3em] uppercase text-gold-400">On the ground in {name}</span></div>
      <h2 class="font-display text-4xl md:text-5xl uppercase leading-[0.92] text-cream">Retaining walls in <span class="text-gold-400">{name}.</span></h2>
      <p class="mt-5 text-cream/70 leading-relaxed">{d["intro"]}</p>
    </div>
    <div class="grid md:grid-cols-3 gap-5 lg:gap-6">
{grid}
    </div>
    <p class="mt-10 text-sm text-cream/65 leading-relaxed">Also in {name}: <a href="{exc}" class="text-gold-400 hover:text-gold-300 transition">excavation and earthmoving</a>, <a href="{civ}" class="text-gold-400 hover:text-gold-300 transition">civil and drainage</a> and <a href="{prep}" class="text-gold-400 hover:text-gold-300 transition">site prep and demolition</a>.</p>
  </div>
</section>
'''


def areas_section(active_slug=None):
    """Grid linking every Retaining Walls suburb page built so far. The active
    suburb (on its own page) renders as a non-linked gold tile. Three columns, not
    four, while the cluster is small, so a short row does not read as a gap."""
    tiles = []
    for s in SUBURBS:
        href = f"/services/retaining-walls-{s['slug']}"
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
      <h2 class="font-display text-4xl md:text-5xl uppercase leading-[0.92] text-cream">Retaining walls across <span class="text-gold-400">South East Melbourne.</span></h2>
      <p class="mt-5 text-cream/70 leading-relaxed">Owner-operated wall builds from our Keysborough base, from Dandenong out to Pakenham and down to Frankston. Local detail for the suburbs below, or call Dylan direct on <a href="tel:0431529254" class="text-gold-400 hover:text-gold-300 transition">0431 529 254</a>.</p>
    </div>
    <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 lg:gap-4">
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
    url = f"{BASE}/services/retaining-walls-{slug}"
    title = f"Retaining Walls {name} | Charm Excavation"

    # Head lengths are audited (title 40-65, meta description 120-170 in
    # Apps/sutera-seo/checklist.py) - fail the build rather than ship a warn.
    if not 40 <= len(title) <= 65:
        raise SystemExit(f"[{slug}] title is {len(title)} chars (need 40-65): {title}")
    if not 120 <= len(sub["meta"]) <= 170:
        raise SystemExit(f"[{slug}] meta description is {len(sub['meta'])} chars (need 120-170)")

    # -- head --
    html = rep(html,
        "<title>Retaining Walls - Concrete Sleeper, Timber & Stone, Melbourne SE</title>",
        f"<title>{title}</title>", "title")
    html = rep(html,
        '<meta name="description" content="Concrete sleeper, timber and stone retaining walls across Melbourne\'s South East. Engineered to plan, built to hold. Owner-operated. Call Dylan for a quote." />',
        f'<meta name="description" content="{sub["meta"]}" />', "desc")
    html = rep(html,
        '<meta name="geo.placename" content="Melbourne">',
        f'<meta name="geo.placename" content="{name}">', "geo")
    html = rep(html,
        '<link rel="canonical" href="https://charmexcavation.com.au/services/retaining-walls">',
        f'<link rel="canonical" href="{url}">', "canonical")
    # open graph
    html = rep(html,
        '<meta property="og:title" content="Retaining Walls - Concrete Sleeper, Timber & Stone, Melbourne SE">',
        f'<meta property="og:title" content="Retaining Walls {name} - Charm Excavation">', "og:title")
    html = rep(html,
        '<meta property="og:description" content="Concrete sleeper, timber and stone retaining walls across Melbourne\'s South East. Engineered to plan, built to hold.">',
        f'<meta property="og:description" content="{sub["meta"]}">', "og:desc")
    html = rep(html,
        '<meta property="og:url" content="https://charmexcavation.com.au/services/retaining-walls">',
        f'<meta property="og:url" content="{url}">', "og:url")
    # twitter
    html = rep(html,
        '<meta name="twitter:title" content="Retaining Walls - Concrete Sleeper, Timber & Stone, SE Melbourne">',
        f'<meta name="twitter:title" content="Retaining Walls {name} - Charm Excavation">', "tw:title")
    html = rep(html,
        '<meta name="twitter:description" content="Concrete sleeper, timber and stone retaining walls across Melbourne\'s South East.">',
        f'<meta name="twitter:description" content="Concrete sleeper, timber and stone retaining walls in {name}, South East Melbourne.">', "tw:desc")

    # -- json-ld: replace the first ld+json script block --
    ld_start = html.index('<script type="application/ld+json">')
    ld_end = html.index('</script>', ld_start) + len('</script>')
    html = html[:ld_start] + json_ld(sub) + html[ld_end:]

    # -- visible breadcrumb --
    html = rep(html,
        '''    <li><a href="/services" class="hover:text-gold-400">Services</a></li>
    <li aria-hidden="true">/</li>
    <li aria-current="page" class="text-cream/90">Retaining Walls</li>''',
        f'''    <li><a href="/services" class="hover:text-gold-400">Services</a></li>
    <li aria-hidden="true">/</li>
    <li><a href="/services/retaining-walls" class="hover:text-gold-400">Retaining Walls</a></li>
    <li aria-hidden="true">/</li>
    <li aria-current="page" class="text-cream/90">{name}</li>''', "breadcrumb")

    # -- hero eyebrow / label / h1 / paragraph --
    html = rep(html,
        '<div class="flex items-center gap-4 mb-6 text-xs font-sport tracking-[0.25em] uppercase text-cream/50"><a href="/services" class="hover:text-gold-400 transition">Services</a><span>/</span><span class="text-gold-400">Retaining Walls</span></div>',
        f'<div class="flex items-center gap-4 mb-6 text-xs font-sport tracking-[0.25em] uppercase text-cream/50"><a href="/services/retaining-walls" class="hover:text-gold-400 transition">Retaining Walls</a><span>/</span><span class="text-gold-400">{name}</span></div>', "hero-eyebrow")
    html = rep(html,
        '<span class="font-sport text-xs tracking-[0.3em] uppercase text-gold-400">Service</span>',
        f'<span class="font-sport text-xs tracking-[0.3em] uppercase text-gold-400">{name}, SE Melbourne</span>', "hero-label")
    html = rep(html,
        '<h1 class="font-display text-5xl md:text-6xl lg:text-[6rem] leading-[0.9] uppercase text-cream">Retaining <br/><span class="text-gold-400">Walls.</span></h1>',
        f'<h1 class="font-display text-5xl md:text-6xl lg:text-[6rem] leading-[0.9] uppercase text-cream">Retaining Walls <br/>in <span class="text-gold-400">{name}.</span></h1>', "h1")
    html = rep(html,
        '<p class="mt-8 text-lg md:text-xl text-cream/80 max-w-2xl leading-relaxed">Concrete sleeper, timber, stone. Engineered to plan, built to hold. From tight backyard walls to tiered rural drops.</p>',
        f'<p class="mt-8 text-lg md:text-xl text-cream/80 max-w-2xl leading-relaxed">{sub["hero"]}</p>', "hero-p")

    # -- overview heading + paragraphs (2 -> 3, incl local knowledge) --
    html = rep(html,
        '<h2 class="font-display text-4xl md:text-5xl uppercase leading-[0.92] text-cream">Built to <br/><span class="text-burgundy-500">hold ground.</span></h2>',
        f'<h2 class="font-display text-4xl md:text-5xl uppercase leading-[0.92] text-cream">Walls built for <br/><span class="text-burgundy-500">{name}.</span></h2>', "ov-head")
    html = rep(html,
        '''        <p>A retaining wall is one of those jobs where the prep matters as much as the build. We excavate to line, set the footings, stand the posts, and backfill with the right drainage behind.</p>
        <p>Sleeper, timber, natural stone, we've built them in tight backyards, on rural slopes, alongside sheds and driveways. If it's an engineered wall we work to the spec. If it's straightforward, we quote the build turnkey.</p>''',
        f'''        <p>{sub["ov1"]}</p>
        <p>{sub["ov2"]}</p>
        <p>{sub["local"]}</p>''', "ov-body")

    # -- insert depth + FAQ + Areas before the CTA section --
    cta = '<section class="relative bg-burgundy-800 overflow-hidden">'
    html = rep(html, cta, deep_section(sub) + faq_section(sub) + "\n" + areas_section(slug) + "\n" + cta, "insert-deep-faq-areas")

    out = os.path.join(SERVICES, f"retaining-walls-{slug}.html")
    open(out, "w", encoding="utf-8").write(html)
    return out


def patch_parent():
    """Add (or refresh) the Areas section on the hub service page, so the cluster
    is crawlable from the hub and a later batch's suburbs appear there too."""
    html = open(PARENT, encoding="utf-8").read()
    had = 'id="areas-we-service"' in html
    html = strip_areas(html)
    cta = '<section class="relative bg-burgundy-800 overflow-hidden">'
    if html.count(cta) != 1:
        raise SystemExit("parent: CTA anchor not unique")
    new = html.replace(cta, areas_section(None) + "\n" + cta, 1)
    if had and new == open(PARENT, encoding="utf-8").read():
        return "parent: areas section already current"
    open(PARENT, "w", encoding="utf-8").write(new)
    return "parent: areas section " + ("refreshed" if had else "inserted")


def patch_grids():
    """Add a 'Retaining walls' link to each built suburb's card in the homepage and
    services-index 'Where we work' grids (both indexed and recrawled often), right
    after that card's Site prep link."""
    notes = []
    for path in GRID_PAGES:
        html = open(path, encoding="utf-8").read()
        added = 0
        for s in SUBURBS:
            href = f"/services/retaining-walls-{s['slug']}"
            if f'href="{href}"' in html:
                continue
            anchor = f'<a href="/services/site-preparation-demolition-{s["slug"]}" class="hover:text-gold-400 transition">Site prep</a>'
            if html.count(anchor) != 1:
                raise SystemExit(f"{os.path.basename(path)}: grid anchor for {s['slug']} not unique ({html.count(anchor)})")
            i = html.index(anchor) + len(anchor)
            indent = html[html.rindex("\n", 0, html.index(anchor)) + 1:html.index(anchor)]
            html = html[:i] + f'\n{indent}<a href="{href}" class="hover:text-gold-400 transition">Retaining walls</a>' + html[i:]
            added += 1
        if added:
            open(path, "w", encoding="utf-8").write(html)
        notes.append(f"{os.path.basename(path)}: {added} grid link(s) added")
    return "; ".join(notes)


def patch_sitemap():
    """Add any missing suburb URLs straight after the parent service entry, and
    bump lastmod on the pages this run changed (hub, homepage, services index)."""
    xml = open(SITEMAP, encoding="utf-8").read()
    anchor = f"""  <url>
    <loc>{BASE}/services/retaining-walls</loc>"""
    if anchor not in xml:
        raise SystemExit("sitemap: parent retaining-walls entry not found")
    end = xml.index("</url>", xml.index(anchor)) + len("</url>\n")

    added = []
    block = ""
    for s in SUBURBS:
        loc = f"{BASE}/services/retaining-walls-{s['slug']}"
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
    if block:
        xml = xml[:end] + block + xml[end:]

    bumped = []
    for loc in (f"{BASE}/", f"{BASE}/services", f"{BASE}/services/retaining-walls"):
        i = xml.index(f"<loc>{loc}</loc>")
        j = xml.index("<lastmod>", i)
        k = xml.index("</lastmod>", j)
        if xml[j + len("<lastmod>"):k] < LASTMOD:
            xml = xml[:j] + f"<lastmod>{LASTMOD}" + xml[k:]
            bumped.append(loc)

    if not block and not bumped:
        return "sitemap: already current"
    open(SITEMAP, "w", encoding="utf-8").write(xml)
    return f"sitemap: added {len(added)} URLs, lastmod bumped on {len(bumped)}"


def main():
    # Build suburb pages from the clean hub first, then patch the hub itself.
    for sub in SUBURBS:
        out = build_page(sub)
        print(f"  built {os.path.basename(out)}")
    print(patch_parent())
    print(patch_grids())
    print(patch_sitemap())
    print(f"\nDone. {len(SUBURBS)} pages. Idempotent.")


if __name__ == "__main__":
    main()
