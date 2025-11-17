#!/usr/bin/env python
"""Dedicated Tistory publisher stub."""
from __future__ import annotations

import os
import sys
try:
    import requests  # type: ignore
except Exception:  # pragma: no cover
    requests = None  # type: ignore


def publish(title: str, html: str) -> None:
    token = os.getenv("PUBLISH_TISTORY_TOKEN")
    if not token or not requests:
        print("[publish] Tistory not configured or requests missing")
        return
    # TODO: implement real endpoint call
    print(f"[publish] would send '{title}' to Tistory")


if __name__ == "__main__":
    publish("sample", "<p>sample</p>")
