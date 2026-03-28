#!/usr/bin/env python3
"""
Recover English HTML from Italian translations using DOM-level text node replacement.
Uses BeautifulSoup for precise text handling.
"""

import json
import re
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment

ROOT = Path("/home/user/workspace/jackpoker-fan-site")
LOCALES = ROOT / "i18n" / "locales"
PAGES = ["index.html", "games.html", "tournaments.html", "bonuses.html", "promo-code.html", "news.html"]

# Use Italian as source since Italian words are most distinct from English
# (less chance of false positive replacements compared to Spanish)
SOURCE_LANG = "it"

def load(code):
    with open(LOCALES / f"{code}.json", "r", encoding="utf-8") as f:
        return json.load(f)

def flatten(d, prefix=""):
    flat = {}
    for k, v in d.items():
        if k == "_meta": continue
        if isinstance(v, dict):
            flat.update(flatten(v, f"{prefix}{k}."))
        else:
            flat[f"{prefix}{k}"] = str(v)
    return flat

en = load("en")
it = load(SOURCE_LANG)
en_flat = flatten(en)
it_flat = flatten(it)

# Build a mapping from Italian text -> English text
# Sort by length (longest first) to avoid partial matches
it_to_en = {}
for key in sorted(it_flat.keys(), key=lambda k: len(it_flat[k]), reverse=True):
    it_val = it_flat[key]
    en_val = en_flat.get(key, "")
    if it_val and en_val and it_val != en_val and len(it_val) > 3:
        it_to_en[it_val] = en_val

def reverse_translate(text):
    """Replace Italian strings with English equivalents in a text string."""
    result = text
    for it_val, en_val in it_to_en.items():
        if it_val in result:
            result = result.replace(it_val, en_val)
    return result

for page in PAGES:
    src_file = ROOT / SOURCE_LANG / page
    if not src_file.exists():
        print(f"SKIP {page}")
        continue
    
    html = src_file.read_text(encoding="utf-8")
    
    # 1. Fix lang attribute
    html = re.sub(r'<html\s+lang="it"', '<html lang="en"', html, count=1)
    
    # 2. Fix asset paths (../assets/ -> assets/)
    html = html.replace('href="../style.css"', 'href="style.css"')
    html = html.replace('src="../main.js"', 'src="main.js"')
    html = re.sub(r'(src|href)="\.\./assets/', r'\1="assets/', html)
    
    # 3. Remove hreflang tags
    html = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*" />\n?', '', html)
    
    # 4. Remove lang switcher (precise pattern)
    html = re.sub(
        r'<div class="lang-switcher">\s*<button class="lang-btn".*?</div>\s*</div>\s*',
        '',
        html,
        flags=re.DOTALL,
        count=1
    )
    
    # 5. Remove Thai font link
    html = re.sub(r'<link href="https://fonts\.googleapis\.com/css2\?family=Noto\+Sans\+Thai[^"]*" rel="stylesheet">\n?', '', html)
    
    # 6. Fix canonical URLs
    html = html.replace(f'{SOURCE_LANG}/{page}', page)
    
    # 7. Do the text replacements (Italian -> English)
    html = reverse_translate(html)
    
    out_file = ROOT / page
    out_file.write_text(html, encoding="utf-8")
    
    # Verify key strings
    checks = ["The Future of", "Online Poker", "Play Now", "Explore Games"]
    found = sum(1 for c in checks if c in html)
    print(f"  {page}: recovered ({len(html)} bytes, {found}/{len(checks)} key strings found)")

print("\nDone!")
