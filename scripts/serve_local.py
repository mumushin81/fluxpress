#!/usr/bin/env python
import http.server
import socketserver
from pathlib import Path

PORT = 8000
ROOT = Path(__file__).resolve().parent.parent / "articles" / "final"

class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Serve files from ROOT regardless of cwd
        rel = path.lstrip('/') or 'index.html'
        return str((ROOT / rel).resolve())

if __name__ == "__main__":
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        print(f"Serving {ROOT} at http://localhost:{PORT}")
        httpd.serve_forever()
