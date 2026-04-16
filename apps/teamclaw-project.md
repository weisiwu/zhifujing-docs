# TeamClaw 项目文档

TeamClaw 是一个桌面客户端多 Agent 协作平台，正在重构中。

## 设计文档

- [系统架构设计 V1.0](./teamclaw/architecture) — 技术选型、系统分层、Agent 角色定义、模块划分
- [对话生命周期 V1.0](./teamclaw/conversation-lifecycle) — 8 阶段、9 种状态、7 种用户干预操作

## 重构背景

放弃原有 ~48,000 行 Web 端代码（Next.js + Express + PostgreSQL），转为：
- **桌面客户端**（Tauri 2.0，Windows + macOS）
- **内嵌 OpenClaw** 作为 Agent 编排引擎
- **微信桥接** — 通过 OpenClaw Bot 实现文字交互

## 模块开发优先级

| 优先级 | 模块 |
|--------|------|
| P0 | 项目导入、多 Agent 编排(DAG)、任务体系 |
| P1 | 微信桥接、知识库(RAG)、对话生命周期 |
| P2 | 用户角色、产物版本、Token 计费 |
| P3 | 埋点报警、客户端更新 |
