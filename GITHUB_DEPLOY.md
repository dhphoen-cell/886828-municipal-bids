# 🚀 GitHub + Vercel 部署指南

## 第一步：创建 GitHub 仓库

### 方式 A：网页创建（推荐）

1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `886828-municipal-bids` 或 `886828-xyz`
   - **Description**: 全国市政招标情报平台 - 免费实时智能
   - **Visibility**: Public（公开）或 Private（私有）
   - 不要勾选 "Add README" 等选项
3. 点击 "Create repository"

### 方式 B：CLI 创建（需要 GitHub CLI）

```bash
gh repo create 886828-municipal-bids --public --source=. --remote=origin --push
```

---

## 第二步：推送代码到 GitHub

创建仓库后，GitHub 会显示推送指令。执行：

```bash
cd /home/w/.openclaw/workspace-taizi/886828-site

# 添加远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/886828-municipal-bids.git

# 推送代码
git branch -M main
git push -u origin main
```

---

## 第三步：Vercel 绑定 GitHub

1. 访问 https://vercel.com/new
2. 登录 Vercel（可用 GitHub 账号直接登录）
3. 点击 "Import Git Repository"
4. 找到 `886828-municipal-bids` 仓库，点击 "Import"
5. 配置部署选项：
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: （留空）
   - **Output Directory**: （留空）
6. 点击 "Deploy"

---

## 第四步：绑定自定义域名

1. 在 Vercel Dashboard 进入项目
2. 点击 "Settings" → "Domains"
3. 添加域名：`886828.xyz`
4. 按提示配置 DNS：
   - **Type**: A
   - **Name**: @
   - **Value**: `76.76.21.21`（Vercel IP）
   
   或
   
   - **Type**: CNAME
   - **Name**: www
   - **Value**: `cname.vercel-dns.com`

5. 等待 DNS 生效（通常几分钟到几小时）

---

## 第五步：配置自动部署

Vercel 已自动配置：
- ✅ Push 到 `main` 分支 → 自动部署到生产环境
- ✅ Pull Request → 自动创建预览环境

无需额外配置！

---

## 第六步：配置定时更新（重要）

由于是静态托管，需要外部服务定时运行爬虫更新数据。

### 方案 A：GitHub Actions（推荐）

创建 `.github/workflows/update-bids.yml`：

```yaml
name: Update Bids Data

on:
  schedule:
    - cron: '0 */6 * * *'  # 每 6 小时
  workflow_dispatch:  # 手动触发

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m venv venv
          source venv/bin/activate
          pip install beautifulsoup4 requests
      
      - name: Run crawler
        run: |
          source venv/bin/activate
          python crawler.py
      
      - name: Commit and push
        run: |
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git config user.name "github-actions[bot]"
          git add bids.json stats.json
          git commit -m "Auto-update: $(date)" || exit 0
          git push
```

### 方案 B：外部服务器

在有公网 IP 的服务器上设置 crontab：
```bash
crontab /home/w/.openclaw/workspace-taizi/886828-site/crontab.txt
```

---

## 📊 部署后访问地址

| 类型 | 地址 |
|------|------|
| Vercel 默认域名 | `https://886828-municipal-bids.vercel.app` |
| 自定义域名 | `https://886828.xyz` |

---

## ✅ 检查清单

- [ ] GitHub 仓库已创建
- [ ] 代码已推送
- [ ] Vercel 已绑定仓库
- [ ] 首次部署成功
- [ ] 自定义域名已配置（可选）
- [ ] GitHub Actions 已启用（定时更新）
- [ ] 飞书 Webhook 已配置（推送通知）

---

## 🆘 常见问题

### Q: Vercel 部署失败？
A: 检查 `vercel.json` 配置，确保没有语法错误。

### Q: 爬虫无法访问目标网站？
A: GitHub Actions 环境可能有网络限制，考虑使用外部服务器。

### Q: 如何查看部署日志？
A: Vercel Dashboard → Deployments → 点击具体部署 → View Logs

---

**创建人**: 太子  
**更新时间**: 2026-03-27
