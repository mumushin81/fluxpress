#!/usr/bin/env python
from pathlib import Path
from datetime import datetime

ARTICLES_DIR = Path(__file__).resolve().parent.parent / "articles" / "final"


def collect_posts():
    posts = []
    for html in sorted(ARTICLES_DIR.glob("*.html")):
        if html.name == "index.html":
            continue
        title = html.stem.replace('_—_', ' — ').replace('_', ' ')
        posts.append({"title": title, "href": html.name})
    return posts


def render(posts):
    cards = "\n".join(
        f"<a class='card' href='{p['href']}'><div class='card-title'>{p['title']}</div></a>"
        for p in posts
    )
    return f"""<!doctype html>
<html lang='ko'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>Auto GitHub Blogger — Articles</title>
  <style>
    body {{ font-family: 'Inter', system-ui, -apple-system, sans-serif; margin: 0; padding: 32px; background:#f7f8fa; }}
    h1 {{ margin: 0 0 12px 0; }}
    .meta {{ color:#666; margin-bottom:24px; }}
    .grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(240px,1fr)); gap:16px; }}
    .card {{ display:block; padding:16px; background:#fff; border-radius:10px; box-shadow:0 4px 12px rgba(0,0,0,0.06); color:#111; text-decoration:none; transition: transform .15s ease, box-shadow .15s ease; }}
    .card:hover {{ transform: translateY(-3px); box-shadow:0 10px 20px rgba(0,0,0,0.08); }}
    .card-title {{ font-weight:600; line-height:1.4; }}
  </style>
</head>
<body>
  <h1>Auto GitHub Blogger</h1>
  <div class='meta'>총 {len(posts)}편 · 생성 {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC</div>
  <div class='grid'>
    {cards}
  </div>
</body>
</html>"""


def main():
    posts = collect_posts()
    html = render(posts)
    (ARTICLES_DIR / "index.html").write_text(html, encoding="utf-8")
    print(f"index generated with {len(posts)} posts")


if __name__ == "__main__":
    main()
