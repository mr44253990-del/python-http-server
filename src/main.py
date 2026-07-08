import os
import json
import sqlite3
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# ডাটাবেস সেটআপ
def init_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
    conn.commit()
    conn.close()

init_db()

class CustomHandler(SimpleHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        
        if path == '/status':
            self._set_headers()
            self.wfile.write(json.dumps({"status": "running", "message": "Python app is running with Wasmer!"}).encode('utf-8'))
        
        elif path == '/users':
            conn = sqlite3.connect('app.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users')
            users = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
            conn.close()
            self._set_headers()
            self.wfile.write(json.dumps(users).encode('utf-8'))
        
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode('utf-8'))

    def do_POST(self):
        path = urlparse(self.path).path
        if path == '/users':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            conn = sqlite3.connect('app.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (name) VALUES (?)', (data['name'],))
            conn.commit()
            conn.close()
            
            self._set_headers(201)
            self.wfile.write(json.dumps({"message": "User added"}).encode('utf-8'))
        else:
            self._set_headers(404)

if __name__ == "__main__":
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 8000))
    server = HTTPServer((host, port), CustomHandler)
    print(f"Starting server on http://{host}:{port}")
    server.serve_forever()
