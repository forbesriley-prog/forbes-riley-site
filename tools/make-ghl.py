"""Build the GoHighLevel paste kit for the Inner Circle page from dist/inner-circle.html.
Writes dist/ghl/inner-circle.css, inner-circle.js, inner-circle-paste.html (markup only, loads the css/js
from site.forbesrileyhq.com) and inner-circle-full.html (everything in one paste)."""
import re, os, pathlib
BASE='https://site.forbesrileyhq.com/'
src=pathlib.Path('dist/inner-circle.html').read_text()
def absolutize(t):
    t=re.sub(r'(src|href|data-src)="(img/[^"]+)"',lambda m:f'{m.group(1)}="{BASE}{m.group(2)}"',t)
    t=re.sub(r'url\((img/[^)]+)\)',lambda m:f'url({BASE}{m.group(1)})',t)
    return t
style=re.search(r'<style[^>]*>(.*?)</style>',src,re.S).group(1)
script=re.search(r'<body.*?(<script[^>]*>)(.*?)</script>',src,re.S)
body=src[src.find('<body'):]
body=body[body.find('>')+1:]
body=re.sub(r'<script[^>]*>.*?</script>','',body,flags=re.S)
body=body[:body.rfind('</body>')]
fonts=re.search(r'<link[^>]+fonts\.googleapis\.com/css2[^>]*>',src).group(0)
css=absolutize(style).strip(); js=re.sub(r"(['\"])(img/[^'\"]+)\1",lambda m:f'{m.group(1)}{BASE}{m.group(2)}{m.group(1)}',script.group(2)).strip(); html=absolutize(body).strip()
out=pathlib.Path('dist/ghl'); out.mkdir(exist_ok=True)
(out/'inner-circle.css').write_text(css)
(out/'inner-circle.js').write_text(js)
head=f'<!-- Inner Circle Black Friday page for GoHighLevel. Paste this whole file into ONE Custom JS/HTML element on a blank funnel step. Images, styles and script load from site.forbesrileyhq.com. -->\n<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n{fonts}\n'
(out/'inner-circle-paste.html').write_text(head+f'<link rel="stylesheet" href="{BASE}ghl/inner-circle.css">\n'+html+f'\n<script src="{BASE}ghl/inner-circle.js"></script>\n')
(out/'inner-circle-full.html').write_text(head+'<style>\n'+css+'\n</style>\n'+html+'\n<script>\n'+js+'\n</script>\n')
for f in out.iterdir(): print(f.name, f.stat().st_size)
