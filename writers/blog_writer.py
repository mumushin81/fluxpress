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
    tech_stack = analysis.get("tech_stack", [])
    folders = analysis.get("folders", [])
    main_files = analysis.get("main_files", [])

    sections: List[Dict[str, str]] = []

    sections.append({
        "title": "프로젝트 배경",
        "content": _intro_paragraph(analysis)
    })

    if features:
        bullet_md = "\n".join(f"- {f}" for f in features)
        sections.append({"title": "핵심 기능", "content": bullet_md})

    if folders:
        tree_preview = "\n".join(f"- {p}" for p in folders[:12])
        sections.append({"title": "디렉터리 구조", "content": tree_preview})

    if tech_stack:
        sections.append({"title": "기술 스택", "content": ", ".join(tech_stack)})

    if main_files:
        sections.append({"title": "주요 엔트리 파일", "content": "\n".join(f"- {f}" for f in main_files)})

    sections.append({
        "title": "활용 아이디어",
        "content": _business_ideas(analysis)
    })

    sections.append({
        "title": "설치 및 실행",
        "content": "1. 리포지토리 클론\n2. 의존성 설치\n3. 환경변수(.env) 설정\n4. `python scripts/run_github_blog.py --url <repo>` 실행"
    })

    return sections


def generate_blog(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Return structured blog draft using template + analysis.
    Replace body generation with Codex prompt in production.
    """
    repo = analysis.get("repo_name", "project")
    title = f"{repo} — 오픈소스 자동 소개"
    subtitle = analysis.get("description", "")
    sections = _build_sections(analysis)
    body_md = _compose_body(title, subtitle, analysis.get("summary", ""), sections)
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
    filler = "\n\n" + "이 프로젝트를 통한 자동화, 확장성, 유지보수 방법을 깊게 다룹니다. "
    while len(text) < target_len:
        text += filler
    return text[:target_len]


def _seo_keywords(analysis: Dict[str, Any]) -> List[str]:
    base = analysis.get("tech_stack", [])
    repo = analysis.get("repo_name", "")
    extras = ["github open source", repo] if repo else ["github open source"]
    return list(dict.fromkeys([*base, *extras]))


# ---------------------------------------------------------------------------

def _intro_paragraph(analysis: Dict[str, Any]) -> str:
    repo = analysis.get("repo_name", "이 프로젝트")
    desc = analysis.get("description", "오픈소스")
    return (
        f"{repo}는 {desc}를 중심으로 한 실제 구현 사례입니다. "
        "개발자가 빠르게 기능을 파악하고 바로 활용할 수 있도록 README와 코드 구조를 기반으로 핵심 정보를 추려 소개합니다."
    )


def _business_ideas(analysis: Dict[str, Any]) -> str:
    repo = analysis.get("repo_name", "이 프로젝트")
    ideas = [
        f"{repo}를 내부 서비스 템플릿으로 활용해 팀 온보딩 가속",
        "기술 스택 학습용 워크숍 자료로 재가공",
        "관련 라이브러리 성능 벤치마크 아티클 제작",
        "블로그 시리즈로 기능별 활용법 연재",
        "오픈소스 기여 가이드를 만들어 커뮤니티 확장"
    ]
    return "\n".join(f"- {i}" for i in ideas)


def _compose_body(title: str, subtitle: str, summary: str, sections: List[Dict[str, str]]) -> str:
    body_md = f"# {title}\n\n{subtitle}\n\n## 개요\n{summary}\n\n"
    # 템플릿 주요 섹션
    body_md += "## 문제 제기\n오늘날 개발자는 수많은 오픈소스 중 필요한 것을 고르는 데 시간이 많이 듭니다. 자동화된 리포 분석과 정리된 블로그 글은 탐색 비용을 줄여줍니다.\n\n"
    for sec in sections:
        body_md += f"### {sec['title']}\n{sec['content']}\n\n"
    body_md += "## 마무리\n본 소개 글은 로컬 Codex 파이프라인이 자동 생성했습니다. 추가 기능(이미지, 퍼블리싱)을 연결하면 완전 자동 블로그를 운영할 수 있습니다.\n\n"
    body_md += "## CTA\n- GitHub 리포 방문\n- 별(Star) 추가\n- 이슈/PR로 기여\n- 블로그 구독\n"
    return body_md


__all__ = ["generate_blog", "BLOG_TEMPLATE_PATH"]
