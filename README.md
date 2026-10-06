# Forbes Riley website

Static brand site rebuilt from the Forbes Factor Website Archive (Drive), following the
"Forbes Factor Rebuild Blueprint": 10 pages plus a journal, not a 77-page WordPress clone.

## Build

    python3 build.py        # -> dist/  (deploy this folder to Vercel, Netlify, GitHub Pages, any host)

Pages live in `src/pages/*.html` (body only; the first comment line sets title, description and nav key).
Shared header/footer are in `src/partials/`, styles in `src/style.css`, photos in `src/img/`.

## Before launch

- Contact form: point the `action` in `src/pages/contact.html` at a real endpoint (Formspree, Netlify Forms, CRM).
- Newsletter form posts to pitchsecretstraining.com; confirm the field names it expects.
- Events page: fill in confirmed dates for Forbes Factor Live, FRedX and Momentum X.
- Shop link goes to shop.forbesriley.com; confirm the live store URL.
- Social links are placeholders (facebook/instagram/youtube handles); confirm.
- Photos are web-sized copies from the old site. Full-size originals are in the Drive Photos folder (zips by year).
- The old forbesfactor.com is compromised (redirects to a fake "Apple update" scam page). Do not link to it; set up redirects from it once this site is live.
