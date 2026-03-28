import json
from datetime import datetime
import os

def handler(request):
    """Vercel Serverless Function Handler"""
    
    # 获取当前目录（Vercel 部署后文件在 /var/task）
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    
    try:
        # 处理 /api/bids
        if request.path == '/api/bids':
            bids_path = os.path.join(parent_dir, 'bids.json')
            with open(bids_path, 'r', encoding='utf-8') as f:
                bids = json.load(f)
            
            response_data = {
                "success": True,
                "data": bids[:20],  # 返回最新 20 条
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
        elif request.path == '/api/stats':
            stats_path = os.path.join(parent_dir, 'stats.json')
            try:
                with open(stats_path, 'r', encoding='utf-8') as f:
                    stats = json.load(f)
            except:
                # 默认统计数据
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
            "headers": {
                "Content-Type": "application/json"
            },
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
