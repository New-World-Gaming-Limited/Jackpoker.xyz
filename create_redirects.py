#!/usr/bin/env python3
"""Create physical redirect HTML pages for old /en/* ghost URLs.
S3 doesn't support server-side 301s, so we use meta-refresh + canonical + noindex."""

import os

DOMAIN = "https://www.jackpoker.xyz"

# Map old ghost URLs → new correct URLs
REDIRECTS = {
    "en/index.html": "/",
    "en/promo-code/index.html": "/promo-code.html",
    "en/log-in/index.html": "/",
    "en/registration/index.html": "/",
    "en/payment-methods/index.html": "/bonuses.html",
    "en/tournaments/index.html": "/tournaments.html",
    # Also create direct .html versions for edge cases
    "en/promo-code.html": "/promo-code.html",
    "en/log-in.html": "/",
    "en/registration.html": "/",
    "en/payment-methods.html": "/bonuses.html",
    "en/tournaments.html": "/tournaments.html",
}

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="robots" content="noindex, follow">
  <link rel="canonical" href="{canonical}">
  <meta http-equiv="refresh" content="0;url={target}">
  <title>Redirecting to JackPoker</title>
  <script>window.location.replace("{target}");</script>
</head>
<body>
  <p>This page has moved. <a href="{target}">Click here</a> if not redirected.</p>
</body>
</html>"""

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    count = 0
    
    for old_path, new_path in REDIRECTS.items():
        full_path = os.path.join(base_dir, old_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        target = f"{DOMAIN}{new_path}"
        canonical = target
        
        with open(full_path, 'w') as f:
            f.write(TEMPLATE.format(target=target, canonical=canonical))
        
        count += 1
        print(f"  {old_path} → {new_path}")
    
    print(f"\nCreated {count} redirect pages")

if __name__ == "__main__":
    main()
