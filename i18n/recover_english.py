#!/usr/bin/env python3
"""
Recover English HTML files from Spanish translated versions.
Reverses the translation by swapping es.json values back to en.json values.
Also fixes asset paths (../ back to ./) and lang attribute.
"""

import json
import re
from pathlib import Path

ROOT = Path("/home/user/workspace/jackpoker-fan-site")
LOCALES_DIR = ROOT / "i18n" / "locales"
PAGES = ["index.html", "games.html", "tournaments.html", "bonuses.html", "promo-code.html"]

def load_locale(code):
    with open(LOCALES_DIR / f"{code}.json", "r", encoding="utf-8") as f:
        return json.load(f)

def flatten(d, prefix=""):
    flat = {}
    for k, v in d.items():
        if k == "_meta":
            continue
        if isinstance(v, dict):
            flat.update(flatten(v, f"{prefix}{k}."))
        else:
            flat[f"{prefix}{k}"] = v
    return flat

en = load_locale("en")
es = load_locale("es")
en_flat = flatten(en)
es_flat = flatten(es)

# Sort by length of Spanish value (longest first) for safe replacement
sorted_keys = sorted(es_flat.keys(), key=lambda k: len(str(es_flat[k])), reverse=True)

for page in PAGES:
    src = ROOT / "es" / page
    if not src.exists():
        print(f"SKIP {page} (not in es/)")
        continue
    
    html = src.read_text(encoding="utf-8")
    
    # Reverse translate: replace Spanish -> English
    for key in sorted_keys:
        es_val = str(es_flat[key])
        en_val = str(en_flat.get(key, ""))
        
        if not es_val or not en_val or es_val == en_val:
            continue
        if len(es_val) <= 3:
            continue
        if re.match(r'^[\d\$\%\+\.\,\×\s]+$', es_val):
            continue
        
        html = html.replace(es_val, en_val)
    
    # Fix asset paths back to root-relative
    html = html.replace('href="../style.css"', 'href="style.css"')
    html = html.replace('src="../main.js"', 'src="main.js"')
    html = re.sub(r'(src|href)="\.\./assets/', r'\1="assets/', html)
    html = re.sub(r"(src|href)='\.\./assets/", r"\1='assets/", html)
    
    # Fix lang attribute
    html = re.sub(r'<html\s+lang="es"', '<html lang="en"', html, count=1)
    
    # Remove hreflang tags (will be re-added by build)
    html = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*" />\s*', '', html)
    
    # Remove language switcher (will be re-added by build)
    html = re.sub(r'<div class="lang-switcher">.*?</div>\s*</div>\s*</div>\s*', '', html, flags=re.DOTALL, count=1)
    
    # Remove Thai font link if present
    html = re.sub(r'<link href="https://fonts\.googleapis\.com/css2\?family=Noto\+Sans\+Thai[^"]*" rel="stylesheet">\s*', '', html)
    
    # Fix canonical URL
    html = html.replace(f'href="https://jackpoker.xyz/es/', 'href="https://jackpoker.xyz/')
    
    out = ROOT / page
    out.write_text(html, encoding="utf-8")
    print(f"Recovered {page} ({len(html)} bytes)")

print("\nDone! English files recovered from Spanish versions.")
