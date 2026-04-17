# 应用项目

致富经旗下 **4 个独立应用**，覆盖工具网站、协作平台、数据仪表盘和移动应用。

---

## 项目一览

<div class="project-grid">

<div class="project-card online">

### 🛠️ 小伍工具箱 (xiaowutools)

**状态：** ✅ 已上线 · **版本：** v2.1.0 · **技术栈：** Next.js 14 + Tailwind

AI 工具导航网站 — 370+ 在线工具集合，涵盖短视频下载、图片转 ICO、微信截图生成等实用工具。

**标签：** `AI 导航` `工具集` `SEO`

[→ 查看项目文档](./xiaowutools) · [→ 在线访问](https://xiaowutools.com)

</div>

<div class="project-card dev">

### 🤝 TeamClaw 协作平台

**状态：** 🔨 开发中 · **版本：** v0.1.0 · **技术栈：** Tauri 2.x + React 19

全栈协作平台 — AI Agent 编排 + 项目管理 + 知识库，Tauri 2 桌面端 + 本地 SQLite。

**标签：** `Agent` `协作` `Tauri 桌面端`

[→ 查看项目文档](./teamclaw) · [→ 设计文档](./teamclaw/architecture)

</div>

<div class="project-card online">

### 📊 Projects Dashboard

**状态：** ✅ 已上线 · **版本：** v1.1.0 · **技术栈：** Next.js 16 + Supabase

致富经项目集合大盘 — 集中展示所有子项目状态、技术栈、部署信息和活动流。

**标签：** `监控` `仪表盘` `项目集`

[→ 查看项目文档](./projects-dashboard) · [→ 在线访问](https://dashboard.baoganai.com)

</div>

<div class="project-card dev">

### 📜 Poetry App 诗词应用

**状态：** 🔨 开发中 · **版本：** v0.5.0 · **技术栈：** Expo + React Native

跨平台诗词学习应用 — 中阿双语诗词阅读、收藏与学习，含 AI 翻译和古诗词数据库。

**标签：** `诗词` `教育` `双语` `Expo`

[→ 查看项目文档](./poetry-app)

</div>

</div>

---

## 仓库地址

| 项目 | GitHub 仓库 |
|------|-------------|
| xiaowutools | [weisiwu/zhifujing-tools](https://github.com/weisiwu/zhifujing-tools) |
| TeamClaw | [weisiwu/teamclaw](https://github.com/weisiwu/teamclaw) |
| Dashboard | [weisiwu/ZFJdashboard](https://github.com/weisiwu/ZFJdashboard) |
| Poetry App | 本地开发（无远程仓库） |

## 目录结构

```
apps/
├── xiaowutools/          # 小伍工具箱 — Next.js 14 工具网站
├── teamclaw/             # TeamClaw — Tauri 桌面协作平台
│   ├── src-tauri/        # Rust 后端 (Tauri)
│   ├── src/              # React 前端 (Vite)
│   └── project/          # PRD 与架构设计文档
├── projects-dashboard/   # 项目仪表盘 — Next.js 16
└── poetry-app/           # 诗词应用 — Expo 跨平台
```
