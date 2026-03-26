#!/bin/bash
# 886828.xyz 本地测试启动脚本

set -e

echo "🚀 启动 886828.xyz 本地测试服务器"
echo ""

cd /home/w/.openclaw/workspace-taizi/886828-site

# 激活虚拟环境
source venv/bin/activate

# 启动 API 服务（后台）
echo "📡 启动 API 服务..."
python3 api/bids.py &
API_PID=$!
echo "   API PID: $API_PID"

# 等待 1 秒
sleep 1

# 用 Python 启动静态文件服务
echo "🌐 启动静态文件服务..."
python3 -m http.server 8081 &
WEB_PID=$!
echo "   Web PID: $WEB_PID"

echo ""
echo "✅ 服务启动成功！"
echo ""
echo "📊 访问网站：http://localhost:8081"
echo "🔧 API 接口：http://localhost:8080/api/bids"
echo ""
echo "按 Ctrl+C 停止服务"

# 等待用户中断
wait
