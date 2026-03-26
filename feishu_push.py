#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
886828.xyz - 飞书推送脚本
将最新招标信息推送到飞书群
"""

import json
import requests
from datetime import datetime

# 飞书 Webhook URL（需要配置）
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_KEY"

def load_bids():
    """加载招标数据"""
    try:
        with open('/home/w/.openclaw/workspace-taizi/886828-site/bids.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def send_feishu_message(bids):
    """发送飞书消息"""
    if not bids:
        print("⚠️  没有招标数据")
        return
    
    # 取最新 5 条
    latest = bids[:5]
    
    # 构建消息卡片
    content = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "🏗️ 市政招标日报"
                },
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**今日新增 {len(bids)} 条招标信息**\n更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}"
                    }
                },
                {
                    "tag": "divider"
                }
            ] + [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**{i+1}. {bid['title']}**\n📍 {bid.get('location', '未知')} | 💰 {bid.get('budget', '面议')} | ⏰ {bid.get('date', '未知')}"
                    }
                }
                for i, bid in enumerate(latest)
            ] + [
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "查看全部 →"
                            },
                            "url": "https://886828.xyz",
                            "type": "primary"
                        }
                    ]
                }
            ]
        }
    }
    
    # 发送请求
    headers = {'Content-Type': 'application/json'}
    response = requests.post(FEISHU_WEBHOOK, json=content, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('StatusCode') == 0:
            print("✅ 飞书推送成功")
            return True
        else:
            print(f"❌ 飞书推送失败：{result}")
            return False
    else:
        print(f"❌ 请求失败：{response.status_code}")
        return False

if __name__ == '__main__':
    bids = load_bids()
    if bids:
        send_feishu_message(bids)
        print(f"📊 共 {len(bids)} 条招标信息")
    else:
        print("⚠️  无数据")
