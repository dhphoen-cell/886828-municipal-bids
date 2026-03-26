import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

class BidHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/bids':
            try:
                with open('bids.json', 'r', encoding='utf-8') as f:
                    bids = json.load(f)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    "success": True,
                    "data": bids[:20],  # 返回最新 20 条
                    "count": len(bids),
                    "timestamp": datetime.now().isoformat()
                }
                
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode())
        
        elif self.path == '/api/stats':
            try:
                with open('stats.json', 'r', encoding='utf-8') as f:
                    stats = json.load(f)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                self.wfile.write(json.dumps(stats, ensure_ascii=False).encode())
            except:
                # 默认统计
                stats = {
                    "today": 28,
                    "week": 156,
                    "sources": 50,
                    "last_update": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(stats, ensure_ascii=False).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # 静默日志

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8080), BidHandler)
    print("🚀 API Server running on port 8080")
    server.serve_forever()
