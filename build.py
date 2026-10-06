#!/usr/bin/env python3
"""Build the Forbes Riley static site.

    python3 build.py            -> dist/            (full pages, deploy anywhere)
    python3 build.py --artifact -> dist-artifact/   (index.html without the html skeleton,
                                                     for publishing as a claude.ai artifact)

Each file in src/pages/*.html starts with one comment line:
    <!-- title: Page Title | desc: one sentence | nav: key -->
followed by the page body. Header and footer come from src/partials/.
"""
import re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
artifact = "--artifact" in sys.argv
OUT = ROOT / ("dist-artifact" if artifact else "dist")

header = (SRC / "partials" / "header.html").read_text()
footer = (SRC / "partials" / "footer.html").read_text()
css = (SRC / "style.css").read_text()

HEAD = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;0,6..96,600;1,6..96,400;1,6..96,500&family=Nunito+Sans:ital,opsz,wght@0,6..12,300;0,6..12,400;0,6..12,600;0,6..12,700;1,6..12,400&family=Pinyon+Script&display=swap">
<link rel="stylesheet" href="style.css">
"""

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
shutil.copytree(SRC / "img", OUT / "img")
(OUT / "style.css").write_text(css)

for page in sorted((SRC / "pages").glob("*.html")):
    text = page.read_text()
    m = re.match(r"\s*<!--\s*title:\s*(.*?)\s*\|\s*desc:\s*(.*?)\s*\|\s*nav:\s*(\S*)\s*-->\s*", text, re.S)
    if not m:
        sys.exit(f"{page.name}: missing front-matter comment")
    title, desc, nav = m.groups()
    body = text[m.end():]
    hdr = header.replace(f'data-nav="{nav}"', f'data-nav="{nav}" aria-current="page"')
    inner = f"{hdr}\n<main id=\"main\">\n{body}\n</main>\n{footer}"
    head = HEAD.format(title=title, desc=desc)
    if artifact and page.name == "index.html":
        # The artifact host wraps the page in its own skeleton; keep head bits inline.
        inline_css = f"<style>\n{css}\n</style>"
        html = head.replace('<link rel="stylesheet" href="style.css">', inline_css) + inner
    else:
        html = f"<!doctype html>\n<html lang=\"en\">\n<head>\n{head}</head>\n<body class=\"page-{page.stem}\">\n{inner}\n</body>\n</html>\n"
    (OUT / page.name).write_text(html)
    print("built", page.name)

print("->", OUT)
