#!/usr/bin/env python3
"""Inject the shared Superintelligence SG ecosystem bar and footer block.

Usage: python3 scripts/si-ecosystem.py [--check]

Reads partials/si-ecosystem.html, marks this site's link with aria-current="page",
then writes the CSS (end of <head>), bar (start of <body>, after a skip link) and
footer block (after </footer>) into every site page. Re-running replaces the blocks
between the si-eco markers, so the script is idempotent. Site files are mirrored to
dist/ afterwards because the hosted build serves dist/ while GitHub Pages serves the root.
--check exits non-zero if any page or dist/ copy is out of date.
"""
import pathlib
import re
import shutil
import sys

SITE = 'https://superintelligencesg.ai'
ROOT = pathlib.Path(__file__).resolve().parent.parent
PARTIAL = ROOT / 'partials' / 'si-ecosystem.html'
# Root entries that are not part of the published site (kept out of dist/).
NOT_PUBLISHED = {'.git', '.openai', 'dist', 'docs', 'partials', 'scripts', 'CNAME', 'README.md'}


def blocks():
    text = PARTIAL.read_text()
    found = {}
    for name in ('css', 'bar', 'foot'):
        m = re.search(rf'<!-- si-eco:{name} -->.*?<!-- /si-eco:{name} -->', text, re.S)
        if m:
            found[name] = m.group(0).replace(
                f'<a href="{SITE}">', f'<a href="{SITE}" aria-current="page">')
    return found


def place(html, name, block):
    marked = re.compile(rf'<!-- si-eco:{name} -->.*?<!-- /si-eco:{name} -->', re.S)
    if marked.search(html):
        return marked.sub(lambda _: block, html, count=1)
    if name == 'css':
        return html.replace('</head>', block + '\n</head>', 1)
    if name == 'bar':
        skip = re.search(r'<body[^>]*>\s*<a class="skip"[^>]*>.*?</a>', html, re.S)
        anchor = skip or re.search(r'<body[^>]*>', html)
        return html[:anchor.end()] + '\n' + block + '\n' + html[anchor.end():]
    if name == 'foot':
        end = html.rfind('</footer>') + len('</footer>')
        return html[:end] + '\n' + block + html[end:]
    raise ValueError(name)


def pages():
    return sorted(p for p in ROOT.rglob('*.html')
                  if p.relative_to(ROOT).parts[0] not in NOT_PUBLISHED)


def site_files():
    for p in sorted(ROOT.rglob('*')):
        rel = p.relative_to(ROOT)
        if p.is_file() and rel.parts[0] not in NOT_PUBLISHED:
            yield p, ROOT / 'dist' / rel


def main():
    check = '--check' in sys.argv
    stale = []
    parts = blocks()
    for page in pages():
        html = page.read_text()
        new = html
        for name, block in parts.items():
            new = place(new, name, block)
        if new != html:
            stale.append(str(page.relative_to(ROOT)))
            if not check:
                page.write_text(new)
    for src, dst in site_files():
        if not dst.exists() or dst.read_bytes() != src.read_bytes():
            stale.append(str(dst.relative_to(ROOT)))
            if not check:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
    for path in stale:
        print(('stale: ' if check else 'updated: ') + path)
    if check and stale:
        sys.exit(1)


if __name__ == '__main__':
    main()
