# Projects Dashboard（项目仪表盘）

> 基于 Next.js 16 的项目管理仪表盘，集中展示致富经所有项目的状态、指标和文档。

## 基本信息

| 项目 | 信息 |
|------|------|
| 名称 | projects-dashboard (dashboard) |
| 框架 | Next.js 16.1 (App Router) |
| 语言 | TypeScript + React 19 |
| 样式 | Tailwind CSS |
| 后端 | Supabase (PostgreSQL) |
| 认证 | Google OAuth (Supabase Auth) |
| 部署 | Vercel |
| GitHub | [weisiwu/ZFJdashboard](https://github.com/weisiwu/ZFJdashboard) |
| 在线地址 | https://dashboard-delta-ruddy.vercel.app |

## 功能

- **项目一览** — 4 个子项目的状态、版本、技术栈展示
- **项目详情** — 单项目的详细信息、GitHub 链接、文档站入口
- **GitHub 集成** — 仓库 Stars、Forks、最新提交等信息
- **暗色主题** — 支持深色/浅色主题切换
- **ISR + SEO** — 增量静态渲染、Open Graph 图片、站点地图

## 目录结构

```
projects-dashboard/
├── src/
│   ├── app/              # Next.js App Router
│   │   ├── page.tsx      # 首页（项目一览）
│   │   ├── project/[id]/ # 项目详情页
│   │   ├── data/         # 项目静态数据
│   │   ├── lib/          # 工具库与类型
│   │   └── components/   # React 组件
│   ├── components/       # 通用 UI 组件
│   ├── hooks/            # React Hooks
│   ├── middleware.ts      # 认证中间件
│   └── lib/              # 认证与配置
├── scripts/              # SEO 图片生成
├── supabase-setup.sql    # 数据库初始化 SQL
└── vercel.json           # Vercel 部署配置
```

## 管理的项目

| 项目 | GitHub 仓库 | 文档站 |
|------|-------------|--------|
| xiaowutools | weisiwu/zhifujing-tools | — |
| teamclaw | weisiwu/teamclaw | — |
| dashboard | weisiwu/ZFJdashboard | — |
| poetry-app | — | — |
