#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
886828.xyz - 健康检查脚本
用于监控网站和数据状态
"""

import requests
import json
import sys
from datetime import datetime

WEBSITE_URL = "https://www.886928.xyz"
BIDS_URL = "https://www.886928.xyz/bids.json"
STATS_URL = "https://www.886928.xyz/stats.json"

def check_website():
    """检查网站可访问性"""
    try:
        response = requests.get(WEBSITE_URL, timeout=10)
        if response.status_code == 200:
            return True, f"网站正常 (HTTP {response.status_code})"
        else:
            return False, f"网站异常 (HTTP {response.status_code})"
    except Exception as e:
        return False, f"网站无法访问：{e}"

def check_bids_data():
    """检查招标数据"""
    try:
        response = requests.get(BIDS_URL, timeout=10)
        if response.status_code != 200:
            return False, f"数据文件异常 (HTTP {response.status_code})"
        
        data = response.json()
        if not isinstance(data, list):
            return False, "数据格式错误"
        
        count = len(data)
        if count == 0:
            return False, "数据为空"
        elif count < 3:
            return True, f"数据偏少 ({count}条)"
        else:
            return True, f"数据正常 ({count}条)"
    except Exception as e:
        return False, f"数据检查失败：{e}"

def check_stats():
    """检查统计信息"""
    try:
        response = requests.get(STATS_URL, timeout=10)
        if response.status_code != 200:
            return False, f"统计文件异常 (HTTP {response.status_code})"
        
        stats = response.json()
        updated_at = stats.get('updated_at', '未知')
        return True, f"统计正常 (更新于 {updated_at})"
    except Exception as e:
        return False, f"统计检查失败：{e}"

def main():
    print("=" * 50)
    print(f"886828.xyz 健康检查")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    results = []
    all_healthy = True
    
    # 检查网站
    healthy, msg = check_website()
    status = "✅" if healthy else "❌"
    print(f"{status} 网站：{msg}")
    results.append(("website", healthy, msg))
    if not healthy:
        all_healthy = False
    
    # 检查数据
    healthy, msg = check_bids_data()
    status = "✅" if healthy else "❌"
    print(f"{status} 数据：{msg}")
    results.append(("bids", healthy, msg))
    if not healthy:
        all_healthy = False
    
    # 检查统计
    healthy, msg = check_stats()
    status = "✅" if healthy else "❌"
    print(f"{status} 统计：{msg}")
    results.append(("stats", healthy, msg))
    if not healthy:
        all_healthy = False
    
    print("=" * 50)
    
    if all_healthy:
        print("🎉 所有检查通过，系统运行正常")
        return 0
    else:
        print("⚠️  发现异常，请检查日志")
        return 1

if __name__ == '__main__':
    sys.exit(main())
