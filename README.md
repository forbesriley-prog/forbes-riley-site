# Forbes Riley website

Static brand site rebuilt from the Forbes Factor Website Archive (Drive). Ten designed pages,
plus every one of the old site's 263 blog posts (Journal, searchable) and all 77 old pages (Old site archive),
so nothing from forbesfactor.com is lost.

## Live

https://forbesriley-prog.github.io/forbes-riley-site/ (GitHub Pages, repo github.com/forbesriley-prog/forbes-riley-site, served from `docs/`).
To publish changes: `python3 build.py && rm -rf docs && cp -R dist docs && touch docs/.nojekyll`, commit, push.
To use the real domain: repo Settings > Pages > Custom domain, then point the domain's DNS at GitHub Pages.

## Build

    python3 build.py        # -> dist/  (deploy this folder to Vercel, Netlify, GitHub Pages, any host)

`gen_archive.py` turns `archive/posts.json`, `archive/pages.json` and `archive/featured.json` (pulled from the old
site's WordPress API) into `journal-*.html`, `archive-*.html`, `journal.html` and `archive.html`. Post images are
web-sized copies in `src/postimg/` (about 150 MB); originals are in the Drive Photos zips.

Pages live in `src/pages/*.html` (body only; the first comment line sets title, description and nav key).
Shared header/footer are in `src/partials/`, styles in `src/style.css`, photos in `src/img/`.

## Status (8 Oct 2026)

Live and complete. Everything from the old forbesfactor.com is on the new site (247 real posts, 71 real pages;
template/filler junk from the old theme was dropped and is kept only as text in `archive/`).

Done:
- Contact form delivers by opening a prefilled email to support@teamforbesriley.com (no third-party service needed).
  If the team later wants submissions stored, point the form `action` at Formspree/Netlify Forms and remove the mailto script.
- Events: Forbes Factor Live links to the live ticket page; the free Sunday masterclass links to pitchsecretstraining.com.
- Shop links go to shopforbesriley.com (live Shopify store). It shows a Shopify password page until they switch that off
  in Shopify admin (Online Store > Preferences > Password protection).
- Logos, favicon, real social links, book and masterclass sections.

Only things left are on Forbes' side:
- Put the site on the real domain: GitHub repo Settings > Pages > Custom domain, then point the domain's DNS at GitHub Pages.
- Approve or rewrite the two-paragraph intro on "The Road to Joshua" (src/overrides/19630.html) and delete its "written in 2026" note.
- Confirm FRedX / Momentum X dates when they exist (src/pages/events.html).
- The old forbesfactor.com is compromised (redirects to a scam page). Once the new domain is live, redirect the old one to it.
