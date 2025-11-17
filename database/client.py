"""Supabase client thin wrapper.
Falls back to no-op when supabase-py is unavailable (offline dev).
"""
from __future__ import annotations

from typing import Dict, Any, List

try:  # optional dependency
    from supabase import create_client
except Exception:  # pragma: no cover - missing in sandbox
    create_client = None  # type: ignore


class SupabaseClient:
    def __init__(self, url: str, key: str):
        self.url = url
        self.key = key
        self.client = create_client(url, key) if (url and key and create_client) else None

    def insert(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if self.client:
            try:
                res = self.client.table(table).insert(data).execute()
                return {"status": "ok", "data": res.data}
            except Exception as e:  # tolerant if table missing
                return {"status": "error", "error": str(e)}
        return {"status": "noop", "table": table, "data": data}

    def fetch_waiting_prompts(self) -> List[Dict[str, Any]]:
        if self.client:
            res = self.client.table("image_prompts").select("*").eq("status", "waiting").execute()
            return res.data or []
        return []


__all__ = ["SupabaseClient"]
