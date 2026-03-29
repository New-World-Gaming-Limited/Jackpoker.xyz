#!/usr/bin/env python3
"""Fix all SEO issues across the JackPoker site."""
import re
import json
import os
from pathlib import Path
from datetime import date

ROOT = Path("/home/user/workspace/jackpoker-fan-site")
BASE_URL = "https://jackpoker.poker"
TODAY = date.today().isoformat()

LANGUAGES = ["en", "ru", "es", "it", "pt", "vi", "th", "ms"]
LANG_NAMES = {
    "en": "English", "ru": "Русский", "es": "Español", "it": "Italiano",
    "pt": "Português", "vi": "Tiếng Việt", "th": "ไทย", "ms": "Bahasa Melayu"
}

# ============================================================
# 1. Fix news article OG tags + JSON-LD + shorter titles
# ============================================================
def fix_news_articles():
    print("\n=== Fixing News Articles ===")
    articles_dir = ROOT / "news"
    
    article_metadata = {
        "winter-games-festival-wraps-with-record-breaking-21m-in-payo.html": {
            "short_title": "Winter Games Festival: $2.1M Record Payouts",
            "category": "Tournament",
            "date": "2026-03-25",
            "image": "news-winter-games.jpg"
        },
        "jackpoker-mobile-app-30-launches-with-multi-table-support.html": {
            "short_title": "Mobile App 3.0: Multi-Table Support",
            "category": "Platform",
            "date": "2026-03-20",
            "image": "news-mobile-app.jpg"
        },
        "crypto-deposits-now-available-in-sol-matic-and-ton.html": {
            "short_title": "Crypto Deposits: SOL, MATIC & TON Live",
            "category": "Payments",
            "date": "2026-03-15",
            "image": "news-crypto-deposits.jpg"
        },
        "bonus-bonanza-march-schedule-620-events-125m-in-guarantees.html": {
            "short_title": "Bonus Bonanza March: 620 Events, $1.25M GTD",
            "category": "Tournament",
            "date": "2026-03-10",
            "image": "news-bonus-bonanza.jpg"
        },
        "jackpoker-passes-500000-registered-players-milestone.html": {
            "short_title": "JackPoker Hits 500K Players Milestone",
            "category": "Community",
            "date": "2026-03-05",
            "image": "news-500k-milestone.jpg"
        },
        "new-hand-replayer-and-advanced-statistics-dashboard-released.html": {
            "short_title": "New Hand Replayer & Stats Dashboard",
            "category": "Platform",
            "date": "2026-02-28",
            "image": "news-statistics-dashboard.jpg"
        },
        "big-bang-sunday-guarantee-increased-to-45k-largest-in-jackpo.html": {
            "short_title": "Big Bang Sunday: $45K GTD — Record High",
            "category": "Tournament",
            "date": "2026-02-20",
            "image": "news-big-bang-sunday.jpg"
        },
        "instant-withdrawal-processing-now-available-for-vip-players.html": {
            "short_title": "Instant Withdrawals for VIP Players",
            "category": "Payments",
            "date": "2026-02-15",
            "image": "news-instant-withdrawal.jpg"
        },
    }
    
    for filename, meta in article_metadata.items():
        filepath = articles_dir / filename
        if not filepath.exists():
            continue
        
        html = filepath.read_text(encoding='utf-8')
        
        # Shorten title
        new_title = f"{meta['short_title']} | JackPoker News"
        html = re.sub(r'<title>[^<]+</title>', f'<title>{new_title}</title>', html)
        
        # Get meta description
        desc_match = re.search(r'name="description"\s+content="([^"]+)"', html)
        desc = desc_match.group(1) if desc_match else meta['short_title']
        
        # Add OG tags if missing
        if 'og:title' not in html:
            og_tags = f'''  <meta property="og:title" content="{new_title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="article">
  <meta property="og:image" content="{BASE_URL}/assets/images/news/{meta['image']}">
  <meta property="og:url" content="{BASE_URL}/news/{filename}">
  <meta property="article:published_time" content="{meta['date']}">
  <meta property="article:section" content="{meta['category']}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{new_title}">
  <meta name="twitter:description" content="{desc[:200]}">
  <meta name="twitter:image" content="{BASE_URL}/assets/images/news/{meta['image']}">'''
            html = html.replace('</head>', og_tags + '\n</head>')
        
        # Add Article JSON-LD if missing
        if 'application/ld+json' not in html:
            h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
            headline = h1_match.group(1).strip() if h1_match else meta['short_title']
            
            jsonld = {
                "@context": "https://schema.org",
                "@type": "NewsArticle",
                "headline": headline,
                "description": desc[:200],
                "image": f"{BASE_URL}/assets/images/news/{meta['image']}",
                "datePublished": meta['date'],
                "dateModified": TODAY,
                "author": {
                    "@type": "Organization",
                    "name": "JackPoker",
                    "url": BASE_URL
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "JackPoker",
                    "url": BASE_URL,
                    "logo": {
                        "@type": "ImageObject",
                        "url": f"{BASE_URL}/assets/images/jackpoker-favicon.svg"
                    }
                },
                "mainEntityOfPage": {
                    "@type": "WebPage",
                    "@id": f"{BASE_URL}/news/{filename}"
                }
            }
            jsonld_tag = f'<script type="application/ld+json">\n{json.dumps(jsonld, indent=2)}\n</script>'
            html = html.replace('</head>', jsonld_tag + '\n</head>')
        
        # Add internal contextual link to promo page within article body if only 2 links exist
        # Add a contextual "Related: Get your welcome bonus" link before the CTA section
        if html.count('promo-code.html') <= 2:
            # Add a contextual promo link in the article body
            promo_link = '''
    <div style="background: linear-gradient(135deg, rgba(137,59,247,0.08), rgba(255,61,0,0.05)); border: 1px solid rgba(137,59,247,0.2); border-radius: 12px; padding: 20px; margin: 24px 0; text-align: center;">
      <p style="margin: 0; color: var(--text-secondary); font-size: 0.9rem;">New to JackPoker? Use promo code <strong style="color: var(--gold-primary);">WELCOME</strong> for a <a href="../promo-code.html" style="color: var(--purple-primary); font-weight: 600; text-decoration: none;">300% deposit match up to $2,000</a>.</p>
    </div>'''
            # Insert before the promo CTA at the bottom
            html = html.replace('<!-- PROMO CTA -->', promo_link + '\n    <!-- PROMO CTA -->')
            # If no marker, insert before the "Back to All News" link
            if '<!-- PROMO CTA -->' not in html:
                html = html.replace('← Back to All News', promo_link + '\n    ← Back to All News')
        
        filepath.write_text(html, encoding='utf-8')
        print(f"  Fixed: {filename} (title: {len(new_title)} chars)")

# ============================================================
# 2. Fix index.html title (1 char over)
# ============================================================
def fix_index_title():
    print("\n=== Fixing Index Title ===")
    idx = ROOT / "index.html"
    html = idx.read_text(encoding='utf-8')
    # Shorten by removing the dash: "JackPoker – The Future..." → "JackPoker: Future of Online Poker | 300% Bonus"
    html = re.sub(
        r'<title>[^<]+</title>',
        '<title>JackPoker: Online Poker | 300% Welcome Bonus</title>',
        html
    )
    idx.write_text(html, encoding='utf-8')
    print("  index.html title shortened to 47 chars")

# ============================================================
# 3. Add "Latest News" section to main pages linking to articles
# ============================================================
def add_news_links_to_main_pages():
    print("\n=== Adding News Article Links to Main Pages ===")
    
    news_links_html = '''
    <!-- Latest News Links -->
    <section style="padding: 24px 0 0;">
      <div class="container">
        <h3 style="font-family: var(--font-display); font-size: 1.1rem; font-weight: 700; margin-bottom: 16px; color: var(--text-primary);">Latest from JackPoker</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
          <a href="news/winter-games-festival-wraps-with-record-breaking-21m-in-payo.html" style="color: var(--purple-primary); font-size: 0.82rem; text-decoration: none; padding: 6px 14px; border: 1px solid var(--border-subtle); border-radius: 20px; transition: all 0.2s;">Winter Games Festival: $2.1M Payouts →</a>
          <a href="news/bonus-bonanza-march-schedule-620-events-125m-in-guarantees.html" style="color: var(--purple-primary); font-size: 0.82rem; text-decoration: none; padding: 6px 14px; border: 1px solid var(--border-subtle); border-radius: 20px; transition: all 0.2s;">Bonus Bonanza March: $1.25M GTD →</a>
          <a href="news/jackpoker-mobile-app-30-launches-with-multi-table-support.html" style="color: var(--purple-primary); font-size: 0.82rem; text-decoration: none; padding: 6px 14px; border: 1px solid var(--border-subtle); border-radius: 20px; transition: all 0.2s;">Mobile App 3.0 Launched →</a>
          <a href="news/crypto-deposits-now-available-in-sol-matic-and-ton.html" style="color: var(--purple-primary); font-size: 0.82rem; text-decoration: none; padding: 6px 14px; border: 1px solid var(--border-subtle); border-radius: 20px; transition: all 0.2s;">Crypto Deposits: SOL, MATIC, TON →</a>
        </div>
      </div>
    </section>'''
    
    # Add to pages that don't have news article links: games, tournaments, bonuses, promo-code
    for page_name in ["games.html", "tournaments.html", "bonuses.html", "promo-code.html"]:
        page_path = ROOT / page_name
        if not page_path.exists():
            continue
        html = page_path.read_text(encoding='utf-8')
        
        if 'Latest from JackPoker' in html:
            continue
        
        # Insert before footer
        footer_match = re.search(r'<footer', html)
        if footer_match:
            html = html[:footer_match.start()] + news_links_html + '\n\n  ' + html[footer_match.start():]
            page_path.write_text(html, encoding='utf-8')
            print(f"  Added news links to {page_name}")

# ============================================================
# 4. Add preconnect hints to all pages
# ============================================================
def add_preconnect():
    print("\n=== Adding Preconnect Hints ===")
    preconnect = '''  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'''
    
    for page in ROOT.glob("*.html"):
        html = page.read_text(encoding='utf-8')
        if 'preconnect' not in html and 'fonts.googleapis' in html:
            html = html.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n' + preconnect)
            page.write_text(html, encoding='utf-8')
    print("  Added preconnect to all pages with Google Fonts")

# ============================================================
# 5. Create 404.html
# ============================================================
def create_404():
    print("\n=== Creating 404 Page ===")
    html_404 = '''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Not Found — JackPoker</title>
  <meta name="robots" content="noindex">
  <link rel="stylesheet" href="style.css">
  <link rel="icon" type="image/svg+xml" href="assets/images/jackpoker-favicon.svg">
  <style>
    .error-page { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 80vh; text-align: center; padding: 2rem; }
    .error-code { font-family: var(--font-display); font-size: 8rem; font-weight: 900; background: linear-gradient(90deg, #8032FF, #FF3D00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1; }
    .error-message { font-size: 1.5rem; font-weight: 600; margin: 1rem 0; }
    .error-links { display: flex; gap: 1rem; margin-top: 2rem; flex-wrap: wrap; justify-content: center; }
    .error-links a { padding: 12px 28px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 0.9rem; transition: all 0.2s; }
    .error-links .primary { background: linear-gradient(90deg, #6A2DC0, #FF3D00); color: white; }
    .error-links .secondary { border: 1px solid var(--border-subtle); color: var(--text-secondary); }
  </style>
</head>
<body>
  <div class="error-page">
    <div class="error-code">404</div>
    <p class="error-message">This page doesn't exist</p>
    <p style="color: var(--text-muted); max-width: 400px;">The page you're looking for may have been moved or no longer exists. Try one of these instead:</p>
    <div class="error-links">
      <a href="index.html" class="primary">Back to Home</a>
      <a href="promo-code.html" class="secondary">Get Promo Code</a>
      <a href="games.html" class="secondary">Explore Games</a>
      <a href="news.html" class="secondary">Latest News</a>
    </div>
  </div>
</body>
</html>'''
    (ROOT / "404.html").write_text(html_404, encoding='utf-8')
    print("  Created 404.html")

# ============================================================
# 6. Create manifest.json
# ============================================================
def create_manifest():
    print("\n=== Creating manifest.json ===")
    manifest = {
        "name": "JackPoker — Online Poker",
        "short_name": "JackPoker",
        "description": "Premier online poker platform with Texas Hold'em, PLO, Spin & Win and massive tournaments.",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#000000",
        "theme_color": "#893BF7",
        "icons": [
            {"src": "assets/images/jackpoker-favicon.svg", "sizes": "any", "type": "image/svg+xml"}
        ]
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    
    # Add manifest link to index.html
    idx = ROOT / "index.html"
    html = idx.read_text(encoding='utf-8')
    if 'manifest.json' not in html:
        html = html.replace('</head>', '  <link rel="manifest" href="manifest.json">\n</head>')
        idx.write_text(html, encoding='utf-8')
    print("  Created manifest.json and linked in index.html")

# ============================================================
# 7. Regenerate sitemaps with news articles + Malaysian
# ============================================================
def generate_sitemaps():
    print("\n=== Generating Updated Sitemaps ===")
    
    main_pages = [
        ("index.html", "weekly", "0.9"),
        ("games.html", "monthly", "0.8"),
        ("tournaments.html", "weekly", "0.8"),
        ("bonuses.html", "weekly", "0.8"),
        ("promo-code.html", "weekly", "1.0"),
        ("news.html", "daily", "0.7"),
    ]
    
    news_pages = []
    news_dir = ROOT / "news"
    if news_dir.exists():
        for f in sorted(news_dir.glob("*.html")):
            news_pages.append((f"news/{f.name}", "monthly", "0.6"))
    
    all_pages = main_pages + news_pages
    
    def make_sitemap(lang_code, pages):
        urls = []
        for page, freq, priority in pages:
            if lang_code == "en":
                loc = f"{BASE_URL}/{page}"
            else:
                loc = f"{BASE_URL}/{lang_code}/{page}"
            
            alternates = []
            for lc in LANGUAGES:
                if lc == "en":
                    alt_href = f"{BASE_URL}/{page}"
                else:
                    alt_href = f"{BASE_URL}/{lc}/{page}"
                alternates.append(f'    <xhtml:link rel="alternate" hreflang="{lc}" href="{alt_href}" />')
            alternates.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE_URL}/{page}" />')
            
            urls.append(f'''  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
{chr(10).join(alternates)}
  </url>''')
        
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
{chr(10).join(urls)}
</urlset>'''
    
    # EN sitemap
    (ROOT / "sitemap-en.xml").write_text(make_sitemap("en", all_pages), encoding='utf-8')
    
    # Language sitemaps
    for lang in LANGUAGES:
        if lang == "en":
            continue
        lang_dir = ROOT / lang
        lang_dir.mkdir(exist_ok=True)
        (lang_dir / "sitemap.xml").write_text(make_sitemap(lang, all_pages), encoding='utf-8')
    
    # Sitemap index
    sitemaps = [f'''  <sitemap>
    <loc>{BASE_URL}/sitemap-en.xml</loc>
    <lastmod>{TODAY}</lastmod>
  </sitemap>''']
    for lang in LANGUAGES:
        if lang == "en":
            continue
        sitemaps.append(f'''  <sitemap>
    <loc>{BASE_URL}/{lang}/sitemap.xml</loc>
    <lastmod>{TODAY}</lastmod>
  </sitemap>''')
    
    sitemap_index = f'''<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(sitemaps)}
</sitemapindex>'''
    (ROOT / "sitemap.xml").write_text(sitemap_index, encoding='utf-8')
    
    # Robots.txt
    robots = f'''User-agent: *
Allow: /
Disallow: /i18n/
Disallow: /lang/
Disallow: /skills/

Sitemap: {BASE_URL}/sitemap.xml
'''
    for lang in LANGUAGES:
        if lang == "en":
            robots += f"Sitemap: {BASE_URL}/sitemap-en.xml\n"
        else:
            robots += f"Sitemap: {BASE_URL}/{lang}/sitemap.xml\n"
    
    (ROOT / "robots.txt").write_text(robots, encoding='utf-8')
    
    total_urls = len(all_pages) * len(LANGUAGES)
    print(f"  Generated {len(LANGUAGES)} sitemaps with {total_urls} total URLs")
    print(f"  Updated robots.txt with all sitemap references")

# ============================================================
# Run all fixes
# ============================================================
if __name__ == "__main__":
    fix_news_articles()
    fix_index_title()
    add_news_links_to_main_pages()
    add_preconnect()
    create_404()
    create_manifest()
    generate_sitemaps()
    print("\n✅ All SEO fixes applied!")
