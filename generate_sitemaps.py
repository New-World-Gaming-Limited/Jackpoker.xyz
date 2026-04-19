#!/usr/bin/env python3
"""Generate sitemaps for all 17 languages with proper hreflang tags."""

import os
from datetime import date

DOMAIN = "https://www.jackpoker.xyz"
TODAY = date.today().isoformat()

LANGUAGES = ["en", "ru", "es", "it", "pt", "vi", "th", "ms", "ko", "ar", "ja", "pl", "cs", "hi", "tr", "tl", "fr", "zh", "id", "uk"]

# All pages (matching build_v3.py PAGES list)
MAIN_PAGES = ["index.html", "games.html", "tournaments.html", "bonuses.html", "promo-code.html", "news.html", "terms.html", "faq.html"]

# Auto-discover compare and news pages
compare_dir = os.path.join(os.path.dirname(__file__), "compare")
news_dir = os.path.join(os.path.dirname(__file__), "news")

COMPARE_PAGES = sorted([f"compare/{f}" for f in os.listdir(compare_dir) if f.endswith(".html")]) if os.path.exists(compare_dir) else []
NEWS_PAGES = sorted([f"news/{f}" for f in os.listdir(news_dir) if f.endswith(".html")]) if os.path.exists(news_dir) else []

ALL_PAGES = MAIN_PAGES + COMPARE_PAGES + NEWS_PAGES

# Priority mapping
def get_priority(page):
    if page == "index.html":
        return "1.0"
    elif page == "promo-code.html":
        return "0.9"
    elif page in ["bonuses.html", "games.html", "tournaments.html", "faq.html"]:
        return "0.8"
    elif page.startswith("compare/"):
        return "0.7"
    elif page == "news.html":
        return "0.7"
    elif page.startswith("news/"):
        return "0.6"
    elif page == "terms.html":
        return "0.4"
    return "0.5"

def get_url(lang, page):
    """Get the URL for a page in a given language. No .html in canonical for index."""
    if page == "index.html":
        if lang == "en":
            return f"{DOMAIN}/"
        else:
            return f"{DOMAIN}/{lang}/"
    else:
        if lang == "en":
            return f"{DOMAIN}/{page}"
        else:
            return f"{DOMAIN}/{lang}/{page}"

def generate_hreflang_links(page):
    """Generate hreflang links for all languages + x-default."""
    links = []
    for lang in LANGUAGES:
        url = get_url(lang, page)
        links.append(f'      <xhtml:link rel="alternate" hreflang="{lang}" href="{url}"/>')
    # x-default points to English
    en_url = get_url("en", page)
    links.append(f'      <xhtml:link rel="alternate" hreflang="x-default" href="{en_url}"/>')
    return "\n".join(links)

def generate_language_sitemap(lang):
    """Generate a sitemap for a specific language."""
    urls = []
    for page in ALL_PAGES:
        loc = get_url(lang, page)
        priority = get_priority(page)
        hreflang_links = generate_hreflang_links(page)
        urls.append(f"""    <url>
      <loc>{loc}</loc>
      <lastmod>{TODAY}</lastmod>
      <changefreq>weekly</changefreq>
      <priority>{priority}</priority>
{hreflang_links}
    </url>""")

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
{chr(10).join(urls)}
</urlset>"""
    return sitemap

def generate_sitemap_index():
    """Generate the sitemap index file."""
    sitemaps = []
    # English sitemap is at root
    sitemaps.append(f"""    <sitemap>
      <loc>{DOMAIN}/sitemap.xml</loc>
      <lastmod>{TODAY}</lastmod>
    </sitemap>""")
    # Other languages
    for lang in LANGUAGES[1:]:  # Skip 'en'
        sitemaps.append(f"""    <sitemap>
      <loc>{DOMAIN}/{lang}/sitemap.xml</loc>
      <lastmod>{TODAY}</lastmod>
    </sitemap>""")

    index = f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(sitemaps)}
</sitemapindex>"""
    return index

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Generate English sitemap at root
    en_sitemap = generate_language_sitemap("en")
    with open(os.path.join(base_dir, "sitemap.xml"), "w") as f:
        f.write(en_sitemap)
    print(f"Generated sitemap.xml (English, {len(ALL_PAGES)} URLs)")

    # Generate language sitemaps
    for lang in LANGUAGES[1:]:  # Skip 'en'
        lang_dir = os.path.join(base_dir, lang)
        os.makedirs(lang_dir, exist_ok=True)
        lang_sitemap = generate_language_sitemap(lang)
        with open(os.path.join(lang_dir, "sitemap.xml"), "w") as f:
            f.write(lang_sitemap)
        print(f"Generated {lang}/sitemap.xml ({len(ALL_PAGES)} URLs)")

    # Generate sitemap index
    sitemap_index = generate_sitemap_index()
    with open(os.path.join(base_dir, "sitemap-index.xml"), "w") as f:
        f.write(sitemap_index)
    print(f"Generated sitemap-index.xml ({len(LANGUAGES)} language sitemaps)")

    # Remove old sitemap-{lang}.xml files at root (legacy format)
    for lang in LANGUAGES:
        old_file = os.path.join(base_dir, f"sitemap-{lang}.xml")
        if os.path.exists(old_file):
            os.remove(old_file)
            print(f"Removed legacy {os.path.basename(old_file)}")

    total_urls = len(ALL_PAGES) * len(LANGUAGES)
    print(f"\nTotal: {total_urls} URLs across {len(LANGUAGES)} languages, {len(ALL_PAGES)} pages each")

if __name__ == "__main__":
    main()
