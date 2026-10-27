#!/usr/bin/env python3
"""Check field-note links to Navigator entries against the live API.

Usage: python3 scripts/check-navigator-links.py [entries.json]

For each field note, an entry counts as cited when its exact API name appears in the
note's <main> text (whole words; the longest name wins when names overlap, so "AI Verify
Foundation" does not also count as "AI Verify"). The script fails if a
directory.html?q= link names something that is not an API entry or is not named in
the note, or if a cited entry has no link. Pass a saved /v1/entries response to run offline.
"""
import html
import json
import pathlib
import re
import sys
import urllib.parse
import urllib.request

API = 'https://api.superintelligencesg.org/v1/entries'
ROOT = pathlib.Path(__file__).resolve().parent.parent
LINK = re.compile(r'href="https://superintelligencesg\.com/directory\.html\?q=([^"#&]+)"')


def entries():
    if len(sys.argv) > 1:
        return json.loads(pathlib.Path(sys.argv[1]).read_text())['entries']
    req = urllib.request.Request(API, headers={'User-Agent': 'si-ai-link-check'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)['entries']


def note_text(source):
    # Only the article itself: the shared header, ecosystem bar and footer (which carries
    # the founder disclosure naming Commons participants) are page chrome, not citations.
    main = re.search(r'<main[^>]*>(.*?)</main>', source, re.S)
    source = main.group(1) if main else source
    source = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', source, flags=re.S)
    source = re.sub(r'<!--.*?-->', ' ', source, flags=re.S)
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', source)))


def cited(text, names):
    hits = []
    for name in names:
        hits += [(m.start(), m.end(), name) for m in re.finditer(r'(?<!\w)' + re.escape(name) + r'(?!\w)', text)]
    hits.sort(key=lambda h: (h[0], h[0] - h[1]))
    found, end = set(), -1
    for start, stop, name in hits:
        if start >= end:
            found.add(name)
            end = stop
    return found


def main():
    names = {e['name'] for e in entries()}
    problems = 0
    for note in sorted((ROOT / 'field-notes').glob('*.html')):
        if note.name == 'index.html':
            continue
        source = note.read_text()
        named = cited(note_text(source), names)
        linked = {urllib.parse.unquote(q) for q in LINK.findall(source)}
        errors = [f'link to unknown entry: {n}' for n in sorted(linked - names)]
        errors += [f'link to entry the note does not name: {n}' for n in sorted((linked & names) - named)]
        errors += [f'named but not linked: {n}' for n in sorted(named - linked)]
        problems += len(errors)
        print(f'{note.name}: cites {len(named)} Navigator entries' + (f' ({", ".join(sorted(named))})' if named else ' (none)'))
        for e in errors:
            print('  ERROR ' + e)
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
