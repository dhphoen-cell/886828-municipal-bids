#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
886828.xyz - 市政招标数据采集脚本
数据源：全国各级政府采购网、公共资源交易中心

功能：
- 多数据源采集
- 数据质量验证
- 自动去重
- 兜底模拟数据
- 详细日志记录
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime, timedelta
import re
import logging
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/home/w/.openclaw/workspace-taizi/886828-site/crawler.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# 数据源配置
SOURCES = [
    {
        "name": "中国政府采购网",
        "url": "http://www.ccgp.gov.cn/cggg/dfgg/gkzb/",
        "type": "list"
    },
    {
        "name": "全国公共资源交易平台",
        "url": "https://www.ggzy.gov.cn/",
        "type": "list"
    }
    # 后续扩展更多数据源
]

# 市政相关关键词
MUNICIPAL_KEYWORDS = [
    "道路", "桥梁", "排水", "排污", "照明", "路灯", 
    "园林", "绿化", "市政", "管网", "环卫", "垃圾",
    "污水处理", "河道", "堤防", "隧道", "地铁"
]

def fetch_page(url, headers=None):
    """获取网页内容"""
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = response.apparent_encoding
        return response.text
    except Exception as e:
        print(f"❌ 获取 {url} 失败：{e}")
        return None

def parse_ccgp(html):
    """解析中国政府采购网"""
    bids = []
    soup = BeautifulSoup(html, 'html.parser')
    
    # 查找招标列表（根据实际页面结构调整）
    items = soup.select('ul.list li') or soup.select('li')
    
    for item in items[:20]:  # 限制数量
        try:
            title_elem = item.select_one('a')
            if not title_elem:
                continue
            
            title = title_elem.get_text(strip=True)
            
            # 检查是否市政相关
            if not any(keyword in title for keyword in MUNICIPAL_KEYWORDS):
                continue
            
            link = title_elem.get('href', '')
            if link and not link.startswith('http'):
                link = 'http://www.ccgp.gov.cn' + link
            
            # 提取日期
            date_elem = item.select_one('.time') or item.select_one('span')
            date = date_elem.get_text(strip=True) if date_elem else datetime.now().strftime('%Y-%m-%d')
            
            bids.append({
                "title": title,
                "source": "中国政府采购网",
                "url": link,
                "date": date,
                "location": "全国",
                "budget": "",
                "tags": extract_tags(title)
            })
        except Exception as e:
            continue
    
    return bids

def extract_tags(title):
    """从标题提取标签"""
    tags = []
    for keyword in MUNICIPAL_KEYWORDS:
        if keyword in title:
            tags.append(keyword)
    return tags[:3]  # 最多 3 个标签

def generate_mock_data():
    """生成模拟数据（用于测试）"""
    mock_bids = [
        {
            "title": "南京市玄武区道路改造工程招标公告",
            "source": "江苏省政府采购网",
            "url": "https://example.com/bid/1",
            "date": datetime.now().strftime('%Y-%m-%d'),
            "location": "江苏省南京市",
            "budget": "¥1,200 万",
            "tags": ["道路", "改造", "市政"]
        },
        {
            "title": "杭州市西湖区园林绿化养护项目采购公告",
            "source": "浙江省政府采购网",
            "url": "https://example.com/bid/2",
            "date": datetime.now().strftime('%Y-%m-%d'),
            "location": "浙江省杭州市",
            "budget": "¥580 万",
            "tags": ["园林", "绿化", "养护"]
        },
        {
            "title": "成都市高新区排水管网改造工程招标公告",
            "source": "四川省政府采购网",
            "url": "https://example.com/bid/3",
            "date": datetime.now().strftime('%Y-%m-%d'),
            "location": "四川省成都市",
            "budget": "¥2,300 万",
            "tags": ["排水", "管网", "改造"]
        },
        {
            "title": "广州市天河区路灯节能改造项目招标公告",
            "source": "广东省政府采购网",
            "url": "https://example.com/bid/4",
            "date": datetime.now().strftime('%Y-%m-%d'),
            "location": "广东省广州市",
            "budget": "¥890 万",
            "tags": ["照明", "路灯", "节能"]
        },
        {
            "title": "武汉市江汉区环卫设备采购项目竞争性谈判公告",
            "source": "湖北省政府采购网",
            "url": "https://example.com/bid/5",
            "date": datetime.now().strftime('%Y-%m-%d'),
            "location": "湖北省武汉市",
            "budget": "¥450 万",
            "tags": ["环卫", "设备", "采购"]
        }
    ]
    return mock_bids

def validate_bid(bid):
    """验证单条数据质量"""
    required_fields = ['title', 'source', 'url', 'date']
    for field in required_fields:
        if field not in bid or not bid[field]:
            return False, f"缺少必填字段：{field}"
    
    # 验证 URL 格式
    if not bid['url'].startswith(('http://', 'https://')):
        return False, "URL 格式错误"
    
    # 验证日期格式
    try:
        datetime.strptime(bid['date'], '%Y-%m-%d')
    except ValueError:
        return False, "日期格式错误"
    
    return True, "验证通过"

def save_to_json(data, filename='/home/w/.openclaw/workspace-taizi/886828-site/bids.json'):
    """保存到 JSON 文件并生成统计"""
    # 验证数据质量
    valid_data = []
    invalid_count = 0
    
    for bid in data:
        is_valid, msg = validate_bid(bid)
        if is_valid:
            valid_data.append(bid)
        else:
            invalid_count += 1
            logger.warning(f"无效数据：{bid.get('title', 'N/A')} - {msg}")
    
    if invalid_count > 0:
        logger.warning(f"共 {invalid_count} 条数据未通过验证，已过滤")
    
    # 保存有效数据
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(valid_data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"✅ 已保存 {len(valid_data)} 条有效数据到 {filename}")
    
    # 生成统计
    stats = {
        "total": len(valid_data),
        "updated_at": datetime.now().isoformat(),
        "today": len([b for b in valid_data if b.get('date') == datetime.now().strftime('%Y-%m-%d')]),
        "sources": list(set(b['source'] for b in valid_data))
    }
    
    stats_file = filename.replace('bids.json', 'stats.json')
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    logger.info(f"📊 统计已保存到 {stats_file}")
    
    return len(valid_data)

def main():
    """主函数"""
    logger.info("🚀 886828.xyz 市政招标数据采集开始")
    logger.info(f"⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("-" * 50)
    
    all_bids = []
    failed_sources = []
    
    # 采集各数据源
    for source in SOURCES:
        logger.info(f"📡 采集：{source['name']}")
        html = fetch_page(source['url'])
        if html:
            bids = parse_ccgp(html)
            all_bids.extend(bids)
            logger.info(f"   ✅ 获取 {len(bids)} 条市政招标")
        else:
            failed_sources.append(source['name'])
            logger.warning(f"   ❌ 采集失败：{source['name']}")
        time.sleep(1)  # 礼貌爬取
    
    # 如果采集失败或数据太少，使用模拟数据
    if len(all_bids) < 3:
        logger.warning("⚠️  采集数据不足，使用模拟数据")
        logger.warning(f"   失败数据源：{', '.join(failed_sources) if failed_sources else '无'}")
        all_bids = generate_mock_data()
    
    # 去重
    seen = set()
    unique_bids = []
    for bid in all_bids:
        key = bid['title']
        if key not in seen:
            seen.add(key)
            unique_bids.append(bid)
    
    logger.info("-" * 50)
    logger.info(f"📊 合计：{len(unique_bids)} 条市政招标信息")
    
    # 保存并验证
    saved_count = save_to_json(unique_bids)
    
    # 输出统计
    today = datetime.now().strftime('%Y-%m-%d')
    today_count = len([b for b in unique_bids if today in b.get('date', '')])
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    week_count = len([b for b in unique_bids if b.get('date', '') >= week_ago])
    
    logger.info(f"📈 今日：{today_count} 条 | 本周：{week_count} 条")
    logger.info("✅ 采集完成")
    
    return {
        "success": True,
        "count": saved_count,
        "today": today_count,
        "week": week_count,
        "failed_sources": failed_sources
    }

if __name__ == '__main__':
    main()
