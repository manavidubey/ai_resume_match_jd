import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        response = {
            "message": "Job created successfully",
            "status": "success",
            "job_id": "demo_job_456"
        }
        
        self.wfile.write(json.dumps(response).encode())
        
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        response = {
            "job_id": "demo_job_456",
            "title": "Software Engineer",
            "description": "Demo job posting"
        }
        
        self.wfile.write(json.dumps(response).encode())
