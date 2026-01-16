import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        response = {
            "matches": [
                {
                    "candidate_id": "demo_candidate_123",
                    "score": 85.5,
                    "skills_match": 78.0,
                    "experience_match": 82.0,
                    "overall_fit": "Strong fit for the position"
                }
            ],
            "status": "success"
        }
        
        self.wfile.write(json.dumps(response).encode())
