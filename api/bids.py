import json
from datetime import datetime
import os

# Vercel Python Serverless Function
# The function name must be 'handler' and receive (request, response) or just request

def handler(request):
    """
    Vercel Serverless Function Handler
    Exports a handler function at module level
    """
    path = request.path if hasattr(request, 'path') else '/'
    
    try:
        # 处理 /api/bids
        if path == '/api/bids' or path.startswith('/api/bids'):
            bids_path = os.path.join(os.path.dirname(__file__), '..', 'bids.json')
            with open(bids_path, 'r', encoding='utf-8') as f:
                bids = json.load(f)
            
            response_data = {
                "success": True,
                "data": bids[:20],
                "count": len(bids),
                "timestamp": datetime.now().isoformat()
            }
            
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(response_data, ensure_ascii=False)
            }
        
        # 处理 /api/stats
        elif path == '/api/stats' or path.startswith('/api/stats'):
            stats_path = os.path.join(os.path.dirname(__file__), '..', 'stats.json')
            try:
                with open(stats_path, 'r', encoding='utf-8') as f:
                    stats = json.load(f)
            except:
                stats = {
                    "today": 28,
                    "week": 156,
                    "sources": 50,
                    "last_update": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(stats, ensure_ascii=False)
            }
        
        # 404
        return {
            "statusCode": 404,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Not Found"})
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"success": False, "error": str(e)})
        }
