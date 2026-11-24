# Inner Circle Black Friday page: handoff (updated Nov 24, 2026)

Live: https://site.forbesrileyhq.com/inner-circle.html

**Nov 24, 2026: the refactor from branch `inner-circle-cro` is LIVE** (Katrina: "deploy it"). Sections 11-21 below describe the OLD page (envelope, gifts, ledger) and are kept for history. The live page is the 14-section version: static hero ("You're too talented to still be stuck."), $1,500 annual only, lifetime card hidden behind `CFG.lifetimeEnabled`, one deadline in `CFG` (Mon Nov 30 2026 11:59 PM ET, still unconfirmed), checkout URLs empty so the button opens the 3-question application, GA4/GTM id still to paste at the marked comment, `icPurchase()` for confirmation pages. QA captures: `marketing/qa/inner-circle/`.
Source: `src/standalone/inner-circle.html` (one self-contained file: CSS, HTML, JS). Build with `python3 build.py`, copy `dist` to `docs`, commit, push to `main`. GitHub Pages serves `docs`. Takes 1-3 minutes to go live.
Replaces: https://forbesrileymembership.com/your-invitation
Brand rules: `marketing/FORBES-RILEY-BRAND-BRIEF.md` and https://site.forbesrileyhq.com/brand.html

## The brief from Katrina (in her words)
Forbes is APPLE. Big, a brand, frosted, hip, gold, sleek. This is her private group that pays big bucks to meet with her weekly. It's Black Friday and we have a deal. Interactive things pop on as you get them, gifts unwrap. High value, LOW cost. It's not about your pitch, it's about a COMMUNITY. Nobody reads paragraphs. Never cover Forbes' face. Cutouts can't float in a black void.

## What is on the page, top to bottom
1. Opening invitation overlay: black envelope with the gold Pitch Queen seal, Forbes "shush" cutout beside it. Tap: flap opens, cream card rises ("You're invited."), confetti, Accept button. Shows once per visit.
2. Sticky bar: SALE, $5,000 struck, $1,500, countdown, Get it NOW.
3. Hero: lockup pill, "Be in the room with Forbes. Every week.", four chips, Black Friday deal pill, Get it NOW, leopard heart cutout fading at the waist.
4. "Does this sound like you?": four tap-to-say-yes cards (next step, accountability, building alone, Forbes herself); tally answers back; Forbes in the chair on the right.
5. Video: her keynote speaker reel (YouTube t52E3asvjsw) behind a frame that splits open. The Inner Circle Promo (Vimeo 890473160) is the other option.
6. White chapter: "Inside the Inner Circle, you'll get:" list pops in one line at a time, then "It's the room. It's the people." reveal (room photo, BREAKTHRU as the monthly gathering).
7. Three laptops (ChatGPT art, transparent): Inner Circle LIVE, Pitch Video Review (no Forbes, team notes), Elevate Course Hub. Pods block (accountability, feedback loop, dashboard). Stats.
8. Gifts: Forbes pointing at "Four gifts. Tap to unwrap." beside a 2x2 of frosted wrapped cards (room photo, Pods, private group, Social Media Review laptop).
9. Value ledger adding up to $23,780, then "Black Friday price $1,500" bar.
10. Price card, week calendar (Mon-Thu + monthly BREAKTHRU + daily challenges bar), member quotes, Forbes' letter, FAQ, final "Get it NOW." with countdown, footer, quiz modal (mailto assistant@theforbesfactor.com).

## Numbers used (from the old page)
Values: LIVE $5,200; Pitch Video Review $500; Course Hub $4,500; Pods $580; Social Media Review $500; private group $500; 12 BREAKTHRUs $12,000. Total $23,780. "Normal price $5,000" is the old page's claim. Black Friday price $1,500 is Katrina's. Countdown ends Mon Nov 30, 2026 11:59 PM ET (assumed, not confirmed).

## CRO pass (Nov 23 night, branch `inner-circle-cro`; merged and published Nov 24)
Hero "You're too talented to still be stuck." with ?h=a/b/c variants, campaign line "Don't buy more stuff. Buy yourself a better year.", two plans ($1,500 year / $3,000 lifetime) with a `CHECKOUT` config in the script (fill the two URLs and the buttons go to checkout), tracking layer (dataLayer/gtag events + UTMs; paste a GA4/GTM id at the marked comment), WebP images (12.3 MB -> 1.3 MB), palette per the brief, the `.flip` class clash fixed (that was the real "black on black"). To publish: merge the branch, `python3 build.py`, copy dist to docs, push.

## Still needs a human decision
- Confirm $1,500 and the end date/time.
- Which video in the "Meet Forbes" slot: speaker reel (current) or the Inner Circle Promo.
- The old page's "letter video" and testimonial video were never found as files; only the promo's Vimeo id (890473160) is known.
- SpinGym page (`src/standalone/spingym-bf.html`, live at /spingym-bf.html): needs the sale price, old price is $45, the deal line, the end date (hidden `#ends` span, `data-date`), and the shop has no SpinGym sale set up yet. Buy buttons already go to shopforbesriley.com by colour.

## Katrina rejected tonight (do not bring back)
Crown/throne BREAKTHRU art ("the crown is dumb"); hand-drawn laptop screens; mirrored (flipped) cutouts; floor reflections ("why is one upside down"); flat black doors on the video; paragraphs in the hero; CSS gift boxes on stands; black boxes around laptops; white fringe on cutouts; tiny Forbes floating in black; the invitation card rising off the top of the screen.

## Assets
- Her 8 ChatGPT cutouts: `src/img/px/cut-new-01..08.png` (01 pointing, 02 mic, 03 tee shrug, 04 leopard at table, 05 leopard heart, 06 call-me, 07 shush, 08 chair). Originals in `~/Downloads/Forbes_Riley_8_Cutouts`.
- Laptops: `src/img/ic/live.png, review.png, hub.png, social.png` (ChatGPT chat "Generate Laptop Mockup Image"; key off black with a flood fill from the border, cut at the metal base).
- Seal: `src/img/cut/seal.png`. Room photo: `src/img/ic/room-crop.jpg` (the full promo thumbnail has Vimeo's play button baked in). Reel thumbnail: `src/img/ic/reel.jpg`.
- Older sections/variants: `src/standalone/mock-a/b/c.html` (unused, can be deleted).

## Known gotchas
- `#invite[hidden]{display:none}` must stay or the overlay blocks return visits.
- The quote marquee uses class `.q`; don't reuse `.q` elsewhere. The gifts section uses `.bf`; the top bar uses `.sale`.
- The page sets `color-scheme: only light`; if Katrina sees black text on black in the white sections, it's a dark-mode browser extension, not the page.
