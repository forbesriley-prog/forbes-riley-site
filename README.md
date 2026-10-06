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

## Before launch

- Contact form: point the `action` in `src/pages/contact.html` at a real endpoint (Formspree, Netlify Forms, CRM).
- Newsletter form posts to pitchsecretstraining.com; confirm the field names it expects.
- Events page: fill in confirmed dates for Forbes Factor Live, FRedX and Momentum X.
- Shop links go to shopforbesriley.com (the live Shopify store). It currently shows a Shopify password page; that is a setting in the Shopify admin (Online Store > Preferences > Password protection).
- Social links are placeholders (facebook/instagram/youtube handles); confirm.
- Photos are web-sized copies from the old site. Full-size originals are in the Drive Photos folder (zips by year).
- The old forbesfactor.com is compromised (redirects to a fake "Apple update" scam page). Do not link to it; set up redirects from it once this site is live.
