#!/usr/bin/env python3
"""gen_suburb_excavation.py - build Excavation & Earthmoving x suburb landing pages.

Clones the service-level page (services/excavation-earthmoving.html) - keeping its
header, footer, scripts, styles and the generic service sections (capabilities,
recent work, other services, CTA) verbatim - and localises the head/schema, hero,
overview and adds a suburb FAQ (with FAQPage schema) plus an "Areas we service"
mesh-linking section. Also patches the parent service page with the same Areas
section so the cluster is crawlable from the hub.

Idempotent: re-running overwrites the generated pages and re-inserts the Areas
section on the parent only if it is not already there. Output:
services/excavation-earthmoving-<suburb>.html

House note: compiled-Tailwind site (styles.css). Only utility classes already in
the base page are reused; the Areas/FAQ blocks lean on the page's own scoped
classes (sub-card etc.), so nothing new needs compiling.

URL note: Cloudflare Pages 308-redirects /page.html to /page, so every canonical,
sitemap <loc> and internal href on this site is written WITHOUT the .html extension.
Emitting .html here would point the canonical at a URL that redirects, and Google
indexes both forms and splits the ranking signal between them.
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICES = os.path.join(ROOT, "services")
BASE = "https://charmexcavation.com.au"
PARENT = os.path.join(SERVICES, "excavation-earthmoving.html")

# ── Per-suburb data ────────────────────────────────────────────────────────
# name/slug + localised copy. No fabricated past-project claims - framed as
# service-area capability + genuine local site conditions.
SUBURBS = [
    {
        "slug": "dandenong", "name": "Dandenong",
        "meta": "Excavation and earthmoving in Dandenong, SE Melbourne. Pool and footing digs, bulk cuts and tight-access work, spoil removed. Call Dylan on 0431 529 254.",
        "hero": "From the established brick homes around the CBD to new townhouse and commercial infill, we bring the right machine to every Dandenong excavation and earthmoving job.",
        "ov1": "Dandenong sites cover the full spread - tight established residential blocks needing pool and footing digs, through to open commercial and industrial pads. We match the machine to the access, from a mini-excavator down a narrow side to the 5-tonne on an open lot.",
        "ov2": "We are based just down the road in Keysborough, so we are on Dandenong jobs quickly, and the reactive clay through this pocket is ground we work week in, week out.",
        "local": "A lot of Dandenong's older housing sits on reactive clay, so clean battering, benching and spoil handling make the difference between a smooth pour and a bogged site. We cut to spec, keep the ground safe, and cart the fill off so your builder walks onto pad-ready ground.",
        "faqs": [
            ("Which parts of Dandenong do you cover?", "All of it - Dandenong, Dandenong North, Dandenong South and the surrounding pockets. Being based in Keysborough, we are only minutes from most jobs."),
            ("Can you access a tight block in an older Dandenong street?", "Yes. We run everything from a compact mini-excavator for narrow side access up to a 5-tonne machine for open pads, so older, tighter blocks are no trouble."),
            ("Do you handle spoil removal in Dandenong?", "We do. Loading out and carting away excavated material is part of the job, so you are left with clean, level, pad-ready ground."),
        ],
    },
    {
        "slug": "cranbourne", "name": "Cranbourne",
        "meta": "Excavation and earthmoving in Cranbourne. Footings, pool digs and bulk cuts for new estate builds, set out to plan. Owner-operated. Call 0431 529 254.",
        "hero": "Cranbourne's new estates and house-and-land blocks keep the excavators busy - footings, pool digs and bulk cuts, all sized to the site.",
        "ov1": "Cranbourne and its growth pockets - Cranbourne West, East and North - are full of new builds, which means footings, service trenches, pool excavations and bulk site cuts. We turn up with the machine the block calls for and get the dig done clean.",
        "ov2": "It is a short run from our Keysborough base, so we keep Cranbourne jobs moving to your builder's program without the wait.",
        "local": "New-estate blocks in Cranbourne often mix sand over clay, so getting levels and batters right the first time matters for the slab that follows. We set out accurately, dig to plan, and remove the spoil so the site is ready for the next trade.",
        "faqs": [
            ("Do you cover the Cranbourne growth estates?", "Yes - Cranbourne, Cranbourne West, Cranbourne East, Cranbourne North and the newer estates around them are all in our regular service area."),
            ("Can you dig footings and pools for a new Cranbourne build?", "That is a big part of what we do out here - footing trenches, pool digs and bulk cuts for new house-and-land builds, set out to your plans."),
            ("How quickly can you get to a Cranbourne site?", "We are based in Keysborough, a short drive away, so we can usually slot Cranbourne jobs in fast around your build schedule."),
        ],
    },
    {
        "slug": "berwick", "name": "Berwick",
        "meta": "Excavation and earthmoving in Berwick, including sloping-block cut-and-fill, pool digs and footings. Owner-operated, SE Melbourne. Call 0431 529 254.",
        "hero": "From the leafy established streets to the premium new builds on Berwick's hills, we handle excavation on flat and sloping blocks alike.",
        "ov1": "Berwick mixes established homes with premium new builds, and a lot of it sits on a slope. That means cut-and-fill, benched pads and careful excavation where levels and retaining go hand in hand.",
        "ov2": "We size the machine to the access and the fall of the land, so whether it is a hillside pool dig or footings on a tight established block, the ground comes up right.",
        "local": "The rise through Berwick means a lot of blocks need a considered cut - get the batter and benching wrong and you pay for it in retaining later. We plan the dig around the fall, keep the site stable, and cart the spoil off.",
        "faqs": [
            ("Do you work on Berwick's sloping blocks?", "Yes - sloping-site excavation is routine for us. We plan the cut-and-fill and benching so the pad is stable and ready for footings or a slab."),
            ("Do you cover Berwick and Beaconsfield?", "We service Berwick and the surrounding pockets, including Beaconsfield and Harkaway, as part of our SE Melbourne area."),
            ("Can you handle the excavation and retaining together?", "We can. On sloping Berwick blocks the dig and the retaining often go together, and we can take care of both in the one job."),
        ],
    },
    {
        "slug": "narre-warren", "name": "Narre Warren",
        "meta": "Excavation and earthmoving in Narre Warren - pool digs, shed pads and footings with tight side-gate access. Owner-operated. Call 0431 529 254.",
        "hero": "Pool digs, shed pads, footings and side-access excavation across Narre Warren's family blocks - the right-sized machine for every job.",
        "ov1": "Narre Warren is full of established family homes, which means the work is often pool excavations, shed and garage pads, footings and renovations on standard suburban blocks with side access to negotiate.",
        "ov2": "We run compact machines that fit down a side gate without taking the fence out, then scale up when the block opens onto an easy working area.",
        "local": "Most Narre Warren jobs come down to access - getting a machine to the backyard through a standard side gate. We bring gear that fits, protect the paths and fences on the way through, and leave the site clean.",
        "faqs": [
            ("Can you get a machine into my Narre Warren backyard?", "Usually yes. We run compact excavators built for standard side-gate access, so most backyard pool and shed digs are no problem."),
            ("Do you cover Narre Warren South and Fountain Gate?", "Yes - Narre Warren, Narre Warren South, Narre Warren North and the Fountain Gate area are all in our regular run."),
            ("Do you dig pools in Narre Warren?", "We do - pool excavations are one of our most common jobs out here, set out to the pool builder's dimensions and dug clean."),
        ],
    },
    {
        "slug": "pakenham", "name": "Pakenham",
        "meta": "Excavation and earthmoving in Pakenham, from new-estate footings to rural-fringe earthworks and tank pads. Owner-operated. Call 0431 529 254.",
        "hero": "Pakenham's growth corridor keeps the earthmovers moving - bulk cuts, footings and rural-fringe earthworks across new estates and acreage alike.",
        "ov1": "Pakenham spans brand-new estates - Lakeside, Cardinia Lakes and out toward Officer - and a rural-residential fringe. So the work runs from new-build footings and bulk cuts through to acreage earthworks, dam and tank pads and access tracks.",
        "ov2": "We bring the machine the job needs, whether that is a tidy footing dig on an estate block or a bigger push on a rural property.",
        "local": "The spread of Pakenham means one job is a tight estate footing and the next is an open paddock. We scale the gear accordingly, work to your levels, and cart off or spread spoil depending on what the site needs.",
        "faqs": [
            ("Do you cover Pakenham and the surrounding estates?", "Yes - Pakenham, Pakenham Upper, the Lakeside and Cardinia estates and the rural blocks around town are all part of our service area."),
            ("Can you do earthworks on a rural Pakenham property?", "We can - acreage earthworks, tank and shed pads, dam work and access tracks are all within our scope on the rural fringe."),
            ("Are you set up for new-estate footing digs in Pakenham?", "Yes. Footing trenches, service runs and bulk cuts for new house-and-land builds are core work for us across the growth corridor."),
        ],
    },
    {
        "slug": "officer", "name": "Officer",
        "meta": "Excavation and earthmoving in Officer - footings, service trenches and bulk cuts for new estate builds, set out to plan. Call 0431 529 254.",
        "hero": "Officer's new estates are going up fast, and we are on the ground for the footings, service trenches and bulk cuts that get each build started.",
        "ov1": "Officer is one of the SE corridor's fast-filling growth areas, largely brand-new estates on former farmland. The bread and butter here is new-build excavation - footing trenches, service runs, pool digs and bulk site cuts on greenfield blocks.",
        "ov2": "We set out accurately off your plans and keep the dig moving so the slab and the trades behind it are not left waiting.",
        "local": "Greenfield estate blocks in Officer are often a clean slate, which makes accurate setout and level control the whole game. We dig to plan, keep the batters tidy, and remove spoil so the site hands over pad-ready.",
        "faqs": [
            ("Do you service the new Officer estates?", "Yes - Officer and Officer South, including the newer estates, are in our regular SE Melbourne service area."),
            ("Can you dig footings for a new Officer build?", "That is core work for us out here - footing trenches, service trenches and bulk cuts for new house-and-land builds, set out to your plans."),
            ("How soon can you start on an Officer block?", "We are a short run from Keysborough, so we can usually get onto Officer jobs quickly and keep to your builder's program."),
        ],
    },
    {
        "slug": "clyde", "name": "Clyde",
        "meta": "Excavation and earthmoving in Clyde - footings, pool digs and bulk site cuts for new estate builds. Owner-operated, SE Melbourne. Call 0431 529 254.",
        "hero": "Clyde's former farmland is fast becoming new estates, and we are there for the footings, pools and bulk cuts every new build needs.",
        "ov1": "Clyde has turned from farmland to one of the region's busiest new-build areas almost overnight. That means high volumes of footing digs, service trenches, pool excavations and bulk site cuts on fresh estate blocks.",
        "ov2": "We come set up for new-build work - accurate setout, clean batters, and spoil carted off so the block is ready for the slab crew.",
        "local": "Newly released Clyde blocks are typically flat and open, so the job is about precise levels and getting the dig done to program. We work to your plans, keep the site clean, and remove the fill efficiently.",
        "faqs": [
            ("Do you cover the new estates in Clyde?", "Yes - Clyde and its new estates are part of our core SE Melbourne service area."),
            ("What is the difference between your Clyde and Clyde North service?", "None in practice - we cover both. Clyde and Clyde North sit side by side in the growth corridor and we work throughout."),
            ("Can you handle pool and footing digs on a Clyde estate block?", "Absolutely - pool excavations, footing trenches and bulk cuts for new builds are exactly what we do across Clyde."),
        ],
    },
    {
        "slug": "clyde-north", "name": "Clyde North",
        "meta": "Excavation and earthmoving in Clyde North - fast, accurate footings, pool digs and bulk cuts for new builds. Owner-operated. Call 0431 529 254.",
        "hero": "One of Victoria's fastest-growing pockets - Clyde North's new estates keep us busy with footings, pool digs and bulk earthmoving.",
        "ov1": "Clyde North is among the fastest-growing suburbs in the state, wall-to-wall new estates. The work is new-build excavation at volume: footing trenches, service runs, pool digs, driveways and bulk cuts.",
        "ov2": "We are geared for estate work - in fast, dug to plan, spoil removed, and off to keep your build program on track.",
        "local": "With so many blocks going in at once, Clyde North is all about turnaround and accuracy. We set out off your plans, cut to level, and clear the spoil so the following trades can move straight in.",
        "faqs": [
            ("Do you service all of Clyde North?", "Yes - Clyde North and its many new estates are a core part of our SE Melbourne service area."),
            ("Can you keep up with a tight new-build schedule in Clyde North?", "That is what we are set up for - fast, accurate footing and bulk-cut work so the slab and trades behind you are not held up."),
            ("Do you dig driveways and pools on Clyde North blocks?", "We do - pool excavations, driveway cuts, footings and service trenches are all everyday work for us across Clyde North."),
        ],
    },
    {
        "slug": "frankston", "name": "Frankston",
        "meta": "Excavation and earthmoving in Frankston - pool digs, footings and sloping-site cuts across bayside and inland blocks. Call 0431 529 254.",
        "hero": "From bayside blocks to the hills behind town, we handle excavation across Frankston's mix of established and sloping sites.",
        "ov1": "Frankston runs from established homes near the bay to hillier blocks inland, on soils that shift from coastal sand to heavier ground. The work is pool digs, footings, renovations and the odd sloping-site cut.",
        "ov2": "We read the block first - sand, slope or tight access - and bring the machine to suit, so the dig comes up clean and stable.",
        "local": "Sandy coastal ground near the bay behaves very differently to the firmer blocks inland, and both turn up in Frankston. We adjust battering and shoring to the soil, keep the excavation safe, and cart off the spoil.",
        "faqs": [
            ("Do you cover Frankston and Frankston South?", "Yes - Frankston, Frankston South, Frankston North and Seaford are all within our service area."),
            ("Can you dig in sandy coastal ground?", "We can - sandy blocks near the bay need the batters and any shoring handled correctly, and that is something we account for on every coastal Frankston job."),
            ("Do you work on Frankston's sloping blocks?", "Yes - the hillier blocks inland often need a considered cut, and sloping-site excavation is routine for us."),
        ],
    },
    {
        "slug": "hallam", "name": "Hallam",
        "meta": "Excavation and earthmoving in Hallam - footings, shed pads, drainage and site cuts across residential and light-industrial blocks. Call 0431 529 254.",
        "hero": "Standard blocks, sheds, drainage and footings across Hallam's residential and light-industrial pockets - sized to the site.",
        "ov1": "Hallam sits between Dandenong and Narre Warren and mixes established residential streets with light-industrial pockets. The work is a bit of everything: footings, shed pads, drainage runs, pool digs and small site cuts.",
        "ov2": "It is on our doorstep from Keysborough, so we can be on a Hallam job quickly with the right machine for the block.",
        "local": "Whether it is a residential backyard or a light-industrial lot, Hallam jobs come down to matching the machine to the access and getting the levels right. We dig clean, handle any drainage falls, and clear the spoil.",
        "faqs": [
            ("Do you service Hallam?", "Yes - Hallam is right on our doorstep from Keysborough, so it is a regular part of our SE Melbourne service area."),
            ("Can you do drainage excavation in Hallam?", "We can - trenching for stormwater and site drainage, dug to the right falls, is part of what we do."),
            ("Do you handle both residential and commercial blocks in Hallam?", "Yes - from backyard pool and shed digs to small light-industrial site cuts, we scale the gear to the job."),
        ],
    },
    {
        "slug": "hampton-park", "name": "Hampton Park",
        "meta": "Excavation and earthmoving in Hampton Park - pool, shed and granny-flat pads and footings on standard blocks. Owner-operated. Call 0431 529 254.",
        "hero": "Pools, sheds, granny-flat pads and footings across Hampton Park's established suburban blocks - the right machine, tidy access.",
        "ov1": "Hampton Park is a settled residential suburb of standard family blocks, so the work is mostly pool excavations, shed and granny-flat pads, footings and renovation digs with side access to work around.",
        "ov2": "We bring compact machines that fit through a standard gate, protect the path in, and leave the yard clean when the dig is done.",
        "local": "The typical Hampton Park job is a backyard dig reached through a side gate, so access and site protection matter as much as the excavation itself. We fit the right machine, mind the fences and paths, and cart the spoil off.",
        "faqs": [
            ("Do you cover Hampton Park?", "Yes - Hampton Park is part of our regular SE Melbourne run, only a short drive from our Keysborough base."),
            ("Can you dig a granny-flat or shed pad in Hampton Park?", "We can - pad excavations for granny flats, sheds and garages are common work for us on established blocks."),
            ("Will a machine fit down the side of my Hampton Park house?", "Usually yes - we run compact excavators for standard side-gate access, so most backyard digs are no problem."),
        ],
    },
    {
        "slug": "endeavour-hills", "name": "Endeavour Hills",
        "meta": "Excavation and earthmoving in Endeavour Hills - sloping-site cuts, benched pads and pool digs on undulating blocks. Call 0431 529 254.",
        "hero": "Endeavour Hills lives up to its name - we handle sloping-site excavation, retaining cuts and pool digs across its undulating blocks.",
        "ov1": "Endeavour Hills is built across undulating ground, so a lot of blocks have a real fall to them. The work is sloping-site excavation, benched pads, pool cuts and footings where the dig and any retaining have to be planned together.",
        "ov2": "We plan the cut around the slope, keep the site stable through the dig, and size the machine to both the access and the fall of the land.",
        "local": "On a sloping Endeavour Hills block, the cut and the retaining are two halves of the one job - get the benching right and everything after it goes smoothly. We work to your levels, keep the batters safe, and cart off the spoil.",
        "faqs": [
            ("Do you handle sloping blocks in Endeavour Hills?", "Yes - much of Endeavour Hills is on a slope, and sloping-site excavation with benched pads is routine work for us."),
            ("Can you do the excavation and the retaining together?", "We can - on the undulating blocks here the dig and the retaining usually go hand in hand, and we can take care of both."),
            ("Do you cover Endeavour Hills and nearby Doveton?", "Yes - Endeavour Hills, Doveton and the surrounding pockets are all in our service area."),
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
    url = f"{BASE}/services/excavation-earthmoving-{sub['slug']}"
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
            "serviceType": "Excavation and Earthmoving",
            "name": f"Excavation and Earthmoving in {name}",
            "url": url,
            "provider": {"@id": f"{BASE}/#business"},
            "areaServed": area,
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": f"Excavation and Earthmoving Services in {name}",
                "itemListElement": [
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Bulk Earthmoving"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Pits"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Trenches"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Complete Excavation Services"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Small-Machine Tight-Site Access"}},
                ],
            },
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": "Services", "item": f"{BASE}/services"},
                {"@type": "ListItem", "position": 3, "name": "Excavation & Earthmoving", "item": f"{BASE}/services/excavation-earthmoving"},
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
    """Mesh-linking grid to every Excavation & Earthmoving suburb page. The active
    suburb (on its own page) renders as a non-linked gold tile."""
    tiles = []
    for s in SUBURBS:
        href = f"/services/excavation-earthmoving-{s['slug']}"
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
      <h2 class="font-display text-4xl md:text-5xl uppercase leading-[0.92] text-cream">Excavation across <span class="text-gold-400">South East Melbourne.</span></h2>
      <p class="mt-5 text-cream/70 leading-relaxed">Owner-operated earthmoving from our Keysborough base. Pick your suburb for local detail, or call Dylan direct on <a href="tel:0431529254" class="text-gold-400 hover:text-gold-300 transition">0431 529 254</a>.</p>
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
    url = f"{BASE}/services/excavation-earthmoving-{slug}"

    # -- head --
    html = rep(html,
        "<title>Excavation & Earthmoving - Charm Excavation, South East Melbourne</title>",
        f"<title>Excavation & Earthmoving {name} | Charm Excavation</title>", "title")
    html = rep(html,
        '<meta name="description" content="Bulk earthmoving, pits, trenches, complete excavation services across Melbourne\'s South East. Small-machine access for tight sites." />',
        f'<meta name="description" content="{sub["meta"]}" />', "desc")
    html = rep(html,
        '<meta name="geo.placename" content="Melbourne">',
        f'<meta name="geo.placename" content="{name}">', "geo")
    html = rep(html,
        '<link rel="canonical" href="https://charmexcavation.com.au/services/excavation-earthmoving">',
        f'<link rel="canonical" href="{url}">', "canonical")
    # open graph
    html = rep(html,
        '<meta property="og:title" content="Excavation & Earthmoving - Charm Excavation, South East Melbourne">',
        f'<meta property="og:title" content="Excavation & Earthmoving {name} - Charm Excavation">', "og:title")
    html = rep(html,
        '<meta property="og:description" content="Bulk earthmoving, pits, trenches and complete excavation across Melbourne\'s South East. Mini-ex through to 5-tonne. Small-machine access for tight sites.">',
        f'<meta property="og:description" content="{sub["meta"]}">', "og:desc")
    html = rep(html,
        '<meta property="og:url" content="https://charmexcavation.com.au/services/excavation-earthmoving">',
        f'<meta property="og:url" content="{url}">', "og:url")
    # twitter
    html = rep(html,
        '<meta name="twitter:title" content="Excavation & Earthmoving - Charm Excavation, SE Melbourne">',
        f'<meta name="twitter:title" content="Excavation & Earthmoving {name} - Charm Excavation">', "tw:title")
    html = rep(html,
        '<meta name="twitter:description" content="Bulk earthmoving, pits, trenches and complete excavation across Melbourne\'s South East.">',
        f'<meta name="twitter:description" content="Excavation and earthmoving in {name}, South East Melbourne.">', "tw:desc")

    # -- json-ld: replace the first ld+json script block --
    ld_start = html.index('<script type="application/ld+json">')
    ld_end = html.index('</script>', ld_start) + len('</script>')
    html = html[:ld_start] + json_ld(sub) + html[ld_end:]

    # -- visible breadcrumb --
    html = rep(html,
        '''    <li><a href="/services" class="hover:text-gold-400">Services</a></li>
    <li aria-hidden="true">/</li>
    <li aria-current="page" class="text-cream/90">Excavation & Earthmoving</li>''',
        f'''    <li><a href="/services" class="hover:text-gold-400">Services</a></li>
    <li aria-hidden="true">/</li>
    <li><a href="/services/excavation-earthmoving" class="hover:text-gold-400">Excavation & Earthmoving</a></li>
    <li aria-hidden="true">/</li>
    <li aria-current="page" class="text-cream/90">{name}</li>''', "breadcrumb")

    # -- hero eyebrow / label / h1 / paragraph --
    html = rep(html,
        '<div class="flex items-center gap-4 mb-6 text-xs font-sport tracking-[0.25em] uppercase text-cream/50"><a href="/services" class="hover:text-gold-400 transition">Services</a><span>/</span><span class="text-gold-400">Excavation & Earthmoving</span></div>',
        f'<div class="flex items-center gap-4 mb-6 text-xs font-sport tracking-[0.25em] uppercase text-cream/50"><a href="/services/excavation-earthmoving" class="hover:text-gold-400 transition">Excavation & Earthmoving</a><span>/</span><span class="text-gold-400">{name}</span></div>', "hero-eyebrow")
    html = rep(html,
        '<span class="font-sport text-xs tracking-[0.3em] uppercase text-gold-400">Service</span>',
        f'<span class="font-sport text-xs tracking-[0.3em] uppercase text-gold-400">{name}, SE Melbourne</span>', "hero-label")
    html = rep(html,
        '<h1 class="font-display text-5xl md:text-6xl lg:text-[6rem] leading-[0.9] uppercase text-cream">Excavation <br/>& <span class="text-gold-400">Earthmoving.</span></h1>',
        f'<h1 class="font-display text-5xl md:text-6xl lg:text-[6rem] leading-[0.9] uppercase text-cream">Excavation & Earthmoving <br/>in <span class="text-gold-400">{name}.</span></h1>', "h1")
    html = rep(html,
        '<p class="mt-8 text-lg md:text-xl text-cream/80 max-w-2xl leading-relaxed">Bulk dig-outs, pits, trenches and full-scope excavation. Small machines for tight backyards, bigger iron for volume jobs.</p>',
        f'<p class="mt-8 text-lg md:text-xl text-cream/80 max-w-2xl leading-relaxed">{sub["hero"]}</p>', "hero-p")

    # -- overview heading + paragraphs (2 -> 3, incl local knowledge) --
    html = rep(html,
        '<h2 class="font-display text-4xl md:text-5xl uppercase leading-[0.92] text-cream">Move the dirt. <br/><span class="text-burgundy-500">Move on.</span></h2>',
        f'<h2 class="font-display text-4xl md:text-5xl uppercase leading-[0.92] text-cream">Excavation in <br/><span class="text-burgundy-500">{name}.</span></h2>', "ov-head")
    html = rep(html,
        '''        <p>Excavation is where jobs bog down if you don't have the right gear. We run machines sized to the block, from mini-ex for side access through to the 5-tonne for open pads.</p>
        <p>Whether it's a pool dig, house footings, a garage pit or a full bulk cut, we turn up with the right setup, move what needs moving, and cart off what's left.</p>''',
        f'''        <p>{sub["ov1"]}</p>
        <p>{sub["ov2"]}</p>
        <p>{sub["local"]}</p>''', "ov-body")

    # -- insert FAQ + Areas before the CTA section --
    cta = '<section class="relative bg-burgundy-800 overflow-hidden">'
    html = rep(html, cta, faq_section(sub) + "\n" + areas_section(slug) + "\n" + cta, "insert-faq-areas")

    out = os.path.join(SERVICES, f"excavation-earthmoving-{slug}.html")
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


def main():
    # Build suburb pages from the clean hub first, then patch the hub itself.
    for sub in SUBURBS:
        out = build_page(sub)
        print(f"  built {os.path.basename(out)}")
    print(patch_parent())
    print(f"\nDone. {len(SUBURBS)} pages. Idempotent.")


if __name__ == "__main__":
    main()
