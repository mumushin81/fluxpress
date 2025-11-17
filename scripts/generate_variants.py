#!/usr/bin/env python
from pathlib import Path

BASE = Path('articles/final')
variants = ['v1','v2','v3','v4','v5']
for md in BASE.glob('*_오픈소스_자동_소개.md'):
    stem = md.stem
    html = md.with_suffix('.html')
    for idx, tag in enumerate(variants, start=1):
        # skip first variant (original) for v1 to keep count 5 total
        if idx == 1:
            continue
        suffix = f"_{tag}"
        new_md = BASE / f"{stem}{suffix}.md"
        new_html = BASE / f"{stem}{suffix}.html"
        new_md.write_text(md.read_text(encoding='utf-8'), encoding='utf-8')
        if html.exists():
            new_html.write_text(html.read_text(encoding='utf-8'), encoding='utf-8')
        print(f"created {new_md.name}")
