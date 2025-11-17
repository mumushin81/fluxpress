"""Generate Midjourney prompts based on blog sections."""
from __future__ import annotations

from typing import List, Dict, Any


BASE_STYLE = "ultra-detailed, cinematic lighting, clean UI, trending on artstation"


def generate_prompts(draft: Dict[str, Any]) -> List[Dict[str, str]]:
    prompts: List[Dict[str, str]] = []
    sections = draft.get("sections") or []
    title = draft.get("title", "an open-source project")
    if not sections:
        prompts.append({
            "section": "hero",
            "prompt": f"Hero image for {title}, futuristic knowledge graph, {BASE_STYLE}"
        })
        return prompts

    for section in sections:
        sec_title = section.get("title", "section")
        detail = section.get("content", "")[:180]
        prompts.append({
            "section": sec_title,
            "prompt": f"Illustration for {title} - {sec_title}: {detail}, {BASE_STYLE}"
        })
    return prompts


__all__ = ["generate_prompts"]
