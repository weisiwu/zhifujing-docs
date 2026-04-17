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
├── docs/
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
│   │   ├── lib/
│   │   ├── login/
│   │   ├── overview/
│   │   ├── project/
│   │   ├── settings/
│   │   ├── staff/
│   │   ├── tasks/
│   │   ├── usage/
│   │   ├── error.tsx
│   │   ├── global-error.tsx
│   │   ├── layout.tsx
│   │   ├── loading.tsx
│   │   ├── not-found.tsx
│   │   ├── page.tsx
│   │   ├── robots.ts
│   │   ├── sitemap.ts
│   ├── components/
│   │   ├── animation/
│   │   ├── animations/
│   │   ├── auth/
│   │   ├── batch-operations/
│   │   ├── charts/
│   │   ├── command-palette/
│   │   ├── compare/
│   │   ├── dashboard/
│   │   ├── data/
│   │   ├── empty-states/
│   │   ├── features/
│   │   ├── feedback/
│   │   ├── health/
│   │   ├── kanban/
│   │   ├── layout/
│   │   ├── markdown/
│   │   ├── project/
│   │   ├── skeletons/
│   │   ├── ui/
│   │   ├── usage/
│   │   ├── Breadcrumb.tsx
│   │   ├── ErrorBoundary.tsx
│   │   ├── FavoritesSection.tsx
```

## 最近更新

| Commit | 说明 |
|--------|------|
| `ffc7ff8` | fix: 修复307重定向+更新4项目数据+详情页增加GitHub/Docs链接+删除根目录重复大盘 |
| `20bcfd7` | iter-3: Supabase客户端配置和API改造 - 完成supabase客户端集成 |
| `2d5f05b` | iter-1: Supabase数据库表设计和种子数据 - 添加Supabase客户端和类型定义 |
| `5f7bc60` | iter-10: 功能增加 - 项目健康状态指示、右键上下文菜单、项目对比功能 |
| `0aa578c` | iter-9: 样式改版 - 表单组件/模态框抽屉/表格样式 |

---
*最后同步: 2026-04-17 18:00*
