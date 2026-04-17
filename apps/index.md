# 应用项目

致富经项目下包含 **4 个独立应用**，涵盖工具网站、协作平台、数据仪表盘和移动应用。

## 项目一览

| 项目 | 类型 | 技术栈 | 状态 | 在线地址 |
|------|------|--------|------|----------|
| [xiaowutools](./xiaowutools-v2) | 在线工具网站 | Next.js 14 + Tailwind | ✅ 运行中 | Vercel |
| [teamclaw](./teamclaw) | 桌面协作平台 | Tauri 2.x + React 19 | 🔨 开发中 | 本地 |
| [projects-dashboard](./projects-dashboard) | 项目仪表盘 | Next.js 16 + Supabase | ✅ 运行中 | Vercel |
| [poetry-app](./poetry-app) | 跨平台移动应用 | Expo + React Native | ✅ 运行中 | Expo EAS |

## 仓库地址

| 项目 | GitHub 仓库 |
|------|-------------|
| xiaowutools | [weisiwu/zhifujing-tools](https://github.com/weisiwu/zhifujing-tools) |
| teamclaw | [weisiwu/teamclaw](https://github.com/weisiwu/teamclaw) |
| dashboard | [weisiwu/ZFJdashboard](https://github.com/weisiwu/ZFJdashboard) |
| poetry-app | 本地开发（无远程仓库） |

## 目录结构

```
apps/
├── xiaowutools/          # 小工具箱 — Next.js 14 工具网站
├── teamclaw/             # TeamClaw — Tauri 桌面协作平台
│   ├── src-tauri/        # Rust 后端 (Tauri)
│   ├── src/              # React 前端 (Vite)
│   └── project/          # PRD 与架构设计文档
├── projects-dashboard/   # 项目仪表盘 — Next.js 16
└── poetry-app/           # 诗词应用 — Expo 跨平台
```
