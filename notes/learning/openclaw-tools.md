# OpenClaw 能力地图：它支持哪些 Tools 与扩展机制？

## 概述

拆解 OpenClaw 的五层能力架构，理解每层职责才能正确扩展。

## 五层能力架构

```
Layer 1: Built-in Tools    →  内置工具（文件操作、终端等）
Layer 2: Skills            →  技能模块（可复用的知识/流程包）
Layer 3: Hooks             →  生命周期钩子（事件驱动扩展）
Layer 4: Plugins           →  插件系统（独立功能模块）
Layer 5: MCP               →  Model Context Protocol（外部工具桥接）
```

## 每层职责

| 层级 | 职责 | 扩展方式 |
|------|------|----------|
| Built-in Tools | 基础能力 | 不可扩展（由平台提供） |
| Skills | 知识 + 流程 | 编写 SKILL.md |
| Hooks | 事件响应 | 配置钩子函数 |
| Plugins | 独立功能 | 开发插件包 |
| MCP | 外部集成 | 配置 MCP Server |

## 核心观点

> 不是所有需求都该塞进「插件」——理解每层职责，选择正确的扩展层级，才能写出可维护的 Agent 扩展。
