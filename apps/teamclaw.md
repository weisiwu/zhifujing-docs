# teamclaw（TeamClaw）

> 现代化团队协作平台，提供项目管理、文档协作和团队沟通功能。前后端分离架构，支持飞书集成与多 Agent 自动迭代。

## 技术栈

### 前端

| 类别 | 技术 |
|------|------|
| 框架 | Next.js 14.2 (App Router) |
| 语言 | TypeScript + React 18 |
| UI | Tailwind CSS + shadcn/ui + Radix UI |
| 状态管理 | Zustand |
| 数据获取 | TanStack React Query |
| 可视化 | Recharts |
| Markdown | react-markdown + rehype-highlight + remark-gfm |
| PWA | @ducanh2912/next-pwa |

### 后端

| 类别 | 技术 |
|------|------|
| 运行时 | Node.js + Express |
| 数据库 | PostgreSQL |
| 缓存 | Redis |
| 安全 | Helmet |
| 导出 | xlsx + jszip |
| 容器 | Docker + Docker Compose |

### 质量保障

| 类别 | 技术 |
|------|------|
| 测试 | Vitest + Testing Library + Supertest |
| 代码规范 | Husky + lint-staged + Prettier + ESLint |

## 核心功能

### 📊 项目管理
- 看板视图
- 甘特图
- 里程碑追踪

### 📝 文档协作
- 实时 Markdown 编辑
- 版本控制
- 语法高亮

### 🤝 团队协作
- 任务分配与进度同步
- 通知中心
- 成员管理

### 📈 数据分析
- 可视化报表
- 团队效能分析
- 数据导出（Excel/ZIP）

### 🤖 自动化
- 飞书（Feishu）集成
- OpenClaw Multi-Agent 自动迭代（6 个 Agent 协作，GitHub Issues 驱动）
- 数据库迁移脚本

## 路由结构

```
/dashboard     → 仪表盘总览
/tasks         → 任务管理
/versions      → 版本管理
/members       → 成员管理
/settings      → 系统设置
```

## 项目文档

- `TECH_SPEC.md` — 技术规格详细说明
- `CONTRIBUTING.md` — 贡献指南
- `LOC.md` — 代码行数统计
