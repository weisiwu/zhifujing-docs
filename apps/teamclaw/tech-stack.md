---
title: TeamClaw 技术栈深度分析
---

# 技术栈深度分析

> 基于项目实际代码的依赖项分析，覆盖前端、后端（Rust/Tauri）、构建工具链三层。

---

## 1. 架构总览

```
┌──────────────────────────────────────────────┐
│                 TeamClaw v0.1.0               │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │       前端 (Vite + React 19)           │  │
│  │  React 19 · TypeScript 5.8 · Zustand  │  │
│  │  Tailwind CSS v4 · Lucide Icons        │  │
│  └────────────────┬───────────────────────┘  │
│                   │ @tauri-apps/api (IPC)     │
│  ┌────────────────▼───────────────────────┐  │
│  │       后端 (Rust / Tauri 2.x)          │  │
│  │  SQLite · rusqlite · serde · chrono    │  │
│  │  uuid · tauri-plugin-opener            │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

---

## 2. 前端依赖分析

### 2.1 运行时依赖（dependencies）

| 包名 | 版本 | 用途 | 分析 |
|------|------|------|------|
| `react` | ^19.1.0 | UI 框架 | React 19 最新稳定版，支持 Server Components（本项目未用）、use() hook、改进的 Suspense |
| `react-dom` | ^19.1.0 | DOM 渲染 | 与 React 19 配套，提供 createRoot API |
| `@tauri-apps/api` | ^2 | Tauri IPC | 核心桥接层，提供 `invoke()` 调用 Rust 后端命令、窗口管理、事件系统 |
| `@tauri-apps/plugin-opener` | ^2 | 文件/URL 打开 | Tauri 2 插件，用于打开外部链接和文件，替代 shell API |
| `zustand` | ^5.0.5 | 状态管理 | 轻量状态库 v5，使用 `create()` API，项目中通过 `useAppStore` 统一管理导航、项目、任务、统计 |
| `lucide-react` | ^0.511.0 | 图标库 | 提供 LayoutDashboard、FolderKanban、ListChecks、Settings 等图标 |
| `clsx` | ^2.1.1 | 条件类名 | 轻量 className 合并工具，处理条件样式 |
| `tailwind-merge` | ^3.3.0 | 类名合并 | 智能合并 Tailwind CSS 类名，解决冲突（如 `px-2 px-4` → `px-4`） |

### 2.2 开发依赖（devDependencies）

| 包名 | 版本 | 用途 | 分析 |
|------|------|------|------|
| `@types/react` | ^19.1.8 | React 类型 | TypeScript 类型定义 |
| `@types/react-dom` | ^19.1.6 | ReactDOM 类型 | TypeScript 类型定义 |
| `@vitejs/plugin-react` | ^4.6.0 | Vite React 插件 | 支持 JSX 转换、Fast Refresh、自动注入 React 导入 |
| `typescript` | ~5.8.3 | 类型系统 | 严格模式开启（`strict: true`），配置 ES2020 target + bundler moduleResolution |
| `vite` | ^7.0.4 | 构建工具 | Vite 7（2026 最新），原生 ESM、HMR、Rollup 构建 |
| `@tauri-apps/cli` | ^2 | Tauri CLI | 提供 `tauri dev`、`tauri build` 命令，管理 Rust 编译和前端打包 |
| `tailwindcss` | ^4 | CSS 框架 | Tailwind CSS v4（Rust 引擎），通过 `@import "tailwindcss"` 自动扫描 |
| `@tailwindcss/vite` | ^4 | Vite 插件 | Tailwind v4 的 Vite 集成，零配置内容检测 |

---

## 3. 后端依赖分析（Rust / Cargo.toml）

### 3.1 核心依赖

| Crate | 版本 | 用途 | 分析 |
|-------|------|------|------|
| `tauri` | 2 | 桌面框架 | Tauri 2.x 核心，提供 IPC、窗口管理、打包分发 |
| `tauri-plugin-opener` | 2 | 文件/URL 打开 | 与前端 `@tauri-apps/plugin-opener` 对应 |
| `serde` | 1 (derive) | 序列化 | Rust 标准序列化框架，用于 JSON 序列化/反序列化 |
| `serde_json` | 1 | JSON 处理 | 与 serde 配合，Tauri IPC 数据传输核心 |
| `rusqlite` | 0.31 (bundled) | SQLite 数据库 | **bundled 特性**：内置 SQLite 编译，无需系统安装。提供 `Connection`、`params!` 宏 |
| `chrono` | 0.4 (serde) | 时间处理 | UTC 时间、RFC3339 格式化，serde feature 支持序列化 |
| `uuid` | 1 (v4) | ID 生成 | UUID v4 随机生成，作为所有实体的主键 |
| `thiserror` | 1 | 错误处理 | 派生宏，简化自定义错误类型定义 |

### 3.2 构建依赖

| Crate | 版本 | 用途 |
|-------|------|------|
| `tauri-build` | 2 | Tauri 构建脚本，生成绑定代码 |

---

## 4. 关键设计模式分析

### 4.1 Tauri IPC 通信模式

```
前端 (React)                    后端 (Rust)
──────────                     ──────────
invoke('get_projects')  ───►  #[tauri::command]
                            fn get_projects(state: State<DbState>)
                            -> ApiResponse<Vec<Project>>
                          
invoke('create_project') ─►  #[tauri::command]
  { name, repoUrl, desc }    fn create_project(state, name, repo_url, desc)
                              -> ApiResponse<Project>
```

**特点**：
- 所有 IPC 返回统一的 `ApiResponse<T>` 结构 `{ success, data?, error? }`
- 前端通过 `invoke()` 异步调用，后端通过 `#[tauri::command]` 宏暴露
- 数据库状态通过 Tauri 的 `State` 管理（`Mutex<Connection>`）

### 4.2 数据库设计

**5 张表**（均在 `lib.rs` 的 `init_db()` 中定义）：

| 表名 | 用途 | 关键字段 |
|------|------|---------|
| `projects` | 项目管理 | id, name, repo_url, local_path, status, tech_stack |
| `tasks` | 任务管理 | id, project_id, title, status, priority, task_type, sort_order |
| `task_dependencies` | 任务依赖 | task_id, depends_on_id, dep_type |
| `artifacts` | 产物管理 | id, task_id, name, artifact_type, path, content |
| `conversations` | 对话管理 | id, project_id, title, status |

**当前状态**：使用内存 SQLite（`Connection::open_in_memory()`），数据不持久化。这是 MVP 阶段，后续需改为文件存储。

### 4.3 前端状态管理

```
useAppStore (Zustand)
├── 导航状态
│   ├── currentView: 'dashboard' | 'projects' | 'tasks' | 'settings'
│   ├── selectedProjectId: string | null
│   ├── setView() / selectProject()
├── 项目状态
│   ├── projects: Project[]
│   ├── loadProjects() / createProject()
├── 任务状态
│   ├── tasks: Task[]
│   ├── loadTasks() / createTask() / updateTaskStatus()
└── 统计状态
    ├── stats: { projects, tasks, done, in_progress }
    └── loadStats()
```

### 4.4 前端 UI 结构

```
App
├── Sidebar（侧边栏）
│   ├── Logo (TC)
│   ├── 导航按钮（仪表盘/项目/任务/设置）
│   ├── 最近项目快捷入口
│   └── 底部统计
└── Main Content（主区域）
    ├── DashboardView — 统计卡片 + 快捷操作
    ├── ProjectsView — 项目列表 + 创建
    ├── TasksView — 任务列表 + 状态流转
    └── SettingsView — 应用信息 + OpenClaw 集成
```

---

## 5. TypeScript 配置分析

```json
{
  "target": "ES2020",           // 编译目标
  "module": "ESNext",           // ES 模块
  "moduleResolution": "bundler", // Bundler 模式（Vite 推荐）
  "jsx": "react-jsx",          // React 17+ 自动 JSX 转换
  "strict": true,               // 全量严格模式
  "noUnusedLocals": true,       // 禁止未使用局部变量
  "noUnusedParameters": true,   // 禁止未使用参数
  "noEmit": true                // 只检查，不输出（由 Vite 处理）
}
```

---

## 6. Vite 配置分析

```typescript
// 关键配置
{
  plugins: [react(), tailwindcss()],
  server: {
    port: 1420,              // Tauri 默认端口
    strictPort: true,        // 端口被占用时报错而非自动换端口
    hmr: {                   // HMR 配置（支持移动端调试）
      protocol: "ws",
      host: TAURI_DEV_HOST,
      port: 1421
    },
    watch: {
      ignored: ["**/src-tauri/**"]  // 忽略 Rust 代码变更
    }
  }
}
```

---

## 7. Tauri 配置分析

| 配置项 | 值 | 说明 |
|--------|---|------|
| productName | TeamClaw | 安装包显示名称 |
| identifier | com.teamclaw.desktop | 应用唯一标识 |
| devUrl | `localhost:1420` | 开发时前端地址 |
| frontendDist | ../dist | 构建后前端输出目录 |
| 窗口大小 | 1280×800 | 默认窗口尺寸 |
| 最小窗口 | 900×600 | 最小窗口限制 |
| CSP | null | 内容安全策略未启用（开发阶段） |
| bundle targets | all | 打包所有平台格式 |

### 权限配置（capabilities/default.json）

```json
{
  "permissions": [
    "core:default",      // Tauri 核心权限
    "opener:default"     // 文件/URL 打开权限
  ]
}
```

当前权限较宽松，仅基础功能，后续需按最小权限原则配置。

---

## 8. 依赖版本总结

| 技术栈 | 版本 | 代际 |
|--------|------|------|
| React | 19.1 | 最新稳定版 |
| TypeScript | 5.8 | 最新 |
| Vite | 7.0 | 最新 |
| Tailwind CSS | 4.x | 最新（Rust 引擎重写） |
| Zustand | 5.0 | 最新 |
| Tauri | 2.x | 稳定 |
| Rust Edition | 2021 | 稳定 |
| SQLite | bundled | 随 rusqlite 编译 |
