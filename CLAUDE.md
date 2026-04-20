# CLAUDE.md - Charm Excavation

## Business Context

**Business Name:** Charm Excavation
**Owner:** Dylan
**Phone:** 0431 529 254
**Email:** Dylan@charmexcavation.com.au
**Domain:** charmexcavation.com.au (owned, no live site yet)
**Location:** Keysborough, South East Melbourne
**Instagram:** @charmexcavation

### About
- 10 years experience in the industry, running solo as Charm Excavation for 3 years
- Based in Keysborough, services South East Melbourne region
- Referred by Kosta at Apollo Earthworks (Sutera client) on 2026-04-19
- Came in through Instagram DM, moved to phone on 2026-04-20
- Budget-conscious: explicitly stated he does not have $400/month to spend - package was reshaped as $100/month website + optional 2-week free Ads trial with phased ad spend
- Deal on the table: $100/month website subscription, 6-month lock-in understood. One-off build offered at $1,100 (50/50 split) as alternative.

### Services (from Instagram, grouped into 4 parent categories for homepage)

**1. Site Preparation & Demolition**
- Site Preparation & Cuts
- Precision Final Trimming
- Demolition & Site Clearing

**2. Excavation & Earthmoving**
- Bulk Earthmoving & Excavation
- Complete Excavation Services

**3. Civil & Drainage**
- Civil Construction Services
- Drainage Installation & Solutions
- Retaining Wall Construction

**4. Landscaping & Rural**
- Landscaping & Earthworks
- Rural & Agricultural Projects

### Mockup Brief
- Sourced from Dylan's Instagram content (no assets to send - James is pulling from @charmexcavation)
- Logo will be dropped into `Assets/` by James before design starts
- Design the site around the logo's colour palette - do not invent brand colours
- Service grid: 4 parent cards, each expanding or listing sub-services underneath
- Tone: clean, professional, local earthworks. Not corporate/civil-mining heavy (that's TRS). Closer to Apollo in feel since Dylan came via Kosta.
- Core pages for v1 mockup: homepage only (hero, about, services grid, gallery, contact/CTA)
- Contact: click-to-call (0431 529 254), email (Dylan@charmexcavation.com.au), Formspree contact form (same pattern as Apollo)
- Service area: South East Melbourne + surrounds (confirm with Dylan after mockup)

### Delivery Target
- Mockup due by **end of day 2026-04-20** (promised in email 10:16 AM)

---

## Always Do First
- **Invoke the `frontend-design` skill** before writing any frontend code, every session, no exceptions.

## Reference Images
- If a reference image is provided: match layout, spacing, typography, and color exactly. Swap in placeholder content (images via `https://placehold.co/`, generic copy). Do not improve or add to the design.
- If no reference image: design from scratch with high craft (see guardrails below).
- Screenshot your output, compare against reference, fix mismatches, re-screenshot. Do at least 2 comparison rounds. Stop only when no visible differences remain or user says so.

## Local Server
- **Always serve on localhost** - never screenshot a `file:///` URL.
- Start the dev server: `node serve.mjs` (serves the project root at `http://localhost:3000`)
- `serve.mjs` lives in the project root. Start it in the background before taking any screenshots.
- If the server is already running, do not start a second instance.

## Screenshot Workflow
- Puppeteer is installed at `C:/Users/nateh/AppData/Local/Temp/puppeteer-test/`. Chrome cache is at `C:/Users/nateh/.cache/puppeteer/`.
- **Always screenshot from localhost:** `node screenshot.mjs http://localhost:3000`
- Screenshots are saved automatically to `./temporary screenshots/screenshot-N.png` (auto-incremented, never overwritten).
- Optional label suffix: `node screenshot.mjs http://localhost:3000 label` saves as `screenshot-N-label.png`
- After screenshotting, read the PNG from `temporary screenshots/` with the Read tool.
- When comparing, be specific: "heading is 32px but reference shows ~24px", "card gap is 16px but should be 24px"

## Output Defaults
- Single `index.html` file, all styles inline, unless user says otherwise
- Tailwind CSS via CDN: `<script src="https://cdn.tailwindcss.com"></script>`
- Placeholder images only where no real asset is available
- Mobile-first responsive

## Brand Assets
- Always check the `Assets/` folder before designing. It will contain the logo and Dylan's job photos sourced from Instagram.
- Extract brand colours from the logo. Do not use default Tailwind palette colours.
- If a logo is present, use it. Do not invent a new one.

## Anti-Generic Guardrails
- **Colors:** Never use default Tailwind palette (indigo-500, blue-600, etc.). Pick a custom brand color from Dylan's logo and derive from it.
- **Shadows:** Never use flat `shadow-md`. Use layered, color-tinted shadows with low opacity.
- **Typography:** Never use the same font for headings and body. Pair a display/serif with a clean sans. Apply tight tracking (`-0.03em`) on large headings, generous line-height (`1.7`) on body.
- **Gradients:** Layer multiple radial gradients. Add grain/texture via SVG noise filter for depth.
- **Animations:** Only animate `transform` and `opacity`. Never `transition-all`. Use spring-style easing.
- **Interactive states:** Every clickable element needs hover, focus-visible, and active states.
- **Images:** Add a gradient overlay (`bg-gradient-to-t from-black/60`) and a color treatment layer with `mix-blend-multiply`.
- **Spacing:** Use intentional, consistent spacing tokens, not random Tailwind steps.
- **Depth:** Surfaces should have a layering system (base, elevated, floating), not all sit at the same z-plane.

## Hard Rules
- Do not add sections, features, or content not in the brief
- Do not "improve" a reference design, match it
- Do not stop after one screenshot pass
- Do not use `transition-all`
- Do not use default Tailwind blue/indigo as primary color
- Do not use em dashes or en dashes anywhere. Use regular hyphens (-) instead.
