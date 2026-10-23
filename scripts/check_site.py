#!/usr/bin/env python3
"""Check the deployable static site using only the Python standard library."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1] / 'site'
ORIGIN = 'https://runner.flrgroup.se'

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.ids, self.links, self.errors = path, set(), [], []
        self.headings, self.canonical, self.description = 0, [], []
        self.title, self.language, self.viewport = False, False, False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids: self.errors.append('duplicate id: ' + a['id'])
            self.ids.add(a['id'])
        if tag == 'html': self.language = a.get('lang') == 'en'
        if tag == 'title': self.title = True
        if tag == 'h1': self.headings += 1
        if tag == 'meta' and a.get('name') == 'description': self.description.append(a.get('content', ''))
        if tag == 'meta' and a.get('name') == 'viewport': self.viewport = True
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical.append(a.get('href', ''))
        if tag == 'img' and 'alt' not in a: self.errors.append('image missing alt')
        for key in ('href', 'src'):
            if a.get(key): self.links.append((a[key], tag))
        if tag in ('script', 'iframe'): self.errors.append('unexpected script or iframe')
        if tag == 'meta' and a.get('property') == 'og:image': self.links.append((a['content'], 'asset'))

pages = {}
for path in sorted(ROOT.rglob('*.html')):
    page = Page(path)
    page.feed(path.read_text())
    pages[path] = page
errors = []
for path, page in pages.items():
    rel = path.relative_to(ROOT)
    expected = ORIGIN + ('/' + str(rel).removesuffix('index.html') if path.name == 'index.html' else '/' + str(rel))
    for ok, message in [(page.language, 'missing English language'), (page.title, 'missing title'),
                        (page.headings == 1, 'expected one h1'), (page.viewport, 'missing viewport'),
                        (len(page.description) == 1 and bool(page.description[0]), 'missing description'),
                        (page.canonical == [expected], 'incorrect canonical URL')]:
        if not ok: page.errors.append(message)
    for href, tag in page.links:
        url = urlsplit(href)
        if url.scheme == 'mailto':
            if url.path != 'runner@flrgroup.se': page.errors.append('unexpected contact address')
            continue
        if url.scheme and url.scheme != 'https': page.errors.append('insecure external URL: ' + href)
        if url.netloc and url.netloc != 'runner.flrgroup.se':
            if tag != 'a': page.errors.append('external asset: ' + href)
            continue
        dest = (ROOT / unquote(url.path).lstrip('/')) if url.path.startswith('/') else path.parent / unquote(url.path)
        dest = dest.resolve()
        if not dest.is_relative_to(ROOT):
            page.errors.append('link escapes site: ' + href); continue
        if dest.is_dir(): dest /= 'index.html'
        if not dest.is_file(): page.errors.append('broken local link: ' + href); continue
        if url.fragment and dest in pages and unquote(url.fragment) not in pages[dest].ids:
            page.errors.append('missing fragment: ' + href)
    errors.extend(f'{rel}: {err}' for err in page.errors)
css = (ROOT / 'assets/style.css').read_text()
if re.search(r'@import|url\(\s*[\'"]?https?://', css): errors.append('CSS loads external resources')
for route in ['index.html', 'support/index.html', 'privacy/index.html', '404.html', 'robots.txt', 'sitemap.xml', '.nojekyll']:
    if not (ROOT / route).is_file(): errors.append('missing required file: ' + route)
ET.parse(ROOT / 'sitemap.xml')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f'PASS: {len(pages)} pages; local links and anchors, metadata, contact, and self-hosted assets verified.')
