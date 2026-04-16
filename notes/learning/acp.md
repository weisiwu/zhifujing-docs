# ACP 是什么：从协议定义到 OpenClaw 中的两种用法

## 概述

解析 **Agent Client Protocol (ACP)** 的本质——标准化编辑器/IDE 与智能体通信的协议。

## 核心要点

### ACP 协议定义
- ACP 是一种标准化的通信协议，用于编辑器/IDE 与 AI 智能体之间的交互
- 解决了不同 IDE 与不同 Agent 之间的适配问题
- 类似于 LSP（Language Server Protocol）对代码补全的标准化

### OpenClaw 中的双重角色
1. **作为 ACP Bridge** — 被 IDE 连接，OpenClaw 本身充当 ACP Server
2. **通过 `/acp spawn` 调起外部执行器** — 调用 Codex、Claude Code、Gemini CLI 等外部 Agent

### 实际应用场景
- 在 VSCode/Cursor 中通过 ACP 协议与 OpenClaw 交互
- 通过 ACP Harness 管理多个外部 Agent 的生命周期
- 实现 Agent 间的标准化通信与任务委派

## 关键收获

> ACP 不是简单的 API 调用，而是建立了一套 Agent 生态的互操作标准，让不同厂商的 Agent 可以在同一框架下协作。
