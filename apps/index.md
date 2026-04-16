# 应用项目

致富经项目下包含 5 个独立应用，涵盖工具网站、协作平台、数据仪表盘和移动应用。

## 项目一览

| 项目 | 类型 | 技术栈 | 说明 |
|------|------|--------|------|
| [xiaowutools-v2](./xiaowutools-v2) | 工具网站 | Next.js 14 + Tailwind | 短视频下载、图片转换、微信截图生成等在线工具 |
| [teamclaw](./teamclaw) | 协作平台 | Next.js 14 + Express + PG | 团队项目管理、文档协作、飞书集成 |
| [projects-dashboard](./projects-dashboard) | 数据仪表盘 | Next.js 16 + Supabase + Recharts | 项目展示、拖拽排序、数据可视化 |
| [openclaw-agents-dashboard](./openclaw-agents-dashboard) | 管理面板 | Next.js 16 + React 19 | OpenClaw Agent 运行状态管理 |
| [poetry-app](./poetry-app) | 移动应用 | Expo + Supabase | 跨平台诗词学习应用（iOS/Android/Web） |

## 技术架构概览

```
致富经/
├── apps/
│   ├── xiaowutools-v2/        # 在线工具箱 (Next.js Web)
│   ├── teamclaw/              # 团队协作平台 (Full-Stack)
│   ├── projects-dashboard/    # 项目仪表盘 (Next.js + Supabase)
│   ├── openclaw-agents-dashboard/  # Agent 管理面板
│   └── poetry-app/            # 诗词应用 (Expo RN)
├── 个人/学习/                  # 学习笔记
├── 学习笔记/                   # 技术调研文章
└── docs/                      # 本文档站点
```
