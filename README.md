# 886828.xyz - 全国市政招标情报平台

免费、实时、智能的市政招标信息平台。

## 🚀 快速部署

### 本地测试

```bash
# 1. 安装依赖
python3 -m venv venv
source venv/bin/activate
pip install beautifulsoup4 requests

# 2. 运行爬虫
python3 crawler.py

# 3. 启动 API 服务
python3 api/bids.py

# 4. 打开浏览器
open index.html
```

### Vercel 部署

```bash
# 1. 安装 Vercel CLI
npm i -g vercel

# 2. 登录
vercel login

# 3. 部署
vercel --prod
```

### 定时更新数据

```bash
# 添加 crontab
crontab -e

# 每 30 分钟更新一次
*/30 * * * * cd /home/w/.openclaw/workspace-taizi/886828-site && source venv/bin/activate && python3 update_data.py >> /tmp/886828.log 2>&1
```

## 📁 文件结构

```
886828-site/
├── index.html          # 网站首页
├── crawler.py          # 数据采集爬虫
├── update_data.py      # 数据更新脚本
├── bids.json           # 招标数据（自动生成）
├── stats.json          # 统计数据（自动生成）
├── vercel.json         # Vercel 部署配置
├── api/
│   └── bids.py         # API 服务端
└── venv/               # Python 虚拟环境
```

## 🔧 配置

### 添加数据源

编辑 `crawler.py` 中的 `SOURCES` 列表：

```python
SOURCES = [
    {
        "name": "江苏省政府采购网",
        "url": "http://www.ccgp-jiangsu.gov.cn/",
        "type": "list"
    },
    # 添加更多...
]
```

### 自定义关键词

编辑 `MUNICIPAL_KEYWORDS` 列表以匹配更多市政项目类型。

## 📊 API 接口

### 获取招标列表

```
GET /api/bids
```

响应：
```json
{
  "success": true,
  "data": [...],
  "count": 5,
  "timestamp": "2026-03-26T18:28:41"
}
```

### 获取统计数据

```
GET /api/stats
```

响应：
```json
{
  "today": 28,
  "week": 156,
  "sources": 50,
  "last_update": "2026-03-26 18:28:41"
}
```

## 📝 待办事项

- [ ] 添加更多数据源（省级、地市级）
- [ ] 实现 AI 智能摘要
- [ ] 飞书推送集成
- [ ] 微信公众号对接
- [ ] 用户订阅系统
- [ ] 搜索功能优化

## 📄 许可证

MIT License

---

**886828.xyz** - 不错过每一个市政项目机会
