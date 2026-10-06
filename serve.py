"""Local dev server for the NEXKO site.

Same as `python3 -m http.server`, but tells the browser not to cache anything,
so edits to the page and images always show up on a normal refresh.

    python3 serve.py          # http://localhost:5173
    python3 serve.py 8080     # custom port
"""
import http.server
import sys


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Expires", "0")
        super().end_headers()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5173
    http.server.ThreadingHTTPServer(("", port), NoCacheHandler).serve_forever()
