#!/bin/bash
# 886828.xyz 部署脚本

set -e

echo "🚀 开始部署 886828.xyz"

# 检查 Vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "⚠️  安装 Vercel CLI..."
    npm i -g vercel
fi

# 进入项目目录
cd /home/w/.openclaw/workspace-taizi/886828-site

# 更新数据
echo "📡 更新招标数据..."
source venv/bin/activate
python3 update_data.py

# 部署到 Vercel
echo "🌐 部署到 Vercel..."
vercel --prod

echo "✅ 部署完成！"
echo ""
echo "📊 访问网站：https://886828-municipal-bids.vercel.app"
echo "🔧 管理后台：https://vercel.com/dashboard"
