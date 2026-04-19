#!/usr/bin/env python3
"""Update all source HTML files to use WebP with JPG fallback, lazy loading, and font preconnect."""

import re
import os
import glob

def optimize_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = 0
    img_count = [0]  # Use list for mutability in nested function
    
    def replace_img(match):
        full_tag = match.group(0)
        img_count[0] += 1
        
        # Skip if already inside a <picture> element (check surrounding context)
        pos = match.start()
        preceding = content[max(0, pos-50):pos]
        if '<picture>' in preceding or '<source' in preceding:
            return full_tag
        
        # Extract src
        src_match = re.search(r'src="([^"]*\.jpg)"', full_tag)
        if not src_match:
            return full_tag
        
        jpg_src = src_match.group(1)
        webp_src = jpg_src.replace('.jpg', '.webp')
        
        # Add loading="lazy" for non-first images (first image is LCP)
        modified_tag = full_tag
        if 'loading=' not in modified_tag and img_count[0] > 1:
            modified_tag = modified_tag.replace('<img ', '<img loading="lazy" ')
        
        # Wrap in <picture> with WebP source
        picture = f'<picture><source srcset="{webp_src}" type="image/webp">{modified_tag}</picture>'
        return picture
    
    # Match img tags with .jpg src, not already wrapped in <picture>
    new_content = re.sub(
        r'<img[^>]*src="[^"]*\.jpg"[^>]*/?>',
        replace_img,
        content
    )
    
    if new_content != content:
        changes += 1
    content = new_content
    
    # Remove any double-wrapped <picture> tags (safety)
    content = content.replace('<picture><picture>', '<picture>')
    content = content.replace('</picture></picture>', '</picture>')
    
    # Add preconnect for Google Fonts before any stylesheet link
    # This helps ALL pages since fonts are loaded via CSS @import
    if 'preconnect' not in content:
        preconnect = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        
        # Try various stylesheet link patterns
        for pattern in [
            '<link rel="stylesheet" href="style.css"',
            '<link rel="stylesheet" href="../style.css"',
            "<link rel=\"stylesheet\" href='style.css'",
            "<link rel=\"stylesheet\" href='../style.css'",
        ]:
            if pattern in content:
                content = content.replace(pattern, preconnect + pattern, 1)
                changes += 1
                break
        else:
            # Fallback: insert before </head>
            if '</head>' in content:
                content = content.replace('</head>', preconnect + '</head>', 1)
                changes += 1
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return changes
    return 0

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    total_changes = 0
    files_changed = 0
    
    # Only process English source files (build system propagates to translations)
    patterns = ['*.html', 'compare/*.html', 'news/*.html']
    skip = ['404.html', 'check.html', 'review.html', 'google06ee58b7d2497d1a.html']
    
    for pattern in patterns:
        for filepath in sorted(glob.glob(os.path.join(root, pattern))):
            basename = os.path.basename(filepath)
            if basename in skip:
                continue
            if '/en/' in filepath:
                continue
                
            changes = optimize_html(filepath)
            if changes > 0:
                files_changed += 1
                total_changes += changes
                print(f"  {os.path.relpath(filepath, root)}: {changes} optimizations")
    
    print(f"\nTotal: {total_changes} changes across {files_changed} files")

if __name__ == '__main__':
    main()
