"""Generate pages for every old blog post and every old WordPress page.

Reads archive/posts.json, archive/pages.json, archive/categories.json (pulled from the
old forbesfactor.com API) and returns {filename: body_html, ...} plus the Journal index
and the old-site archive index. build.py wraps each body in the site header/footer.

Images are rewritten to postimg/<year>/<month>/<file> (copies in src/postimg, downloaded
from the old site and resized). If a copy is missing the <img> removes itself on error.
"""
import html as H
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
ARCH = ROOT / "archive"

JUNK = re.compile(r"odd future|sugar plum|lorem ipsum|wes anderson|macaroon candy|meggings|jean shorts cred|dolor sit amet|construction of europe|realm of asia|natural beauty of asia|harmony of wild africa|human compassion binds|take an adventure|fellow travelers|biggest adventure of them all|avada|click edit button|consectetur", re.I)
EXCLUDE_PAGES = {"typography", "tabs", "promotion-boxes", "home-version-18", "home-3-2-2-2-2", "test-blog-sidebar-mr"}


def is_template(p):
    t = H.unescape(p["title"]["rendered"]).strip()
    return t.upper().startswith("#TEMPLATE") or not t or p["slug"] == "fitness-interview-honeycutt"


posts = [p for p in json.load(open(ARCH / "posts.json")) if not is_template(p)]
pages = [p for p in json.load(open(ARCH / "pages.json")) if p["slug"] not in EXCLUDE_PAGES and not is_template(p)]
cats = {c["id"]: c for c in json.load(open(ARCH / "categories.json"))}
featured = json.load(open(ARCH / "featured.json")) if (ARCH / "featured.json").exists() else {}


def featured_img(p):
    u = featured.get(str(p["id"]))
    if not u:
        return None
    loc = local_img(u)
    return loc if loc and (ROOT / "src" / loc).exists() else None


def thumb(p):
    return featured_img(p) or first_image(p["content"]["rendered"])

POST_FILE = {p["slug"]: f"journal-{p['slug']}.html" for p in posts}
PAGE_FILE = {p["slug"]: f"archive-{p['slug']}.html" for p in pages}

# Old page slugs that now have a proper new page.
PAGE_REDIRECT = {
    "about-forbes": "about.html", "meet-forbes-3-3": "about.html", "meet-forbes-3-4": "about.html",
    "meet-forbes-4": "about.html", "meet-forbes-3-2": "about.html", "work-with-forbes": "work-with-forbes.html",
    "speaking-3": "work-with-forbes.html", "about-spingym-2": "spingym.html", "spingym": "spingym.html",
    "forbes-factor-live": "events.html", "healthy-living": "health.html", "recipes": "health.html",
    "business": "business.html", "press": "press.html", "media-kit": "press.html",
}

IMG_RE = re.compile(r'<img\b[^>]*>', re.I)


def local_img(src):
    src = src.split("?")[0]
    if "forbesfactor.com/wp-content/uploads/" not in src:
        return None
    rel = src.split("/wp-content/uploads/")[1]
    rel = re.sub(r"-\d+x\d+(\.\w+)$", r"\1", rel)
    return "postimg/" + rel


def first_image(content):
    for m in IMG_RE.finditer(content):
        s = re.search(r'src="([^"]+)"', m.group(0))
        if s:
            loc = local_img(s.group(1))
            if loc and (ROOT / "src" / loc).exists():
                return loc
    return None


def rewrite_img(m):
    tag = m.group(0)
    s = re.search(r'src="([^"]+)"', tag)
    alt = re.search(r'alt="([^"]*)"', tag)
    if not s:
        return ""
    loc = local_img(s.group(1))
    if not loc:
        return ""  # third-party hotlinked image: drop
    a = alt.group(1) if alt else ""
    return f'<img src="{loc}" alt="{H.escape(a)}" loading="lazy" onerror="this.remove()">'


def rewrite_link(m):
    href, inner = m.group(1), m.group(2)
    if "forbesfactor.com" in href:
        slug = href.rstrip("/").split("/")[-1].split("?")[0].split("#")[0]
        if slug in POST_FILE:
            return f'<a href="{POST_FILE[slug]}">{inner}</a>'
        if slug in PAGE_REDIRECT:
            return f'<a href="{PAGE_REDIRECT[slug]}">{inner}</a>'
        if slug in PAGE_FILE:
            return f'<a href="{PAGE_FILE[slug]}">{inner}</a>'
        if "/wp-content/uploads/" in href:
            return inner  # link to an image file: keep the image, drop the link
        return inner
    if href.startswith("#"):
        return inner
    return f'<a href="{H.escape(href, quote=True)}" target="_blank" rel="noopener">{inner}</a>'


def sanitize(content):
    c = content
    c = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", "", c, flags=re.S | re.I)
    c = re.sub(r"<!--.*?-->", "", c, flags=re.S)
    # Embedded video -> link card
    def embed(m):
        src = m.group(1)
        yt = re.search(r"(?:youtube\.com/embed/|youtu\.be/|youtube\.com/watch\?v=)([\w-]+)", src)
        if yt:
            return f'<p class="embed-card"><a href="https://www.youtube.com/watch?v={yt.group(1)}" target="_blank" rel="noopener">&#9654; Watch the video on YouTube</a></p>'
        return f'<p class="embed-card"><a href="{H.escape(src, quote=True)}" target="_blank" rel="noopener">Open embedded content</a></p>'
    c = re.sub(r'<iframe\b[^>]*src="([^"]+)"[^>]*>.*?</iframe>', embed, c, flags=re.S | re.I)
    c = re.sub(r"\[/?(fusion_[a-z_]*|layerslider|rev_slider|caption|gallery)[^\]]*\]", "", c)
    c = re.sub(r'(?<!["\w])https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+)\S*', r'<a class="embed-card" href="https://www.youtube.com/watch?v=\1" target="_blank" rel="noopener">&#9654; Watch the video on YouTube</a>', c)
    c = IMG_RE.sub(rewrite_img, c)
    c = re.sub(r'<a\b[^>]*href="([^"]*)"[^>]*>(.*?)</a>', rewrite_link, c, flags=re.S | re.I)
    c = re.sub(r"<a\b[^>]*>(.*?)</a>", r"\1", c, flags=re.S | re.I)  # anchors without href
    # strip inline styles/classes/ids from the old theme
    c = re.sub(r'\s(style|class|id|width|height|srcset|sizes|data-[\w-]+)="[^"]*"', "", c)
    c = re.sub(r"<(div|span|section)\b[^>]*>", "", c, flags=re.I)
    c = re.sub(r"</(div|span|section)>", "", c, flags=re.I)
    # Theme CSS that leaked into the text, e.g. ".fusion-accordian #accordion-1 .panel-title a{...}"
    c = re.sub(r"(?:[.#@][\w.#:>()\[\]=\"\'\s,-]*\{[^{}]*\}\s*)+", "", c)
    # Designer filler ("Odd Future tote bag...", "Lorem ipsum...") left in real posts
    c = re.sub(r"<(p|li|h[1-6]|blockquote)\b[^>]*>(?:(?!</\1>).)*?(?:odd future|sugar plum|lorem ipsum|wes anderson|macaroon candy|meggings|jean shorts cred|dolor sit amet|construction of europe|realm of asia|natural beauty of asia|harmony of wild africa|human compassion binds|take an adventure|fellow travelers|biggest adventure of them all|avada|click edit button|consectetur)(?:(?!</\1>).)*</\1>", "", c, flags=re.S | re.I)
    c = re.sub(r"Explore All There Is To See|Stunning landscapes, historical cities and intriguing cultures\.?", "", c)
    c = re.sub(r"\[contact-form-7[^\]]*\]", "", c)
    c = re.sub(r"<p>\s*(&nbsp;|\s)*</p>", "", c)
    c = re.sub(r"\n{3,}", "\n\n", c)
    return c.strip()


def text_excerpt(p, n=180):
    t = re.sub(r"<[^>]+>", "", p["excerpt"]["rendered"] or p["content"]["rendered"])
    t = H.unescape(t).replace("[…]", "").replace("[...]", "").strip()
    t = re.sub(r"\s+", " ", t)
    return (t[: n - 1] + "…") if len(t) > n else t


def nice_cat(cid):
    c = cats.get(cid)
    if not c:
        return None
    name = H.unescape(c["name"])
    if name.isupper():
        name = " ".join(w[:1].upper() + w[1:].lower() for w in name.split(" "))
    name = name.replace("Spingym", "SpinGym")
    name = {"meet FORBES": "Meet Forbes", "about SpinGym": "About SpinGym", "about Events": "About Events"}.get(name, name)
    return name


def post_cats(p):
    names = [nice_cat(c) for c in p.get("categories", [])]
    return [n for n in names if n and n != "Uncategorized"]


def fmt_date(d):
    from datetime import date
    y, m, dd = int(d[:4]), int(d[5:7]), int(d[8:10])
    return date(y, m, dd).strftime("%B %-d, %Y")


def generate():
    out = {}
    sorted_posts = sorted(posts, key=lambda p: p["date"], reverse=True)
    for i, p in enumerate(sorted_posts):
        title = H.unescape(p["title"]["rendered"])
        body = sanitize(p["content"]["rendered"])
        hero = featured_img(p)
        if hero and hero == first_image(p["content"]["rendered"]):
            hero = None  # already the first picture in the body
        catlinks = " &middot; ".join(f'<a href="journal.html#cat-{slugify(c)}">{H.escape(c)}</a>' for c in post_cats(p)) or "Journal"
        newer = sorted_posts[i - 1] if i > 0 else None
        older = sorted_posts[i + 1] if i + 1 < len(sorted_posts) else None
        nav = '<nav class="post-nav" aria-label="More posts">'
        nav += f'<a href="{POST_FILE[older["slug"]]}"><small>Older</small>{H.escape(H.unescape(older["title"]["rendered"]))}</a>' if older else "<span></span>"
        nav += f'<a href="{POST_FILE[newer["slug"]]}"><small>Newer</small>{H.escape(H.unescape(newer["title"]["rendered"]))}</a>' if newer else "<span></span>"
        nav += "</nav>"
        hero_html = f'<img class="post-hero" src="{hero}" alt="" onerror="this.remove()">' if hero else ""
        html_body = f"""<!-- title: {H.escape(title)} | desc: {H.escape(text_excerpt(p, 150))} | nav: journal -->
<article class="post">
  <header class="wrap post-head">
    <p class="breadcrumb"><a href="journal.html">Journal</a> &nbsp;/&nbsp; {catlinks}</p>
    <h1>{H.escape(title)}</h1>
    <p class="post-meta">By Forbes Riley &middot; <time datetime="{p['date'][:10]}">{fmt_date(p['date'])}</time></p>
  </header>
  <div class="wrap post-body">
    {hero_html}
    <div class="prose-wide">
{body if body else '<p class="caption">This post was a photo or video gallery on the old site. The images are in the archive.</p>'}
    </div>
    {nav}
  </div>
</article>
"""
        out[POST_FILE[p["slug"]]] = html_body

    # Journal index: every post, searchable, grouped by year
    all_cats = sorted({c for p in posts for c in post_cats(p)})
    chips = "".join(f'<button type="button" data-f="{slugify(c)}" aria-pressed="false">{H.escape(c)}</button>' for c in all_cats)
    rows = []
    years = {}
    for p in sorted_posts:
        y = p["date"][:4]
        years.setdefault(y, []).append(p)
    for y, ps in years.items():
        rows.append(f'<h2 class="year" data-year="{y}">{y}</h2><div class="post-list">')
        for p in ps:
            title = H.unescape(p["title"]["rendered"])
            cs = post_cats(p)
            th = thumb(p)
            img = f'<img src="{th}" alt="" loading="lazy" onerror="this.remove()">' if th else '<span class="noimg"></span>'
            rows.append(
                f'<a class="post-row" href="{POST_FILE[p["slug"]]}" data-cats="{" ".join(slugify(c) for c in cs)}" data-text="{H.escape((title + " " + text_excerpt(p, 400)).lower(), quote=True)}">'
                f'{img}<span class="post-row-body"><span class="kicker">{H.escape(" · ".join(cs) or "Journal")} &middot; {fmt_date(p["date"])}</span>'
                f'<h3>{H.escape(title)}</h3><p>{H.escape(text_excerpt(p))}</p></span></a>'
            )
        rows.append("</div>")
    out["journal.html"] = f"""<!-- title: Forbes Riley Journal | desc: Every story from Forbes Riley's blog, 2014 to 2019: travel, friends, SpinGym, business, health, recipes and behind the scenes. | nav: journal -->
<section class="wrap page-hero">
  <p class="eyebrow">Journal</p>
  <h1>Join me. Explore and enjoy.</h1>
  <p class="lede">All {len(posts)} stories from Forbes&rsquo; blog, brought over from the old site: travel with the twins, friends and mentors, SpinGym, business, health, recipes and behind the scenes.</p>
</section>
<section class="section-tight">
  <div class="wrap">
    <div class="journal-tools">
      <label class="sr-only" for="journal-search">Search stories</label>
      <input id="journal-search" type="search" placeholder="Search {len(posts)} stories…" autocomplete="off">
      <div class="filter" role="group" aria-label="Filter by category">
        <button type="button" data-f="all" aria-pressed="true">All</button>{chips}
      </div>
      <p class="caption" id="journal-count"></p>
    </div>
    {''.join(rows)}
    <p class="caption" id="journal-empty" hidden>No stories match. Try another word or category.</p>
  </div>
</section>
<script>
(function () {{
  var q = document.getElementById('journal-search');
  var buttons = document.querySelectorAll('.filter button');
  var rows = document.querySelectorAll('.post-row');
  var years = document.querySelectorAll('.year');
  var count = document.getElementById('journal-count');
  var empty = document.getElementById('journal-empty');
  var cat = 'all';
  function apply() {{
    var t = (q.value || '').toLowerCase().trim();
    var shown = 0;
    rows.forEach(function (r) {{
      var ok = (cat === 'all' || r.getAttribute('data-cats').split(' ').indexOf(cat) !== -1) && (!t || r.getAttribute('data-text').indexOf(t) !== -1);
      r.hidden = !ok; if (ok) shown++;
    }});
    years.forEach(function (y) {{
      var list = y.nextElementSibling; var any = list.querySelector('.post-row:not([hidden])');
      y.hidden = !any; list.hidden = !any;
    }});
    count.textContent = shown + ' of ' + rows.length + ' stories';
    empty.hidden = shown > 0;
  }}
  q.addEventListener('input', apply);
  buttons.forEach(function (b) {{
    b.addEventListener('click', function () {{
      cat = b.getAttribute('data-f');
      buttons.forEach(function (x) {{ x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }});
      apply();
    }});
  }});
  var h = location.hash.replace('#cat-', '');
  if (h) {{ buttons.forEach(function (b) {{ if (b.getAttribute('data-f') === h) b.click(); }}); }}
  apply();
}})();
</script>
"""

    # Old pages
    rows = []
    for p in sorted(pages, key=lambda x: H.unescape(x["title"]["rendered"]).lower()):
        title = H.unescape(p["title"]["rendered"])
        body = sanitize(p["content"]["rendered"])
        redirect = PAGE_REDIRECT.get(p["slug"])
        note = f'<p class="caption">This page has a new home: <a href="{redirect}">{redirect.replace(".html", "").replace("-", " ")}</a>. The original is kept below for reference.</p>' if redirect else ""
        out[PAGE_FILE[p["slug"]]] = f"""<!-- title: {H.escape(title)} | desc: Page from the original forbesfactor.com, kept in the archive. | nav: archive -->
<article class="post">
  <header class="wrap post-head">
    <p class="breadcrumb"><a href="archive.html">Old site archive</a></p>
    <h1>{H.escape(title)}</h1>
    <p class="post-meta">Original page from forbesfactor.com &middot; last updated {fmt_date(p['date'])}</p>
    {note}
  </header>
  <div class="wrap post-body"><div class="prose-wide">
{body if body else '<p class="caption">This page was a slider or layout-only page on the old site, with no text of its own.</p>'}
  </div></div>
</article>
"""
        rows.append(f'<a class="post-row slim" href="{PAGE_FILE[p["slug"]]}"><span class="post-row-body"><h3>{H.escape(title)}</h3><p>{H.escape(text_excerpt(p, 140)) or "Layout-only page."}</p></span></a>')
    out["archive.html"] = f"""<!-- title: Old Site Archive | desc: Every page from the original forbesfactor.com, kept for reference. | nav: archive -->
<section class="wrap page-hero">
  <p class="eyebrow">Archive</p>
  <h1>Every page from the old site</h1>
  <p class="lede">All {len(pages)} pages from forbesfactor.com, kept here so nothing is lost. Blog posts are in the <a class="link" href="journal.html">Journal</a>. Pages that have a new home say so at the top.</p>
</section>
<section class="section-tight"><div class="wrap post-list">{''.join(rows)}</div></section>
"""
    return out


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


if __name__ == "__main__":
    g = generate()
    print(len(g), "generated pages")
