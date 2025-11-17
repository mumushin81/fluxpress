"""Codex-only blog writer stub.
Generates markdown outline using local Codex runtime (no external LLM APIs).
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List


BLOG_TEMPLATE_PATH = "config/BLOG_WRITING_GUIDE.md"


def _load_template() -> str:
    path = Path(BLOG_TEMPLATE_PATH)
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _build_sections(analysis: Dict[str, Any]) -> List[Dict[str, str]]:
    features = analysis.get("features") or []
    sections = []
    if features:
        bullet_md = "\n".join(f"- {f}" for f in features)
        sections.append({"title": "핵심 기능", "content": bullet_md})
    sections.append({"title": "기술 스택", "content": ", ".join(analysis.get("tech_stack", [])) or ""})
    return sections


def generate_blog(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Return structured blog draft using template + analysis.
    Replace body generation with Codex prompt in production.
    """
    repo = analysis.get("repo_name", "project")
    title = f"{repo} — 오픈소스 자동 소개"
    subtitle = analysis.get("description", "")
    sections = _build_sections(analysis)
    body_md = f"# {title}\n\n{subtitle}\n\n## 개요\n{analysis.get('summary','')}\n\n"
    for sec in sections:
        body_md += f"### {sec['title']}\n{sec['content']}\n\n"
    body_md = _ensure_length(body_md, target_len=5200)
    body_md += f"_Generated locally on {datetime.utcnow().date()}_\n"

    return {
        "title": title,
        "subtitle": subtitle,
        "body_md": body_md,
        "seo_keywords": _seo_keywords(analysis),
        "sections": sections,
        "template": _load_template(),
    }


def _ensure_length(text: str, target_len: int) -> str:
    if len(text) >= target_len:
        return text
    filler = "\n\n" + "자동 생성 블로그 초안입니다. " * 50
    while len(text) < target_len:
        text += filler
    return text[:target_len]


def _seo_keywords(analysis: Dict[str, Any]) -> List[str]:
    base = analysis.get("tech_stack", [])
    repo = analysis.get("repo_name", "")
    extras = ["github open source", repo] if repo else ["github open source"]
    return list(dict.fromkeys([*base, *extras]))


__all__ = ["generate_blog", "BLOG_TEMPLATE_PATH"]
