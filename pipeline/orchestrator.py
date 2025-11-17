"""High-level orchestration of the GitHub-to-blog pipeline."""
from __future__ import annotations

import json
from pathlib import Path
from collectors.github_collector import collect_repo, save_snapshot
from analyzers.repo_analyzer import analyze_repo
from writers.blog_writer import generate_blog
from prompts.prompt_generator import generate_prompts
from database.client import SupabaseClient


class Pipeline:
    def __init__(self, supabase: SupabaseClient, workdir: Path = Path(".cache")):
        self.supabase = supabase
        self.workdir = workdir
        self.workdir.mkdir(parents=True, exist_ok=True)

    def run(self, repo_url: str) -> dict:
        snapshot = collect_repo(repo_url, self.workdir / "repo")
        save_snapshot(snapshot, self.workdir / "snapshot.json")
        analysis = analyze_repo(snapshot)
        draft = generate_blog(analysis)
        prompts = generate_prompts(draft)
        self._persist(draft, prompts)
        self._write_local_outputs(draft)
        return {
            "snapshot": snapshot,
            "analysis": analysis,
            "draft": draft,
            "prompts": prompts,
        }

    # Internal helpers -------------------------------------------------
    def _persist(self, draft: dict, prompts: list[dict]) -> None:
        self.supabase.insert("blog_drafts", draft)
        for p in prompts:
            self.supabase.insert("image_prompts", p)

    def _write_local_outputs(self, draft: dict) -> None:
        out_dir = Path("articles/final")
        out_dir.mkdir(parents=True, exist_ok=True)
        slug = draft.get("title", "draft").replace(" ", "_")
        (out_dir / f"{slug}.md").write_text(draft.get("body_md", ""), encoding="utf-8")
        html = self._markdown_to_html(draft.get("body_md", ""))
        (out_dir / f"{slug}.html").write_text(html, encoding="utf-8")

    @staticmethod
    def _markdown_to_html(md: str) -> str:
        # very small converter to keep dependencies light; replace with markdown lib if needed
        html = md.replace("\n\n", "<br><br>").replace("\n", "<br>")
        return f"<html><body>{html}</body></html>"


__all__ = ["Pipeline"]
