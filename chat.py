import os
import requests
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
        
        if not ANTHROPIC_API_KEY:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "API key not set"}).encode())
            return

        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length))

        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
            },
            json=body,
            timeout=60,
        )

        self.send_response(resp.status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(resp.content)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
