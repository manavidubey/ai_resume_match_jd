import json
import os
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        response = {
            "message": "Resume Matcher API is working!",
            "status": "success",
            "timestamp": "2024-01-16"
        }
        
        self.wfile.write(json.dumps(response).encode())
        
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        response = {
            "message": "POST request received",
            "status": "success"
        }
        
        self.wfile.write(json.dumps(response).encode())
