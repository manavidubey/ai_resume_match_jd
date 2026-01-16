import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        response = {
            "message": "Resume uploaded successfully",
            "status": "success",
            "candidate_id": "demo_candidate_123"
        }
        
        self.wfile.write(json.dumps(response).encode())
