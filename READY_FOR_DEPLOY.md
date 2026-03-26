# 🚀 886828.xyz GitHub 部署 - 待皇上执行

## ✅ 太子已完成

- [x] 初始化 Git 仓库
- [x] 创建 .gitignore
- [x] 提交所有代码（2 次 commit）
- [x] 创建 GitHub Actions 工作流（自动更新数据）
- [x] 编写部署指南

---

## 📋 皇上只需 3 步

### 第 1 步：创建 GitHub 仓库

访问：https://github.com/new

填写：
- **Repository name**: `886828-municipal-bids`
- **Description**: 全国市政招标情报平台
- **Visibility**: Public（推荐）或 Private

点击 **"Create repository"**

---

### 第 2 步：推送代码

复制以下命令（替换 `YOUR_USERNAME` 为你的 GitHub 用户名）：

```bash
cd /home/w/.openclaw/workspace-taizi/886828-site

# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/886828-municipal-bids.git

# 重命名分支并推送
git branch -M main
git push -u origin main
```

---

### 第 3 步：Vercel 绑定

1. 访问：https://vercel.com/new
2. 用 GitHub 账号登录
3. 找到 `886828-municipal-bids` 仓库
4. 点击 **"Import"**
5. 点击 **"Deploy"**

等待 1-2 分钟，部署完成后会显示访问地址！

---

## 🎉 部署成功后

### 访问地址
- Vercel 默认：`https://886828-municipal-bids.vercel.app`
- 自定义域名：`https://886828.xyz`（需配置 DNS）

### 自动更新
- GitHub Actions 每 6 小时自动运行爬虫
- 更新 `bids.json` 和 `stats.json`
- Vercel 自动重新部署

### 手动触发更新
访问：`https://github.com/YOUR_USERNAME/886828-municipal-bids/actions`
点击 "Update Bids Data" → "Run workflow"

---

## 📞 需要帮助？

太子已准备完整文档：
- `GITHUB_DEPLOY.md` - 详细部署指南
- `README.md` - 项目说明
- `DEPLOYMENT_REPORT.md` - 部署报告

---

**请皇上执行上述 3 步，完成后告知太子，太子继续配置飞书推送和域名绑定。** 🙇
