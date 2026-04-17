# TeamClaw（协作平台）

> 基于 Tauri 2.x 的桌面协作平台，目标是构建 AI Agent 驱动的团队协作工具。

## 基本信息

| 项目 | 信息 |
|------|------|
| 名称 | teamclaw |
| 框架 | Tauri 2.x + Vite + React 19 |
| 后端 | Rust (Tauri) |
| 前端 | React 19 + TypeScript |
| 桌面端 | Tauri (跨平台) |
| 状态管理 | Zustand |
| GitHub | [weisiwu/teamclaw](https://github.com/weisiwu/teamclaw) |
| 状态 | 🔨 开发中（骨架已完成） |

## 架构概览

```
teamclaw/
├── src/                  # React 前端 (Vite)
│   ├── App.tsx           # 主应用入口
│   ├── store.ts          # Zustand 状态管理
│   └── assets/           # 静态资源
├── src-tauri/            # Tauri Rust 后端
│   ├── src/              # Rust 源码
│   ├── Cargo.toml        # Rust 依赖
│   ├── capabilities/     # Tauri 权限配置
│   └── icons/            # 应用图标
├── project/              # 项目设计文档
│   ├── prd-module*.md    # 6 个模块 PRD
│   ├── teamclaw-architecture.md  # 架构设计
│   └── teamclaw-conversation-lifecycle.md  # 对话生命周期
└── _legacy-nextjs/       # 旧版 Next.js 全栈代码（参考）
```

## 功能模块（PRD 已完成）

| 模块 | 名称 | 说明 |
|------|------|------|
| 模块 1 | 项目导入 | 导入和管理 GitHub 项目 |
| 模块 2 | Agent 编排 | AI Agent 任务调度与编排 |
| 模块 3 | 任务系统 | 任务创建、分配、跟踪 |
| 模块 4 | 能力系统 | Agent 能力注册与扩展 |
| 模块 5 | 知识库 | 文档与知识管理 |
| 模块 6 | 对话生命周期 | 多轮对话管理 |

## 技术选型

- **桌面框架**: Tauri 2.x（轻量、安全、跨平台）
- **前端**: React 19 + TypeScript + Vite
- **状态管理**: Zustand
- **旧版参考**: `_legacy-nextjs/` 中保留了完整的 Next.js 全栈实现，含 Express 后端、PostgreSQL、Docker 部署等

## 相关文档

- [系统架构设计](./teamclaw/architecture)
- [对话生命周期](./teamclaw/conversation-lifecycle)
- [Agent 编排 PRD](./teamclaw/prd-module2-agent-orchestration)
