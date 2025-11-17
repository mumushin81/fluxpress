"""GitHub Repository Collector.
Collects README, tree, main files, contributors, tech stack.
Network use is optional: if cloning fails (offline sandbox), returns minimal metadata.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import urllib.request
from pathlib import Path
from typing import Dict, Any, List


def _run(cmd: List[str], cwd: Path | None = None) -> str:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Command failed")
    return result.stdout


def clone_repo(repo_url: str, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    repo_path = dest_dir / "repo"
    if repo_path.exists():
        return repo_path
    _run(["git", "clone", "--depth", "1", repo_url, str(repo_path)])
    return repo_path


def read_readme(repo_path: Path) -> str:
    for name in ("README.md", "README.MD", "readme.md"):
        p = repo_path / name
        if p.exists():
            return p.read_text(encoding="utf-8", errors="ignore")
    return ""


def tree_paths(repo_path: Path) -> List[str]:
    paths: List[str] = []
    for p in repo_path.rglob("*"):
        if p.is_dir():
            continue
        rel = p.relative_to(repo_path)
        parts = rel.parts
        if ".git" in parts:
            continue
        paths.append(str(rel))
    return paths


def guess_tech_stack(paths: List[str], readme: str) -> List[str]:
    stack: set[str] = set()
    ext_map = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".jsx": "javascript",
        ".go": "go",
        ".rs": "rust",
        ".java": "java",
        ".rb": "ruby",
        ".php": "php",
        ".swift": "swift",
        ".kt": "kotlin",
    }
    for path in paths:
        ext = Path(path).suffix
        if ext in ext_map:
            stack.add(ext_map[ext])
    # simple README keyword sniffing
    keywords = {
        "supabase": "supabase",
        "fastapi": "fastapi",
        "flask": "flask",
        "django": "django",
        "react": "react",
        "next.js": "next.js",
        "vite": "vite",
        "docker": "docker",
    }
    lower = readme.lower()
    for k, v in keywords.items():
        if k in lower:
            stack.add(v)
    return sorted(stack)


def collect_repo(repo_url: str, dest_dir: Path = Path("/tmp/github_repo")) -> Dict[str, Any]:
    """Clone repo, read README, compute tree and basic metadata.
    If cloning fails (e.g., offline), returns minimal fallback structure.
    """
    repo_name = repo_url.rstrip("/").split("/")[-1]
    try:
        repo_path = clone_repo(repo_url, dest_dir)
        readme_text = read_readme(repo_path)
        files = tree_paths(repo_path)
        folders = sorted({str(Path(f).parent) for f in files if "/" in f})
    except Exception:
        repo_path = None
        readme_text = ""
        files = []
        folders = []

    main_files = [f for f in files if re.match(r"(src/)?(main|app|server|index)\.(py|js|ts|tsx|go)$", f)]
    tech_stack = guess_tech_stack(files, readme_text)
    contributors = fetch_contributors(repo_url)

    return {
        "repo_name": repo_name,
        "description": "",  # filled by analyzer
        "readme_text": readme_text,
        "folders": folders,
        "main_files": main_files,
        "tech_stack": tech_stack,
        "contributors": contributors,
        "file_list": files,
        "repo_path": str(repo_path) if repo_path else None,
    }


def fetch_contributors(repo_url: str) -> List[str]:
    """Lightweight GitHub contributors fetch; returns [] when offline or rate-limited."""
    token = os.getenv("GITHUB_TOKEN")
    m = re.match(r"https?://[^/]+/([^/]+)/([^/]+)", repo_url)
    if not m:
        return []
    owner, repo = m.group(1), m.group(2)
    api = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    headers = {"User-Agent": "auto-github-blogger"}
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(api, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
            return [c.get("login", "") for c in data if isinstance(c, dict)]
    except Exception:
        return []


def save_snapshot(data: Dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


__all__ = ["collect_repo", "save_snapshot", "clone_repo"]
