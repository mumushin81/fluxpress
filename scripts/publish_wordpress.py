#!/usr/bin/env python
"""Publisher skeleton for WordPress/Tistory/Velog."""
from __future__ import annotations

import os
import json
from typing import Optional

try:
    import requests  # type: ignore
except Exception:  # pragma: no cover
    requests = None  # type: ignore


def publish_wordpress(title: str, html: str) -> Optional[str]:
    url = os.getenv("PUBLISH_WORDPRESS_URL")
    key = os.getenv("PUBLISH_WORDPRESS_KEY")
    if not url or not key or not requests:
        print("[publish] WordPress not configured or requests missing; skipped")
        return None
    payload = {"title": title, "content": html, "status": "publish"}
    headers = {"Authorization": f"Bearer {key}"}
    resp = requests.post(f"{url}/wp-json/wp/v2/posts", json=payload, headers=headers, timeout=10)
    if resp.ok:
        link = resp.json().get("link")
        print(f"[publish] WordPress published: {link}")
        return link
    print("[publish] WordPress failed:", resp.text)
    return None


def publish_tistory(title: str, html: str) -> None:
    token = os.getenv("PUBLISH_TISTORY_TOKEN")
    if not token or not requests:
        print("[publish] Tistory not configured; skipped")
        return
    # Placeholder: add actual Tistory API endpoint parameters
    print("[publish] Tistory stub invoked")


def publish_velog(title: str, html: str) -> None:
    cookie = os.getenv("PUBLISH_VELOG_COOKIE")
    if not cookie or not requests:
        print("[publish] Velog not configured; skipped")
        return
    print("[publish] Velog stub invoked")


def main() -> None:
    sample = {"title": "sample post", "html": "<p>Hello</p>"}
    link = publish_wordpress(sample["title"], sample["html"])
    publish_tistory(sample["title"], sample["html"])
    publish_velog(sample["title"], sample["html"])
    print("Publish complete. Link:", link)


if __name__ == "__main__":
    main()
