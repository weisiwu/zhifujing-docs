# projects-dashboard（项目仪表盘）

> This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## 技术栈

| 类别 | 技术 |
|------|------|
| 框架 | Next.js 16.1.6 |
| 语言 | React 19.2.3 |
| 语言 | TypeScript |
| 样式 | Tailwind CSS |
| 数据获取 | SWR |
| 可视化 | Recharts |
| 后端 | Supabase |
| 测试 | Vitest |

## 关键依赖

| 包名 | 版本 |
|------|------|
| `@dnd-kit/core` | ^6.3.1 |
| `@dnd-kit/sortable` | ^10.0.0 |
| `@dnd-kit/utilities` | ^3.2.2 |
| `@next/bundle-analyzer` | ^16.1.6 |
| `@supabase/supabase-js` | ^2.99.1 |
| `@t3-oss/env-nextjs` | ^0.13.10 |
| `date-fns` | ^4.1.0 |
| `framer-motion` | ^12.36.0 |
| `next` | 16.1.6 |
| `next-swagger-doc` | ^0.4.1 |
| `next-themes` | ^0.4.6 |
| `rate-limiter-flexible` | ^10.0.0 |
| `react` | 19.2.3 |
| `react-dom` | 19.2.3 |
| `recharts` | ^3.8.0 |
| `swagger-ui-react` | ^5.32.0 |
| `swr` | ^2.4.1 |
| `zod` | ^4.3.6 |

## 项目结构

```
projects-dashboard/
├── .vercel/
│   ├── project.json
├── context/
│   ├── project-context.md
├── docs/
│   ├── PROMPT_SUPABASE_MIGRATION.md
├── overview-docs/
│   ├── .vitepress/
│   │   ├── cache/
│   │   ├── theme/
│   │   ├── config.mts
│   ├── apps/
│   │   ├── index.md
│   │   ├── marker-tracker.md
│   │   ├── poetry-app.md
│   │   ├── projects-dashboard.md
│   │   ├── teamclaw.md
│   │   ├── xiaowutools.md
│   ├── notes/
│   │   ├── index.md
│   │   ├── learning.md
│   │   ├── practice.md
│   ├── index.md
│   ├── package-lock.json
│   ├── package.json
│   ├── vercel.json
├── public/
│   ├── manifest.json
├── scripts/
│   ├── generate-seo-images.ts
├── src/
│   ├── __tests__/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── utils/
│   │   ├── ProjectCard.test.tsx
│   │   ├── setup.ts
│   ├── app/
│   │   ├── api/
│   │   ├── api-reference/
│   │   ├── components/
│   │   ├── data/
│   │   ├── items/
│   │   ├── lib/
│   │   ├── login/
│   │   ├── overview/
│   │   ├── privacy/
│   │   ├── project/
│   │   ├── settings/
│   │   ├── staff/
│   │   ├── tasks/
│   │   ├── terms/
│   │   ├── usage/
│   │   ├── error.tsx
│   │   ├── global-error.tsx
│   │   ├── layout.tsx
│   │   ├── loading.tsx
│   │   ├── not-found.tsx
│   │   ├── page.tsx
```

## 最近更新

| Commit | 说明 |
|--------|------|
| `e42a3c0` | fix: 首页移除学习笔记卡片，只保留5个项目 |
| `d20a6a8` | feat: 添加致富经大盘总览文档站 (overview-docs) |
| `ffc7ff8` | fix: 修复307重定向+更新4项目数据+详情页增加GitHub/Docs链接+删除根目录重复大盘 |
| `20bcfd7` | iter-3: Supabase客户端配置和API改造 - 完成supabase客户端集成 |
| `2d5f05b` | iter-1: Supabase数据库表设计和种子数据 - 添加Supabase客户端和类型定义 |

---
*最后同步: 2026-05-12 06:00*
