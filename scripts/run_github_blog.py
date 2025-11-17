#!/usr/bin/env python
"""CLI to run GitHub → blog pipeline."""
from __future__ import annotations
import argparse
import os
from pathlib import Path
from pipeline.orchestrator import Pipeline
from database.client import SupabaseClient


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate blog draft from GitHub repo")
    parser.add_argument("--url", required=True, help="GitHub repository URL")
    args = parser.parse_args()

    supabase = SupabaseClient(os.getenv("SUPABASE_URL", ""), os.getenv("SUPABASE_KEY", ""))
    pipeline = Pipeline(supabase, workdir=Path(".cache"))
    result = pipeline.run(args.url)
    print("Draft title:", result["draft"].get("title"))
    print("Prompts queued:", len(result["prompts"]))


if __name__ == "__main__":
    main()
