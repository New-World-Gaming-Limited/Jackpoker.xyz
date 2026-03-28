#!/usr/bin/env python3
"""
Add data-i18n attributes to all translatable text elements in HTML pages.
This marks each element for JS-based runtime translation.

Approach: Parse HTML, find text nodes that match en.json values,
and add data-i18n="section.key" to their parent elements.
"""

import json
import re
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment

ROOT = Path("/home/user/workspace/jackpoker-fan-site")
LOCALES_DIR = ROOT / "i18n" / "locales"
PAGES = ["index.html", "games.html", "tournaments.html", "bonuses.html", "promo-code.html", "news.html"]

def load_en():
    with open(LOCALES_DIR / "en.json", "r", encoding="utf-8") as f:
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

# This approach is too complex and fragile with BeautifulSoup on complex HTML.
# Instead, we'll take a simpler approach using the JS i18n runtime.
print("Skipping DOM-level approach. Using JS runtime i18n instead.")
