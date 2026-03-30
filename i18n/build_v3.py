#!/usr/bin/env python3
"""
JackPoker i18n Build v3 — Full-Page Translation
================================================
Extracts ALL visible text from English HTML, translates via cached
translation maps, and produces fully translated pages.

Workflow for adding new content:
1. Edit the English HTML pages
2. Run: python3 i18n/build_v3.py --extract
   → Creates i18n/translations/{lang}_missing.json for each language
3. Translate the missing strings (manually or via API)
   → Put translations in i18n/translations/{lang}.json
4. Run: python3 i18n/build_v3.py
   → Builds all language versions
"""

import json
import os
import re
import sys
import hashlib
from pathlib import Path

ROOT = Path("/home/user/workspace/jackpoker-fan-site")
I18N_DIR = ROOT / "i18n"
TRANSLATIONS_DIR = I18N_DIR / "translations"
TRANSLATIONS_DIR.mkdir(exist_ok=True)

MAIN_PAGES = ["index.html", "games.html", "tournaments.html", "bonuses.html", "promo-code.html", "news.html", "terms.html"]

# Auto-discover news article pages
NEWS_DIR = ROOT / "news"
NEWS_PAGES = [f"news/{f.name}" for f in sorted(NEWS_DIR.glob("*.html"))] if NEWS_DIR.exists() else []

PAGES = MAIN_PAGES + NEWS_PAGES

LANGUAGES = {
    "en": {"name": "English", "flag_code": "GB"},
    "ru": {"name": "Русский", "flag_code": "RU"},
    "es": {"name": "Español", "flag_code": "ES"},
    "it": {"name": "Italiano", "flag_code": "IT"},
    "pt": {"name": "Português", "flag_code": "BR"},
    "vi": {"name": "Tiếng Việt", "flag_code": "VN"},
    "th": {"name": "ไทย", "flag_code": "TH"},
    "ms": {"name": "Bahasa Melayu", "flag_code": "MY"},
    "ko": {"name": "한국어", "flag_code": "KR"},
    "ar": {"name": "العربية", "flag_code": "SA"},
    "pl": {"name": "Polski", "flag_code": "PL"},
    "cs": {"name": "Čeština", "flag_code": "CZ"},
}

BASE_URL = "https://jackpoker.poker"

# Brand names that should never be translated
PROTECTED_BRAND_NAMES = [
    "JackPoker", "JACKPOKER", "jackpoker",
    "WELCOME",  # promo code
    "Cash Carnival", "Winter Games Festival",
    "Big Bang Sunday", "Bonus Bonanza",
    "Texas Hold'em", "Omaha", "PLO", "PLO6",
    "NL25+", "NLH",
]


def text_hash(text):
    return hashlib.md5(text.strip().encode('utf-8')).hexdigest()[:12]


def is_translatable(text):
    """Check if a text string should be translated."""
    s = text.strip()
    if len(s) < 3:
        return False
    # Must contain letters
    if not re.search(r'[a-zA-Z]', s):
        return False
    # Skip pure numbers/symbols
    if re.match(r'^[\d\$\%\+\.\,\×\s\-\—\–\♠\♦\♣\♥\·\|\/:;]+$', s):
        return False
    return True


def extract_text_with_positions(html):
    """Extract all visible text between HTML tags with their positions.
    Returns list of (start_in_original, end_in_original, stripped_text)."""
    
    # Remove script and style content (but keep their tags for position tracking)
    # We need positions in the ORIGINAL html, so we track differently
    
    # Find regions to skip (script/style content)
    skip_regions = []
    for pattern in [r'<script[^>]*>.*?</script>', r'<style[^>]*>.*?</style>', r'<!--.*?-->']:
        for m in re.finditer(pattern, html, re.DOTALL):
            skip_regions.append((m.start(), m.end()))
    
    def in_skip(pos):
        for s, e in skip_regions:
            if s <= pos < e:
                return True
        return False
    
    # Find all text nodes: content between > and <
    results = []
    for m in re.finditer(r'>([^<]+)<', html):
        text = m.group(1)
        # Position of the text content (after > before <)
        text_start = m.start(1)
        text_end = m.end(1)
        
        if in_skip(text_start):
            continue
        
        stripped = text.strip()
        if is_translatable(stripped):
            results.append((text_start, text_end, text, stripped))
    
    return results


def extract_meta_strings(html):
    """Extract <title> and meta description for translation."""
    results = {}
    
    title_match = re.search(r'<title>([^<]+)</title>', html)
    if title_match and is_translatable(title_match.group(1)):
        results[text_hash(title_match.group(1))] = title_match.group(1).strip()
    
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html)
    if desc_match and is_translatable(desc_match.group(1)):
        results[text_hash(desc_match.group(1))] = desc_match.group(1).strip()
    
    # Also extract og:title, og:description
    for attr in ['og:title', 'og:description']:
        og_match = re.search(rf'<meta\s+property="{attr}"\s+content="([^"]+)"', html)
        if og_match and is_translatable(og_match.group(1)):
            results[text_hash(og_match.group(1))] = og_match.group(1).strip()
    
    return results


def extract_all_strings():
    """Extract every translatable string from all English pages."""
    all_strings = {}
    
    for page in PAGES:
        src = ROOT / page
        if not src.exists():
            continue
        html = src.read_text(encoding='utf-8')
        # Strip previously injected elements
        html = strip_injected_elements(html)
        
        # Text nodes
        for start, end, full_text, stripped in extract_text_with_positions(html):
            h = text_hash(stripped)
            all_strings[h] = stripped
        
        # Meta strings
        all_strings.update(extract_meta_strings(html))
    
    return all_strings


def apply_translations(html, translations):
    """Replace all English text nodes with translations."""
    # Translate meta tags first
    title_match = re.search(r'<title>([^<]+)</title>', html)
    if title_match:
        h = text_hash(title_match.group(1))
        if h in translations and translations[h]:
            html = html[:title_match.start(1)] + translations[h] + html[title_match.end(1):]
    
    # Meta description
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html)
    if desc_match:
        h = text_hash(desc_match.group(1))
        if h in translations and translations[h]:
            html = html.replace(
                f'content="{desc_match.group(1)}"',
                f'content="{translations[h]}"',
                1
            )
    
    # OG tags
    for attr in ['og:title', 'og:description']:
        og_match = re.search(rf'<meta\s+property="{attr}"\s+content="([^"]+)"', html)
        if og_match:
            h = text_hash(og_match.group(1))
            if h in translations and translations[h]:
                html = html.replace(
                    f'property="{attr}" content="{og_match.group(1)}"',
                    f'property="{attr}" content="{translations[h]}"',
                    1
                )
    
    # Translate text nodes — process in reverse to preserve positions
    nodes = extract_text_with_positions(html)
    for start, end, full_text, stripped in reversed(nodes):
        h = text_hash(stripped)
        if h in translations and translations[h]:
            translated = translations[h]
            # Preserve leading/trailing whitespace
            leading = full_text[:len(full_text) - len(full_text.lstrip())]
            trailing = full_text[len(full_text.rstrip()):]
            html = html[:start] + leading + translated + trailing + html[end:]
    
    return html


# === HTML processing helpers ===

def build_language_switcher_html(current_lang, current_page):
    """Build language switcher HTML with correct relative paths.
    
    For main pages (e.g. news.html):
      - From /{lang}/news.html: English = ../news.html, other = ../{other}/news.html
      - From /news.html (English): other = {lang}/news.html
    
    For news articles (e.g. news/article.html):
      - From /{lang}/news/article.html: English = ../../news/article.html, other = ../../{other}/news/article.html
      - From /news/article.html (English): other = {lang}/news/article.html
    """
    info = LANGUAGES[current_lang]
    is_nested = "/" in current_page  # e.g., news/article.html
    page_filename = current_page.split("/")[-1] if is_nested else current_page
    
    lines = [
        '<div class="lang-switcher">',
        '  <button class="lang-btn" aria-label="Change language" aria-expanded="false">',
        f'    <span class="lang-flag">{info["flag_code"]}</span>',
        f'    <span class="lang-label">{info["name"]}</span>',
        '    <svg class="lang-chevron" width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
        '  </button>',
        '  <div class="lang-dropdown" role="menu">'
    ]
    for code, lang_info in LANGUAGES.items():
        active = ' class="active"' if code == current_lang else ''
        
        if current_lang == "en":
            # From English root
            if code == "en":
                href = current_page  # same page
            else:
                href = f"{code}/{current_page}"  # e.g., ru/news.html or ru/news/article.html
        else:
            # From a language subdirectory
            if is_nested:
                # From /{lang}/news/article.html
                if code == "en":
                    href = f"../../{current_page}"  # ../../news/article.html
                elif code == current_lang:
                    href = page_filename  # just article.html (same dir)
                else:
                    href = f"../../{code}/{current_page}"  # ../../{other}/news/article.html
            else:
                # From /{lang}/page.html
                if code == "en":
                    href = f"../{current_page}"  # ../page.html
                elif code == current_lang:
                    href = current_page  # same page
                else:
                    href = f"../{code}/{current_page}"  # ../{other}/page.html
        
        lines.append(f'    <a href="{href}"{active} role="menuitem" hreflang="{code}"><span class="lang-flag">{lang_info["flag_code"]}</span><span>{lang_info["name"]}</span></a>')
    lines.append('  </div>')
    lines.append('</div>')
    return '\n'.join(lines)


def build_hreflang_tags(current_page):
    tags = []
    for code in LANGUAGES:
        href = f"{BASE_URL}/{current_page}" if code == "en" else f"{BASE_URL}/{code}/{current_page}"
        tags.append(f'<link rel="alternate" hreflang="{code}" href="{href}" />')
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}/{current_page}" />')
    return '\n'.join(tags)


def strip_injected_elements(html):
    html = re.sub(r'<div class="lang-switcher">.*?</div>\s*</div>\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*" />\n?', '', html)
    return html


def inject_switcher(html, lang, page_name):
    switcher = build_language_switcher_html(lang, page_name)
    pattern = r'(<button\s[^>]*class="theme-toggle"[^>]*>)'
    match = re.search(pattern, html)
    if match:
        pos = match.start()
        html = html[:pos] + switcher + '\n        ' + html[pos:]
    return html


def fix_asset_paths(html, lang_code, page):
    """Fix asset paths for translated pages in language subdirectories.
    Main pages go to /{lang}/ so assets need ../ prefix.
    News articles go to /{lang}/news/ so assets need ../../ prefix.
    The English news articles already use ../ prefix."""
    is_news_article = page.startswith("news/")
    
    if is_news_article:
        # English news articles use ../style.css, ../assets/, etc.
        # In /{lang}/news/, we need ../../ for root assets
        html = html.replace('href="../style.css"', 'href="../../style.css"')
        html = html.replace('src="../main.js"', 'src="../../main.js"')
        html = re.sub(r'(src|href)="\.\./assets/', r'\1="../../assets/', html)
        html = re.sub(r"(src|href)='\.\./assets/", r"\1='../../assets/", html)
        # Fix nav links: ../index.html → ../../index.html for going up to site root from /{lang}/news/
        # But actually we want nav links to point to /{lang}/ versions
        # ../index.html should become ../index.html (staying in /{lang}/)
        # No change needed for nav — they're already ../page.html which resolves to /{lang}/page.html
        # Fix favicon
        html = html.replace('href="../assets/images/jackpoker-favicon.svg"', 'href="../../assets/images/jackpoker-favicon.svg"')
    else:
        # Main pages: from /{lang}/, assets are at root
        html = html.replace('href="style.css"', 'href="../style.css"')
        html = html.replace('src="main.js"', 'src="../main.js"')
        html = re.sub(r'(src|href)="assets/', r'\1="../assets/', html)
        html = re.sub(r"(src|href)='assets/", r"\1='../assets/", html)
    
    return html


def build():
    print("=" * 60)
    print("JackPoker i18n Build v3 — Full-Page Translation")
    print("=" * 60)
    
    # Extract
    print("\n1. Extracting translatable strings...")
    all_strings = extract_all_strings()
    print(f"   Found {len(all_strings)} unique translatable strings")
    
    with open(I18N_DIR / "extracted_strings.json", 'w', encoding='utf-8') as f:
        json.dump(all_strings, f, ensure_ascii=False, indent=2)
    
    # Check coverage
    for lang_code in LANGUAGES:
        if lang_code == "en":
            continue
        cache_file = TRANSLATIONS_DIR / f"{lang_code}.json"
        translations = json.load(open(cache_file)) if cache_file.exists() else {}
        missing = {h: all_strings[h] for h in all_strings if h not in translations or not translations[h]}
        
        if missing:
            print(f"   ⚠ {lang_code.upper()}: {len(missing)}/{len(all_strings)} strings need translation")
            with open(TRANSLATIONS_DIR / f"{lang_code}_missing.json", 'w', encoding='utf-8') as f:
                json.dump(missing, f, ensure_ascii=False, indent=2)
        else:
            print(f"   ✓ {lang_code.upper()}: fully translated")
    
    # Build
    for lang_code, lang_info in LANGUAGES.items():
        print(f"\n--- {lang_code} ({lang_info['name']}) ---")
        
        cache_file = TRANSLATIONS_DIR / f"{lang_code}.json"
        translations = json.load(open(cache_file)) if lang_code != "en" and cache_file.exists() else {}
        
        for page in PAGES:
            src = ROOT / page
            if not src.exists():
                continue
            
            html = src.read_text(encoding='utf-8')
            html = strip_injected_elements(html)
            
            if lang_code == "en":
                html = html.replace('</head>', build_hreflang_tags(page) + '\n</head>', 1)
                html = inject_switcher(html, "en", page)
                src.write_text(html, encoding='utf-8')
                print(f"  {page}: updated")
            else:
                html = apply_translations(html, translations)
                html = re.sub(r'<html\s+lang="[^"]*"', f'<html lang="{lang_code}"', html, count=1)
                html = fix_asset_paths(html, lang_code, page)
                
                # Canonical — regex replacement to handle all URL formats
                new_canonical = f'{BASE_URL}/{lang_code}/{page}'
                html = re.sub(
                    r'<link\s+rel="canonical"\s+href="[^"]*"\s*/?>',
                    f'<link rel="canonical" href="{new_canonical}" />',
                    html, count=1
                )
                
                # Hreflang + switcher
                html = html.replace('</head>', build_hreflang_tags(page) + '\n</head>', 1)
                html = inject_switcher(html, lang_code, page)
                
                # Font support + RTL
                if lang_code == "th":
                    html = html.replace('</head>', '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;500;600;700&display=swap" rel="stylesheet">\n</head>', 1)
                elif lang_code == "ko":
                    html = html.replace('</head>', '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700&display=swap" rel="stylesheet">\n</head>', 1)
                elif lang_code == "pl" or lang_code == "cs":
                    # Polish and Czech use Latin Extended characters — Inter covers them, no extra font needed
                    pass
                elif lang_code == "ar":
                    # Arabic: RTL direction + Arabic font
                    html = re.sub(r'<html\s+lang="ar"', '<html lang="ar" dir="rtl"', html, count=1)
                    html = html.replace('</head>', '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@400;500;600;700&display=swap" rel="stylesheet">\n<style>\n/* Arabic RTL overrides */\n[dir="rtl"] { font-family: "Noto Sans Arabic", var(--font-body); }\n[dir="rtl"] .nav-links { flex-direction: row-reverse; }\n[dir="rtl"] .nav-cta { margin-left: 0; margin-right: auto; }\n[dir="rtl"] .hero-content { text-align: right; }\n[dir="rtl"] .feature-card, [dir="rtl"] .game-card { text-align: right; }\n[dir="rtl"] .lang-switcher { left: auto; }\n[dir="rtl"] .footer-grid { direction: rtl; }\n[dir="rtl"] .breadcrumb { direction: rtl; }\n[dir="rtl"] .news-card-content { text-align: right; }\n[dir="rtl"] .promo-steps { direction: rtl; }\n[dir="rtl"] .step-number { margin-right: 0; margin-left: 1rem; }\n</style>\n</head>', 1)
                
                out_path = ROOT / lang_code / page
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(html, encoding='utf-8')
                print(f"  {page}: written to /{lang_code}/{page}")
    
    import shutil
    public_locales = ROOT / "lang"
    public_locales.mkdir(exist_ok=True)
    locales_dir = I18N_DIR / "locales"
    for f in locales_dir.glob("*.json"):
        shutil.copy2(f, public_locales / f.name)
    
    print(f"\n{'=' * 60}")
    print(f"Generated {len(PAGES) * len(LANGUAGES)} pages across {len(LANGUAGES)} languages")
    print("=" * 60)


if __name__ == "__main__":
    if "--extract" in sys.argv:
        print("Extracting translatable strings...")
        strings = extract_all_strings()
        print(f"Found {len(strings)} strings")
        with open(I18N_DIR / "extracted_strings.json", 'w', encoding='utf-8') as f:
            json.dump(strings, f, ensure_ascii=False, indent=2)
        
        for lang_code in LANGUAGES:
            if lang_code == "en":
                continue
            cache_file = TRANSLATIONS_DIR / f"{lang_code}.json"
            translations = json.load(open(cache_file)) if cache_file.exists() else {}
            missing = {h: strings[h] for h in strings if h not in translations or not translations[h]}
            missing_file = TRANSLATIONS_DIR / f"{lang_code}_missing.json"
            with open(missing_file, 'w', encoding='utf-8') as f:
                json.dump(missing, f, ensure_ascii=False, indent=2)
            print(f"  {lang_code.upper()}: {len(missing)} missing → {missing_file}")
    else:
        build()
