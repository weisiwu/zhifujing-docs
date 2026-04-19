# poetry-app（诗词应用）

> 基于 Expo 的跨平台诗词学习应用，支持 iOS/Android/Web。

## 技术栈

| 类别 | 技术 |
|------|------|
| 语言 | React ^19.1.0 |
| 语言 | TypeScript |
| 样式 | Tailwind CSS |
| 状态管理 | Zustand |

## 关键依赖

| 包名 | 版本 |
|------|------|
| `@tauri-apps/api` | ^2 |
| `@tauri-apps/plugin-opener` | ^2 |
| `clsx` | ^2.1.1 |
| `lucide-react` | ^0.511.0 |
| `react` | ^19.1.0 |
| `react-dom` | ^19.1.0 |
| `tailwind-merge` | ^3.3.0 |
| `zustand` | ^5.0.5 |

## 项目结构

```
poetry-app/
├── _backup/
│   ├── AGENTS.md
│   ├── CLAUDE.md
│   ├── README.md
│   ├── 最终产品原型定稿.md
│   ├── 最终技术方案设计.md
│   ├── 本地数据库.md
├── data/
│   ├── dynasties.json
│   ├── poems.json
│   ├── poets.json
├── docs/
│   ├── tests/
│   │   ├── mvp-test-cases.md
│   ├── 产品需求确认点/
│   │   ├── 00-产品需求汇总.md
│   │   ├── 01-最终确认-目标用户画像.md
│   │   ├── 02-最终确认-核心价值主张.md
│   │   ├── 03-最终确认-产品差异化定位.md
│   │   ├── 04-最终确认-竞品分析.md
│   │   ├── 05-最终确认-用户使用场景.md
│   │   ├── 06-最终确认-信息架构.md
│   │   ├── 07-最终确认-核心功能列表.md
│   │   ├── 08-13-最终确认-功能设计.md
│   │   ├── 14-18-最终确认-视觉与交互.md
│   │   ├── 19-24-最终确认-商业模式.md
│   │   ├── 25-31-最终确认-内容与技术.md
│   ├── issue-list.md
│   ├── 最终产品原型定稿.md
│   ├── 最终技术方案设计.md
│   ├── 本地数据库.md
├── public/
├── src/
│   ├── components/
│   │   ├── Sidebar.tsx
│   ├── hooks/
│   ├── pages/
│   │   ├── FavoritesPage.tsx
│   │   ├── HistoryPage.tsx
│   │   ├── HomePage.tsx
│   │   ├── PoemDetailPage.tsx
│   │   ├── PoemsPage.tsx
│   │   ├── PoetDetailPage.tsx
│   │   ├── PoetsPage.tsx
│   │   ├── SearchPage.tsx
│   ├── stores/
│   │   ├── appStore.ts
│   │   ├── poetryStore.ts
│   ├── styles/
│   ├── types/
│   │   ├── index.ts
│   ├── App.tsx
│   ├── main.tsx
│   ├── vite-env.d.ts
├── src-tauri/
│   ├── gen/
│   │   ├── schemas/
│   ├── icons/
│   ├── src/
```

---
*最后同步: 2026-04-19 12:00*
