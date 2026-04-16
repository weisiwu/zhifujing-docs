# teamclaw（TeamClaw）

> Teamclaw 是一个现代化的团队协作平台，提供项目管理、文档协作和团队沟通功能。

## 技术栈

| 类别 | 技术 |
|------|------|
| 框架 | Next.js 14.2.35 |
| 语言 | React ^18 |
| 语言 | TypeScript |
| 样式 | Tailwind CSS |
| 状态管理 | Zustand |
| 数据获取 | TanStack React Query |
| 可视化 | Recharts |
| 测试 | Vitest |

## 关键依赖

| 包名 | 版本 |
|------|------|
| `@base-ui/react` | ^1.3.0 |
| `@tanstack/react-query` | ^5.90.21 |
| `clsx` | ^2.1.1 |
| `helmet` | ^8.1.0 |
| `jszip` | ^3.10.1 |
| `lucide-react` | ^0.577.0 |
| `next` | 14.2.35 |
| `next-themes` | ^0.4.6 |
| `react` | ^18 |
| `react-dom` | ^18 |
| `react-markdown` | ^10.1.0 |
| `recharts` | ^3.8.0 |
| `rehype-highlight` | ^7.0.2 |
| `rehype-slug` | ^6.0.0 |
| `remark-gfm` | ^4.0.1 |
| `sonner` | ^2.0.7 |
| `tailwind-merge` | ^3.5.0 |
| `xlsx` | ^0.18.5 |
| `zustand` | ^5.0.12 |

## 项目结构

```
teamclaw/
├── .github/
│   ├── workflows/
│   │   ├── cd.yml
│   │   ├── ci.yml
├── .husky/
│   ├── _/
├── .pids/
├── .vercel/
│   ├── project.json
├── app/
│   ├── admin/
│   │   ├── agents/
│   │   ├── audit/
│   │   ├── config/
│   │   ├── webhooks/
│   ├── agent-team/
│   │   ├── page.tsx
│   ├── agent-tokens/
│   │   ├── page.tsx
│   ├── api/
│   │   ├── download/
│   │   ├── health/
│   │   ├── v1/
│   ├── api-tokens/
│   │   ├── page.tsx
│   ├── branches/
│   │   ├── page.tsx
│   ├── capabilities/
│   │   ├── page.tsx
│   ├── cron/
│   │   ├── page.tsx
│   ├── docs/
│   │   ├── [slug]/
│   │   ├── components/
│   │   ├── DocsPageClient.tsx
│   │   ├── page.tsx
│   ├── import/
│   │   ├── page.tsx
│   ├── lib/
│   │   ├── api/
│   │   ├── api-proxy.ts
│   │   ├── api-shared.ts
│   ├── login/
│   │   ├── page.tsx
│   ├── members/
│   │   ├── page.tsx
│   ├── messages/
│   │   ├── page.tsx
│   ├── monitor/
│   │   ├── page.tsx
│   ├── projects/
│   │   ├── [id]/
│   │   ├── page.tsx
│   ├── settings/
│   │   ├── page.tsx
│   ├── tags/
│   │   ├── [name]/
│   │   ├── new/
│   │   ├── page.tsx
```

## 最近更新

| Commit | 说明 |
|--------|------|
| `b09032a` | iter 45: 任务14「多端形态探索」第2轮 - modularizeImports修复+SW重建 |
| `4102d07` | iter 44: 任务14「多端形态探索」第1轮 - PWA基础设施搭建 |
| `0973bd4` | iter 43: 任务13「前端交互体验与动效升级」第1轮 - 页面过渡/列表动画/按钮反馈基础设施 |
| `097eb69` | iter 42: 任务12「配色方案与视觉风格全面刷新」第2轮（最终轮） |
| `e18521c` | iter 41: 任务12「配色方案与视觉风格全面刷新」第1轮 |

---
*最后同步: 2026-04-16 16:39*
