# projects-dashboard（项目仪表盘）

> 功能丰富的项目管理 Dashboard，集成数据可视化、拖拽排序、SEO 自动化、API 文档生成等功能。

## 技术栈

| 类别 | 技术 |
|------|------|
| 框架 | Next.js 16 + React 19 |
| 语言 | TypeScript |
| 样式 | Tailwind CSS v4 |
| 后端 | Supabase |
| 可视化 | Recharts 3 |
| 拖拽 | @dnd-kit (core + sortable) |
| 动画 | Framer Motion |
| 数据获取 | SWR |
| 验证 | Zod |
| 测试 | Vitest + Testing Library |
| API 文档 | next-swagger-doc + swagger-ui-react |
| 暗色模式 | next-themes |
| 环境变量 | @t3-oss/env-nextjs |
| 限流 | rate-limiter-flexible |
| 包分析 | @next/bundle-analyzer |

## 核心功能

### 🎯 项目管理
- 拖拽排序（dnd-kit）
- 项目状态追踪
- Supabase 数据持久化

### 📊 数据可视化
- Recharts 图表（折线图、柱状图、饼图等）
- 实时数据更新（SWR）

### 🔍 SEO 优化
- 自动生成 SEO 图片（`generate:seo-images` 脚本）
- 结构化元数据

### 📖 API 文档
- Swagger UI 自动生成
- 基于 Zod Schema 的类型安全 API

### 🧪 测试与质量
- Vitest 单元测试 + Testing Library 组件测试
- 测试覆盖率报告
- 环境变量 Schema 验证（@t3-oss/env-nextjs）
- 包体积分析（`ANALYZE=true next build`）

## 特色亮点

- 使用 **Next.js 16 + React 19** 最新版本
- 完整的 **测试体系**（Vitest + Testing Library + 覆盖率）
- **类型安全** 全链路（Zod + TypeScript）
- **暗色模式** 开箱即用
