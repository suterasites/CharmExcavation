#!/usr/bin/env python3
"""gen_suburb_siteprep.py - build Site Preparation & Demolition x suburb pages.

Third sibling of gen_suburb_excavation.py / gen_suburb_civil.py, same method:
clone the service-level page (services/site-preparation-demolition.html) - keeping
header, footer, scripts, styles and the generic service sections verbatim - then
localise the head/schema, hero and overview, and add a suburb FAQ (with FAQPage
schema) plus an "Areas we service" mesh-linking section. Also patches the parent
service page with the same Areas section so the cluster is crawlable from the hub,
and adds every page to sitemap.xml.

Idempotent: re-running overwrites the generated pages, re-inserts the Areas section
on the parent only if missing, and skips sitemap URLs already listed. Output:
services/site-preparation-demolition-<suburb>.html

House note: compiled-Tailwind site (styles.css). Only utility classes already in
the base page are reused; the Areas/FAQ blocks lean on the page's own scoped
classes (sub-card etc.), so nothing new needs compiling.

Coverage note: the filename must carry the clients.yaml term for this service
("demolition") plus the suburb slug, or Apps/seo-hq's coverage matrix will not
count the page. site-preparation-demolition-<suburb> satisfies both, and no other
Charm service term ("excavation", "drainage", "retaining wall", "landscaping") is
a substring of it, so the cell lights for this service only.

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
PARENT = os.path.join(SERVICES, "site-preparation-demolition.html")
SITEMAP = os.path.join(ROOT, "sitemap.xml")
LASTMOD = "2026-08-28"

# ── Per-suburb data ────────────────────────────────────────────────────────
# name/slug + localised copy. No fabricated past-project claims - framed as
# service-area capability plus genuine local ground conditions and job types.
SUBURBS = [
    {
        "slug": "dandenong", "name": "Dandenong",
        "meta": "Site preparation and demolition in Dandenong, SE Melbourne. Clearing, site cuts, slab and shed demolition, pad trimmed to spec. Call 0431 529 254.",
        "hero": "Dandenong blocks are usually a knock-down or a clear-out before anything else can start, so we take the old structure off, cut the pad and trim it to level.",
        "ov1": "Around Dandenong the site prep is mostly on established blocks: old sheds, garages, concrete slabs and driveways coming out, trees and rubbish cleared, then a site cut and final trim so the new build has ground to sit on.",
        "ov2": "We are minutes away in Keysborough, so we can get a Dandenong block cleared and cut quickly, load the spoil out as we go, and hand over a pad the builder can measure off.",
        "local": "Reactive clay runs under most of Dandenong, and it swells and shrinks with the seasons. That makes the depth of the cut and the compaction under the pad matter more than they would on sand, because a pad that has been cut short moves under the slab later.",
        "faqs": [
            ("Can you demolish an old shed or garage in Dandenong?", "Yes. Sheds, garages, carports, concrete slabs and driveways all come out as part of our site prep scope across Dandenong, Dandenong North and Dandenong South, with the material loaded and taken away rather than left in a pile."),
            ("Do you do the site cut as well as the clearing?", "That is the normal job. Clear the block, cut to level, then trim the pad to spec so the concreter or the builder can start without having to bring another machine back in."),
            ("How do you deal with the clay ground around Dandenong?", "We cut to the depth on the plan rather than the depth that looks right, and compact as we go. Reactive clay moves seasonally, so a shallow cut or a soft pad shows up as a problem under the slab a year or two later."),
        ],
    },
    {
        "slug": "cranbourne", "name": "Cranbourne",
        "meta": "Site preparation in Cranbourne. Estate block clearing, site cuts and precision pad trimming, ready for the slab. Owner-operated. Call 0431 529 254.",
        "hero": "Cranbourne's estate blocks come as bare dirt with a levels plan, so the whole job is cutting them accurately and trimming the pad to the millimetre the slab needs.",
        "ov1": "Across Cranbourne, Cranbourne West, East and North the work is new-build site prep: strip the topsoil, cut the block to the levels on the plan, batter the edges and trim the pad so it hands over ready for the setout.",
        "ov2": "We work off the engineer's drawings, cart the surplus off the block rather than pushing it into a corner, and get clear so the slab crew is not waiting on us.",
        "local": "A lot of Cranbourne estate ground is fill placed by the developer over the original profile. Knowing where the fill stops and the natural ground starts is what decides how deep the cut goes and whether the pad needs anything under it.",
        "faqs": [
            ("Do you do site cuts for new builds in the Cranbourne estates?", "Yes, that is most of what we do out here. Topsoil strip, cut to the plan levels, batters and a trimmed pad, across Cranbourne and the growth estates around it."),
            ("Can you take the spoil away?", "We can. On a tight estate lot there is usually nowhere to stockpile, so carting the surplus off as we cut is normally the cleanest way to run the job."),
            ("How accurate is the final trim?", "The pad is trimmed to the levels on the engineer's plan, not eyeballed. That is the whole point of the trim: the concreter should be able to set out straight onto it."),
        ],
    },
    {
        "slug": "berwick", "name": "Berwick",
        "meta": "Site preparation and demolition in Berwick. Sloping-block cuts, batters, tree and structure clearing on hillside sites. Call Dylan on 0431 529 254.",
        "hero": "Berwick's blocks fall away, so site prep here is a cut-and-batter job: get a level pad out of sloping ground without leaving an unstable face behind it.",
        "ov1": "Berwick mixes established homes with premium builds on hillside ground. Site prep means clearing the block, working out how much comes out and where it goes, cutting a level pad into the fall, and battering or benching the cut so it holds.",
        "ov2": "On a sloping block the cut and the retaining are the same conversation, so we set the pad where it works with the wall rather than leaving a face that has to be re-dug later.",
        "local": "On a Berwick slope the cut face is the risk. Batter it too steep and it slumps in the first wet week, so the pad position, the batter angle and where any retaining wall lands all get decided together before the machine starts.",
        "faqs": [
            ("Can you cut a level pad on a sloping Berwick block?", "Yes, that is standard work here. We cut into the fall to the depth the plan needs and batter or bench the face so it stays where we put it."),
            ("Do you clear trees and old structures?", "We do. Tree and stump removal, old sheds, slabs and driveways all come out as part of the site prep, and the material goes off the block rather than into a corner of it."),
            ("Do you cover Berwick and Beaconsfield?", "Yes. Berwick, Beaconsfield, Harkaway and the pockets around them are all part of our South East Melbourne service area."),
        ],
    },
    {
        "slug": "narre-warren", "name": "Narre Warren",
        "meta": "Site preparation in Narre Warren. Backyard clearing, shed and slab demolition, pads for extensions, granny flats and sheds. Call 0431 529 254.",
        "hero": "Most Narre Warren site prep happens behind the house: clearing the back yard, taking out the old slab or shed, and cutting a pad for whatever is going up in its place.",
        "ov1": "Narre Warren is established family housing, so the work is extensions, granny flats, sheds and pools. That means backyard clearing, breaking out old concrete, removing stumps, and cutting a level pad in a space with a house on one side and a fence on the other.",
        "ov2": "We run compact machines that fit through a standard side gate, protect what stays, and take the broken concrete and green waste away instead of leaving it on the nature strip.",
        "local": "The constraint on a Narre Warren job is almost never the digging, it is the access. Whether a machine fits down the side, and where the spoil and the broken concrete go once it is out, is what decides how the job runs.",
        "faqs": [
            ("Can you get a machine into my Narre Warren backyard?", "Usually yes. Our compact excavator is sized for standard side-gate access, which covers most backyard site prep and small demolition around here."),
            ("Can you break out an old concrete slab or driveway?", "Yes. Breaking out slabs, paths and driveways, then loading and carting the broken concrete away, is part of the job rather than an extra you have to arrange."),
            ("Do you cover Narre Warren South and North?", "Yes. Narre Warren, Narre Warren South, Narre Warren North and the Fountain Gate area are all on our regular run."),
        ],
    },
    {
        "slug": "pakenham", "name": "Pakenham",
        "meta": "Site preparation and demolition in Pakenham. Estate site cuts in town, plus rural clearing, shed pads and access tracks. Call 0431 529 254.",
        "hero": "Pakenham runs from new estates to acreage, so site prep does too: accurate pad cuts in town, and clearing, shed pads and access tracks out on the fringe.",
        "ov1": "In the Pakenham estates it is new-build site prep - topsoil strip, cut to plan, batters and a trimmed pad. Out on the rural blocks it is bigger and rougher: clearing scrub and trees, forming shed and machinery pads, cutting access tracks and taking down old farm structures.",
        "ov2": "We bring the machine that suits the block, so a tight estate lot gets a compact rig and an acreage clear-out gets something that can actually move the volume.",
        "local": "The two halves of Pakenham need different things. Estate lots are about hitting the plan levels exactly on a small block; acreage is about volume, access and where the cleared material ends up, since there is usually room to place it rather than cart it.",
        "faqs": [
            ("Do you do site cuts in the Pakenham estates?", "Yes. Pakenham, Pakenham Upper and the Lakeside and Cardinia estates are part of our regular run, and estate site cuts and pad trims are everyday work."),
            ("Can you clear an acreage block or form a shed pad?", "We can. Clearing scrub and trees, forming a level shed or machinery pad and cutting an access track are all within scope out on the rural blocks."),
            ("Can the cleared material stay on the property?", "On acreage, often yes, and it is usually cheaper that way. On an estate lot there is rarely room, so it goes off the block. We work out which applies when we quote."),
        ],
    },
    {
        "slug": "officer", "name": "Officer",
        "meta": "Site preparation in Officer. Greenfield estate site cuts, topsoil strip, batters and precision pad trimming to plan. Call Dylan on 0431 529 254.",
        "hero": "Officer's estates move fast and the pad is the first thing on the critical path, so the cut has to be right and it has to be finished on the day.",
        "ov1": "Officer is largely new greenfield estates, so site prep is the clean version of the job: strip the topsoil, cut the block to the levels on the plan, form the batters and trim the pad ready for setout.",
        "ov2": "There is no demolition to work around on a fresh block, which means the whole job is accuracy and turnaround. We work off the drawings, cart the surplus, and get off the lot.",
        "local": "Greenfield ground in Officer is a blank slate, so the plan levels are the only reference there is. Accurate setout and a properly compacted pad are what stop settlement turning up under a driveway or a slab edge a year later.",
        "faqs": [
            ("Do you service the new Officer estates?", "Yes. Officer and Officer South, including the newer releases, are part of our regular South East Melbourne run."),
            ("How quickly can you turn a pad around?", "Most single estate lots are a short job once we are on site. The thing that decides the date is the machine schedule, so the earlier we know your build programme the easier it is to slot in."),
            ("Do you trim the pad or just cut it?", "Both. The cut gets you close, the trim gets you to the levels on the plan. We finish the trim so the concreter can set out straight off the pad."),
        ],
    },
    {
        "slug": "clyde", "name": "Clyde",
        "meta": "Site preparation in Clyde. Flat estate block cuts, topsoil strip and precision pad trimming, ready for the slab. Call Dylan on 0431 529 254.",
        "hero": "Clyde's blocks are flat and newly released, so there is nothing to hide behind: the pad is either on the plan levels or it is not.",
        "ov1": "Clyde is new estate land, so the site prep is topsoil strip, a cut to the plan levels, batters where the block needs them and a trimmed pad handed over ready for setout.",
        "ov2": "Flat ground sounds like the easy version, but it removes every excuse for being a bit out. We work to the drawings and check the levels before we call the pad finished.",
        "local": "Because Clyde blocks are flat and freshly released, most of what you are cutting is developer fill rather than natural ground. How deep that fill goes changes what the pad needs under it, so it is worth knowing before the machine starts.",
        "faqs": [
            ("Do you do site cuts for new builds in Clyde?", "Yes. Clyde and Clyde North estate lots are core work for us, from topsoil strip through to the finished trimmed pad."),
            ("What happens to the topsoil and the surplus?", "On a tight estate lot it normally leaves with us, because there is nowhere to stockpile it without getting in the way of the build."),
            ("Do you work to the engineer's levels?", "Always. The pad is cut and trimmed to the levels on the plan, which is what the slab and the setout depend on."),
        ],
    },
    {
        "slug": "clyde-north", "name": "Clyde North",
        "meta": "Site preparation in Clyde North. Estate site cuts, topsoil strip, batters and pad trimming across the growth corridor. Call 0431 529 254.",
        "hero": "Clyde North is one of the fastest-growing pockets in the south east, and every one of those blocks needs cutting and trimming before a slab can go down.",
        "ov1": "Clyde North is almost entirely new estate building, so the job is the same shape every time: strip the topsoil, cut the block to plan, form the batters, trim the pad. The variable is the levels, and those come off the drawings.",
        "ov2": "We run enough of these that the process is settled, which is what keeps them quick. Cut, trim, cart the surplus, off the block.",
        "local": "Clyde North estates are built on placed fill, and the depth of it varies lot to lot even within a release. That is the thing worth checking before the cut, because it changes what sits under the pad.",
        "faqs": [
            ("Do you cover the Clyde North estates?", "Yes. Clyde North is part of our regular run, and estate site cuts are the bulk of what we do out here."),
            ("Can you work in around the builder's programme?", "We try to. Site prep is early on the critical path, so the more notice we have of your slab date the easier it is to land the pad when you need it."),
            ("Do you handle the batters as well?", "Yes. Where a block needs battering or benching to hold the cut, that is formed as part of the same job rather than left for someone else."),
        ],
    },
    {
        "slug": "frankston", "name": "Frankston",
        "meta": "Site preparation and demolition in Frankston. Sandy-ground site cuts, clearing, slab and shed demolition. Owner-operated. Call 0431 529 254.",
        "hero": "Frankston ground is sandy and it does not hold a face, so the cut has to be planned around what the block will actually stand up in.",
        "ov1": "Frankston work is a mix: knock-down rebuilds on established blocks needing old slabs, sheds and driveways removed, and site cuts on sandy ground where the batter has to be laid back further than it would be in clay.",
        "ov2": "We clear the block, cut the pad, batter it to something that stays put, and take the demolition material away rather than leaving it for someone else to deal with.",
        "local": "Sand is the thing that catches people out around Frankston. It digs easily, which makes the cut quick, but it will not hold a steep face, so a batter that would be fine in Dandenong clay will slump here.",
        "faqs": [
            ("Do you do knock-down site prep in Frankston?", "Yes. Removing old slabs, sheds, garages and driveways, clearing the block and then cutting the pad is a normal job for us across Frankston and the surrounding suburbs."),
            ("Does the sandy ground change how you cut a block?", "It does. Sand will not hold a steep batter, so the face gets laid back further and the cut is set out with that in mind rather than discovering it halfway through."),
            ("Do you cover Frankston South and Seaford?", "Yes. Frankston, Frankston South, Frankston North, Seaford and the surrounding pockets are all in our service area."),
        ],
    },
    {
        "slug": "hallam", "name": "Hallam",
        "meta": "Site preparation and demolition in Hallam. Industrial and residential clearing, slab removal, site cuts and pad trimming. Call 0431 529 254.",
        "hero": "Hallam is half housing and half industrial estate, so site prep here runs from a backyard shed pad up to clearing a commercial hardstand.",
        "ov1": "On the residential side of Hallam it is extensions, sheds and knock-downs: clearing, breaking out concrete and cutting a pad. On the industrial side it is bigger areas, old hardstand and slabs coming out, and levels that have to work for a warehouse floor or a truck apron.",
        "ov2": "We scale the machine to the job and work in with the site manager on the commercial ones, so we are off the site rather than holding up the trades behind us.",
        "local": "Hallam's industrial pockets sit on ground that has already been worked once, so there is usually old slab, footing or fill in the way. Finding that early is what keeps a site cut from turning into a much bigger job midway through.",
        "faqs": [
            ("Do you do commercial and industrial site prep in Hallam?", "Yes. Clearing, breaking out old hardstand and slabs, and cutting to the levels a commercial floor needs are all within our scope, and we coordinate with the site manager so we are in and out."),
            ("Can you remove an old concrete slab?", "Yes. Breaking out, loading and carting away slabs, hardstand and driveways is part of the demolition side of what we do."),
            ("Do you cover Hallam and Hampton Park?", "Yes. Hallam, Hampton Park, Doveton and Endeavour Hills are all part of our regular South East Melbourne run."),
        ],
    },
    {
        "slug": "hampton-park", "name": "Hampton Park",
        "meta": "Site preparation in Hampton Park. Backyard clearing, shed and slab demolition, and pads for extensions and granny flats. Call 0431 529 254.",
        "hero": "Hampton Park blocks are standard family lots, so the site prep is nearly always behind the house and nearly always through a side gate.",
        "ov1": "Hampton Park work is extensions, granny flats, sheds and pools on established blocks. Clearing the back yard, taking out old concrete and stumps, and cutting a level pad in a confined space is the shape of most jobs.",
        "ov2": "Compact machines get down the side, we protect what stays, and the broken concrete and green waste leave with us rather than sitting on the nature strip waiting for a skip.",
        "local": "Hampton Park sits on the same reactive clay as most of the corridor, so a pad that has not been cut deep enough or compacted properly will move once the seasons turn. It is worth getting right before something gets built on it.",
        "faqs": [
            ("Can you fit a machine down the side of my Hampton Park house?", "Usually yes. Our compact excavator is sized for standard side-gate access, which covers most backyard site prep around here."),
            ("Can you take out stumps and old concrete?", "Yes. Stumps, slabs, paths and driveways all come out, and the material is loaded and carted rather than left on site."),
            ("Do you cut pads for granny flats and sheds?", "That is a common job for us. We cut and trim the pad to the levels your plan calls for, ready for the slab or the shed to go straight on."),
        ],
    },
    {
        "slug": "endeavour-hills", "name": "Endeavour Hills",
        "meta": "Site preparation and demolition in Endeavour Hills. Sloping-block cuts, batters, clearing and slab removal on established sites. Call 0431 529 254.",
        "hero": "Endeavour Hills is built across a rise, so most site prep here is cutting a level pad out of a block that does not start level.",
        "ov1": "Endeavour Hills is established housing on undulating ground. That means clearing mature gardens and old structures, breaking out concrete, and cutting a level pad into a slope, with a batter or a bench to hold the face behind it.",
        "ov2": "Because the blocks fall, the cut and any retaining have to be planned together. We set the pad where it works with the wall rather than leaving a face that gets re-dug later.",
        "local": "The gardens are the complication in Endeavour Hills. These are older blocks with mature trees and established landscaping, so the access route in and what you are prepared to lose on the way through usually shapes the job more than the dig itself.",
        "faqs": [
            ("Can you cut a level pad on a sloping Endeavour Hills block?", "Yes. Cutting into the fall and battering or benching the face is standard work on the blocks up here."),
            ("Can you work around established trees and gardens?", "Where we can, yes. We plan the access route and the machine size around what has to stay, and we will tell you upfront if something is genuinely in the way."),
            ("Do you remove old sheds and slabs?", "Yes. Sheds, garages, slabs, paths and driveways all come out as part of the site prep, with the material carted away."),
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
    url = f"{BASE}/services/site-preparation-demolition-{sub['slug']}"
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
            "serviceType": "Site Preparation and Demolition",
            "name": f"Site Preparation and Demolition in {name}",
            "url": url,
            "provider": {"@id": f"{BASE}/#business"},
            "areaServed": area,
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": f"Site Preparation and Demolition Services in {name}",
                "itemListElement": [
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Site Clearing"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Site Cuts"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Precision Final Trim"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Demolition"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Concrete and Slab Removal"}},
                ],
            },
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": "Services", "item": f"{BASE}/services"},
                {"@type": "ListItem", "position": 3, "name": "Site Prep & Demolition", "item": f"{BASE}/services/site-preparation-demolition"},
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
    """Mesh-linking grid to every Site Prep & Demolition suburb page. The active
    suburb (on its own page) renders as a non-linked gold tile."""
    tiles = []
    for s in SUBURBS:
        href = f"/services/site-preparation-demolition-{s['slug']}"
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
      <h2 class="font-display text-4xl md:text-5xl uppercase leading-[0.92] text-cream">Site prep across <span class="text-gold-400">South East Melbourne.</span></h2>
      <p class="mt-5 text-cream/70 leading-relaxed">Owner-operated clearing, site cuts and demolition from our Keysborough base. Pick your suburb for local detail, or call Dylan direct on <a href="tel:0431529254" class="text-gold-400 hover:text-gold-300 transition">0431 529 254</a>.</p>
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
    url = f"{BASE}/services/site-preparation-demolition-{slug}"
    title = f"Site Prep & Demolition {name} | Charm Excavation"

    # Head lengths are audited (title 40-65, meta description 120-170 in
    # Apps/sutera-seo/checklist.py) - fail the build rather than ship a warn.
    if not 40 <= len(title) <= 65:
        raise SystemExit(f"[{slug}] title is {len(title)} chars (need 40-65): {title}")
    if not 120 <= len(sub["meta"]) <= 170:
        raise SystemExit(f"[{slug}] meta description is {len(sub['meta'])} chars (need 120-170)")

    # -- head --
    html = rep(html,
        "<title>Site Preparation & Demolition | Charm Excavation, SE Melbourne</title>",
        f"<title>{title}</title>", "title")
    html = rep(html,
        '<meta name="description" content="Site preparation, cuts, precision trimming and demolition across Melbourne\'s South East. Pad-ready ground so the next trade doesn\'t lose a day." />',
        f'<meta name="description" content="{sub["meta"]}" />', "desc")
    html = rep(html,
        '<meta name="geo.placename" content="Melbourne">',
        f'<meta name="geo.placename" content="{name}">', "geo")
    html = rep(html,
        '<link rel="canonical" href="https://charmexcavation.com.au/services/site-preparation-demolition">',
        f'<link rel="canonical" href="{url}">', "canonical")
    # open graph
    html = rep(html,
        '<meta property="og:title" content="Site Preparation & Demolition - Charm Excavation, South East Melbourne">',
        f'<meta property="og:title" content="Site Prep & Demolition {name} - Charm Excavation">', "og:title")
    html = rep(html,
        '<meta property="og:description" content="Site preparation, site cuts, precision final trimming and demolition across Melbourne\'s South East. Pad-ready ground so the next trade doesn\'t lose a day.">',
        f'<meta property="og:description" content="{sub["meta"]}">', "og:desc")
    html = rep(html,
        '<meta property="og:url" content="https://charmexcavation.com.au/services/site-preparation-demolition">',
        f'<meta property="og:url" content="{url}">', "og:url")
    # twitter
    html = rep(html,
        '<meta name="twitter:title" content="Site Preparation & Demolition - Charm Excavation, SE Melbourne">',
        f'<meta name="twitter:title" content="Site Prep & Demolition {name} - Charm Excavation">', "tw:title")
    html = rep(html,
        '<meta name="twitter:description" content="Site preparation, cuts, precision trimming and demolition across Melbourne\'s South East.">',
        f'<meta name="twitter:description" content="Site clearing, cuts, precision trimming and demolition in {name}, South East Melbourne.">', "tw:desc")

    # -- json-ld: replace the first ld+json script block --
    ld_start = html.index('<script type="application/ld+json">')
    ld_end = html.index('</script>', ld_start) + len('</script>')
    html = html[:ld_start] + json_ld(sub) + html[ld_end:]

    # -- visible breadcrumb --
    html = rep(html,
        '''    <li><a href="/services" class="hover:text-gold-400">Services</a></li>
    <li aria-hidden="true">/</li>
    <li aria-current="page" class="text-cream/90">Site Prep & Demolition</li>''',
        f'''    <li><a href="/services" class="hover:text-gold-400">Services</a></li>
    <li aria-hidden="true">/</li>
    <li><a href="/services/site-preparation-demolition" class="hover:text-gold-400">Site Prep & Demolition</a></li>
    <li aria-hidden="true">/</li>
    <li aria-current="page" class="text-cream/90">{name}</li>''', "breadcrumb")

    # -- hero eyebrow / label / h1 / paragraph --
    html = rep(html,
        '<div class="flex items-center gap-4 mb-6 text-xs font-sport tracking-[0.25em] uppercase text-cream/50"><a href="/services" class="hover:text-gold-400 transition">Services</a><span>/</span><span class="text-gold-400">Site Prep & Demolition</span></div>',
        f'<div class="flex items-center gap-4 mb-6 text-xs font-sport tracking-[0.25em] uppercase text-cream/50"><a href="/services/site-preparation-demolition" class="hover:text-gold-400 transition">Site Prep & Demolition</a><span>/</span><span class="text-gold-400">{name}</span></div>', "hero-eyebrow")
    html = rep(html,
        '<span class="font-sport text-xs tracking-[0.3em] uppercase text-gold-400">Service</span>',
        f'<span class="font-sport text-xs tracking-[0.3em] uppercase text-gold-400">{name}, SE Melbourne</span>', "hero-label")
    html = rep(html,
        '<h1 class="font-display text-5xl md:text-6xl lg:text-[6rem] leading-[0.9] uppercase text-cream">Site Prep <br/>& <span class="text-gold-400">Demolition.</span></h1>',
        f'<h1 class="font-display text-5xl md:text-6xl lg:text-[6rem] leading-[0.9] uppercase text-cream">Site Prep & Demolition <br/>in <span class="text-gold-400">{name}.</span></h1>', "h1")
    html = rep(html,
        '<p class="mt-8 text-lg md:text-xl text-cream/80 max-w-2xl leading-relaxed">Clear it, cut it, trim it to spec. We get the ground ready so the next trade can start clean.</p>',
        f'<p class="mt-8 text-lg md:text-xl text-cream/80 max-w-2xl leading-relaxed">{sub["hero"]}</p>', "hero-p")

    # -- overview heading + paragraphs (2 -> 3, incl local knowledge) --
    html = rep(html,
        '<h2 class="font-display text-4xl md:text-5xl uppercase leading-[0.92] text-cream">Ready ground, <br/><span class="text-burgundy-500">no surprises.</span></h2>',
        f'<h2 class="font-display text-4xl md:text-5xl uppercase leading-[0.92] text-cream">Site prep in <br/><span class="text-burgundy-500">{name}.</span></h2>', "ov-head")
    html = rep(html,
        '''        <p>Site prep is the first job on most builds and the one that costs the most time if it gets done wrong. We run an owner-operated rig with the right machines for the site, from tight backyards through to multi-unit pads.</p>
        <p>Clear the trees and rubbish, cut to level, trim the pad to spec. You get the ground the builder expected, on the day they expected, with a tidy site to hand over.</p>''',
        f'''        <p>{sub["ov1"]}</p>
        <p>{sub["ov2"]}</p>
        <p>{sub["local"]}</p>''', "ov-body")

    # -- insert FAQ + Areas before the CTA section --
    cta = '<section class="relative bg-burgundy-800 overflow-hidden">'
    html = rep(html, cta, faq_section(sub) + "\n" + areas_section(slug) + "\n" + cta, "insert-faq-areas")

    out = os.path.join(SERVICES, f"site-preparation-demolition-{slug}.html")
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
    <loc>{BASE}/services/site-preparation-demolition</loc>"""
    if anchor not in xml:
        raise SystemExit("sitemap: parent site-preparation-demolition entry not found")
    end = xml.index("</url>", xml.index(anchor)) + len("</url>\n")

    added = []
    block = ""
    for s in SUBURBS:
        loc = f"{BASE}/services/site-preparation-demolition-{s['slug']}"
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
