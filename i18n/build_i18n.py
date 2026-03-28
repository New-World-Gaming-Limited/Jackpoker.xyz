#!/usr/bin/env python3
"""
JackPoker i18n Static Site Generator v2
========================================
Generates language subdirectories from English source pages + locale JSONs.

Strategy: Use precise HTML-aware replacements. Build replacements as
(context_pattern, en_text, target_text) tuples where context_pattern helps
ensure we only replace the right instance.
"""

import json
import os
import re
import html as html_lib
from pathlib import Path
from copy import deepcopy

ROOT = Path("/home/user/workspace/jackpoker-fan-site")
I18N_DIR = ROOT / "i18n"
LOCALES_DIR = I18N_DIR / "locales"

PAGES = ["index.html", "games.html", "tournaments.html", "bonuses.html", "promo-code.html", "news.html"]

LANGUAGES = {
    "en": {"name": "English", "flag_code": "US"},
    "ru": {"name": "Русский", "flag_code": "RU"},
    "es": {"name": "Español", "flag_code": "ES"},
    "it": {"name": "Italiano", "flag_code": "IT"},
    "pt": {"name": "Português", "flag_code": "BR"},
    "vi": {"name": "Tiếng Việt", "flag_code": "VN"},
    "th": {"name": "ไทย", "flag_code": "TH"},
}

BASE_URL = "https://jackpoker.poker"

def load_locale(lang_code):
    with open(LOCALES_DIR / f"{lang_code}.json", "r", encoding="utf-8") as f:
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


def build_language_switcher_html(current_lang, current_page):
    """Build dropdown HTML for language selection."""
    info = LANGUAGES[current_lang]
    lines = [
        f'<div class="lang-switcher">',
        f'  <button class="lang-btn" aria-label="Change language" aria-expanded="false">',
        f'    <span class="lang-flag">{info["flag_code"]}</span>',
        f'    <span class="lang-label">{info["name"]}</span>',
        f'    <svg class="lang-chevron" width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
        f'  </button>',
        f'  <div class="lang-dropdown" role="menu">'
    ]
    for code, lang_info in LANGUAGES.items():
        active = ' class="active"' if code == current_lang else ''
        if code == "en":
            href = f"../{current_page}" if current_lang != "en" else current_page
        else:
            if current_lang == "en":
                href = f"{code}/{current_page}"
            elif code == current_lang:
                href = current_page
            else:
                href = f"../{code}/{current_page}"
        lines.append(f'    <a href="{href}"{active} role="menuitem" hreflang="{code}"><span class="lang-flag">{lang_info["flag_code"]}</span><span>{lang_info["name"]}</span></a>')
    lines.append('  </div>')
    lines.append('</div>')
    return '\n'.join(lines)


def build_hreflang_tags(current_page):
    """Build hreflang link tags for SEO."""
    tags = []
    for code in LANGUAGES:
        if code == "en":
            href = f"{BASE_URL}/{current_page}"
        else:
            href = f"{BASE_URL}/{code}/{current_page}"
        tags.append(f'<link rel="alternate" hreflang="{code}" href="{href}" />')
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}/{current_page}" />')
    return '\n'.join(tags)


def do_replacements(html_content, en_flat, target_flat):
    """
    Replace English text with target language text using smart matching.
    
    We sort replacements by string length (longest first) to avoid
    partial replacement issues. We skip very short strings.
    """
    result = html_content
    
    # Sort keys by the length of the English value (longest first)
    sorted_keys = sorted(en_flat.keys(), key=lambda k: len(str(en_flat[k])), reverse=True)
    
    for key in sorted_keys:
        en_val = str(en_flat[key])
        target_val = str(target_flat.get(key, en_val))
        
        if not en_val or en_val == target_val:
            continue
        
        # Skip single words that are too common and could cause false positives
        if len(en_val) <= 3:
            continue
            
        # Skip pure numbers/symbols
        if re.match(r'^[\d\$\%\+\.\,\×\s]+$', en_val):
            continue
        
        result = result.replace(en_val, target_val)
    
    return result


def fix_asset_paths(html_content, lang_code):
    """Fix relative paths for files in subdirectories."""
    # Add <base> tag so all relative links resolve correctly from the subdirectory
    # This is needed because 'serve' uses clean URLs: /ru/index.html -> /ru
    # Without trailing slash, relative links resolve from / instead of /ru/
    base_tag = f'<base href="/{lang_code}/">'
    html_content = html_content.replace('<head>', f'<head>\n  {base_tag}', 1)
    
    # CSS — needs ../ since base is /{lang}/
    html_content = html_content.replace('href="style.css"', 'href="../style.css"')
    # JS  
    html_content = html_content.replace('src="main.js"', 'src="../main.js"')
    # Images (both src and href)
    html_content = re.sub(r'(src|href)="assets/', r'\1="../assets/', html_content)
    html_content = re.sub(r"(src|href)='assets/", r"\1='../assets/", html_content)
    # Favicon link in head
    # Internal page links stay as-is (base tag handles resolution)
    return html_content


def inject_switcher(html_content, lang, page_name):
    """Inject language switcher before the theme toggle."""
    switcher = build_language_switcher_html(lang, page_name)
    # Find the theme-toggle button and insert before it
    pattern = r'(<button\s[^>]*class="theme-toggle"[^>]*>)'
    match = re.search(pattern, html_content)
    if match:
        pos = match.start()
        html_content = html_content[:pos] + switcher + '\n        ' + html_content[pos:]
    return html_content


def inject_hreflang(html_content, page_name):
    """Add hreflang tags before </head>."""
    tags = build_hreflang_tags(page_name)
    html_content = html_content.replace('</head>', f'{tags}\n</head>', 1)
    return html_content


def update_html_lang(html_content, lang_code):
    """Update the lang attribute on <html>."""
    html_content = re.sub(r'<html\s+lang="[^"]*"', f'<html lang="{lang_code}"', html_content, count=1)
    return html_content


def update_meta(html_content, page_name, en_locale, target_locale):
    """Update <title> and meta description."""
    page_key_map = {
        "index.html": "home",
        "games.html": "games",
        "tournaments.html": "tournaments",
        "bonuses.html": "bonuses",
        "promo-code.html": "promo_code",
        "news.html": "news"
    }
    section = page_key_map.get(page_name, "home")
    
    en_title = en_locale.get(section, {}).get("meta_title", "")
    target_title = target_locale.get(section, {}).get("meta_title", "")
    if en_title and target_title and en_title != target_title:
        html_content = html_content.replace(f"<title>{en_title}</title>", f"<title>{target_title}</title>", 1)
    
    en_desc = en_locale.get(section, {}).get("meta_description", "")
    target_desc = target_locale.get(section, {}).get("meta_description", "")
    if en_desc and target_desc and en_desc != target_desc:
        html_content = html_content.replace(en_desc, target_desc, 1)
    
    return html_content


def update_canonical(html_content, lang_code, page_name):
    """Update canonical URL for translated versions."""
    if lang_code != "en":
        # Update canonical
        old_canonical = f'{BASE_URL}/{page_name}'
        new_canonical = f'{BASE_URL}/{lang_code}/{page_name}'
        html_content = html_content.replace(
            f'href="{old_canonical}"', 
            f'href="{new_canonical}"',
            1
        )
    return html_content


def add_font_support(html_content, lang_code):
    """Add Google Font imports for non-Latin scripts."""
    font_links = {
        "th": '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;500;600;700&display=swap" rel="stylesheet">',
        "vi": '',  # Inter supports Vietnamese
        "ru": '',  # Inter supports Cyrillic
    }
    link = font_links.get(lang_code, "")
    if link:
        html_content = html_content.replace('</head>', f'{link}\n</head>', 1)
    return html_content


def strip_injected_elements(html_content):
    """Remove previously injected language switchers and hreflang tags."""
    # Remove language switcher blocks
    html_content = re.sub(r'<div class="lang-switcher">.*?</div>\s*</div>\s*', '', html_content, flags=re.DOTALL)
    # Remove hreflang tags
    html_content = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*" />\n?', '', html_content)
    return html_content


def process_page(page_name, lang_code, en_locale, target_locale=None):
    """Process a single page for a specific language."""
    src = ROOT / page_name
    html = src.read_text(encoding="utf-8")
    
    # Strip any previously injected elements to avoid duplicates
    html = strip_injected_elements(html)
    
    if lang_code == "en":
        # English: just add switcher and hreflang
        html = inject_hreflang(html, page_name)
        html = inject_switcher(html, "en", page_name)
        return html
    
    en_flat = flatten(en_locale)
    target_flat = flatten(target_locale)
    
    # 1. Update meta tags first (before general replacement)
    html = update_meta(html, page_name, en_locale, target_locale)
    
    # 2. Update lang attribute
    html = update_html_lang(html, lang_code)
    
    # 3. Do the text replacements
    html = do_replacements(html, en_flat, target_flat)
    
    # 4. Fix asset paths for subdirectory
    html = fix_asset_paths(html, lang_code)
    
    # 5. Update canonical
    html = update_canonical(html, lang_code, page_name)
    
    # 6. Add hreflang
    html = inject_hreflang(html, page_name)
    
    # 7. Add language switcher
    html = inject_switcher(html, lang_code, page_name)
    
    # 8. Add font support for non-Latin scripts
    html = add_font_support(html, lang_code)
    
    return html


def build():
    """Main build."""
    en_locale = load_locale("en")
    
    print("=" * 60)
    print("JackPoker i18n Build v2")
    print("=" * 60)
    
    for lang_code, lang_info in LANGUAGES.items():
        print(f"\n--- {lang_code} ({lang_info['name']}) ---")
        
        target_locale = None if lang_code == "en" else load_locale(lang_code)
        
        for page in PAGES:
            src = ROOT / page
            if not src.exists():
                print(f"  SKIP {page}")
                continue
            
            html = process_page(page, lang_code, en_locale, target_locale)
            
            if lang_code == "en":
                src.write_text(html, encoding="utf-8")
                print(f"  {page}: updated in place")
            else:
                out_dir = ROOT / lang_code
                out_dir.mkdir(exist_ok=True)
                (out_dir / page).write_text(html, encoding="utf-8")
                print(f"  {page}: written to /{lang_code}/")
    
    # Copy locale files to a public path so they can be used by JS if needed
    public_locales = ROOT / "lang"
    public_locales.mkdir(exist_ok=True)
    for f in LOCALES_DIR.glob("*.json"):
        import shutil
        shutil.copy2(f, public_locales / f.name)
    print(f"\nLocale files copied to /lang/")
    
    print(f"\n{'=' * 60}")
    print("Build complete!")
    total_pages = len(PAGES) * len(LANGUAGES)
    print(f"Generated {total_pages} pages across {len(LANGUAGES)} languages")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    build()
