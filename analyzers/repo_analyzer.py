"""Analyzes collected repository artifacts to extract structured insights."""
from __future__ import annotations

import re
from typing import Dict, Any, List


def _extract_description(readme: str) -> str:
    # naive: first non-empty line without markdown heading hashes
    for line in readme.splitlines():
        line = line.strip().lstrip("# ")
        if line:
            return line
    return ""


def _extract_features(readme: str) -> List[str]:
    bullets = re.findall(r"^-\s+(.+)$", readme, flags=re.MULTILINE)
    return bullets[:10]


def analyze_repo(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    """Derive summary, tech stack, and key insights from snapshot."""
    readme = snapshot.get("readme_text", "")
    folders: List[str] = snapshot.get("folders", [])
    tech_stack: List[str] = snapshot.get("tech_stack", [])
    description = snapshot.get("description") or _extract_description(readme)
    summary = readme[:500] + ("..." if len(readme) > 500 else "")
    features = _extract_features(readme)
    return {
        "repo_name": snapshot.get("repo_name", ""),
        "description": description,
        "summary": summary,
        "folders": folders,
        "main_files": snapshot.get("main_files", []),
        "tech_stack": tech_stack,
        "features": features,
        "insights": {
            "readme_length": len(readme),
            "folder_count": len(folders),
            "file_count": len(snapshot.get("file_list", [])),
        },
    }


__all__ = ["analyze_repo"]
