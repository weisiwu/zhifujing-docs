# 学习笔记

技术调研与学习笔记，聚焦 AI Agent 架构、RAG 知识库系统、LLM 工程和 DevOps 实践。

## 个人学习（13 篇）

> 深度技术调研文章，涵盖 Agent 协议、知识库系统、LLM 架构等前沿话题。

### AI Agent 与 LLM

| 文章 | 关键词 | 摘要 |
|------|--------|------|
| [ACP 协议解析](./learning/acp) | Agent Client Protocol, OpenClaw | ACP 协议的定义、设计理念，以及在 OpenClaw 中的两种用法 |
| [OpenClaw CLI 强化 Agent](./learning/openclaw-cli) | CLI, 能力接入, 自我进化 | 如何用 OpenClaw CLI 为 Agent 增加工具调用和扩展能力 |
| [OpenClaw Subagent 体系](./learning/openclaw-subagent) | Subagent, 并发, 多任务 | OpenClaw 的子代理架构和并发任务调度机制 |
| [OpenClaw 事件与钩子](./learning/openclaw-events-hooks) | Events, Hooks, 生命周期 | OpenClaw 的事件驱动架构和钩子扩展点 |
| [OpenClaw 能力地图](./learning/openclaw-tools) | Tools, 扩展机制 | OpenClaw 支持的工具类型和扩展机制全景 |
| [Claude Code 源码架构](./learning/claude-code-arch) | Claude Code, 架构设计 | Claude Code 源码中最值得学习的 3 个设计模式 |
| [Token 中转站解析](./learning/token-gateway) | Token, 中转, API | Token 中转站的运作原理、为什么会火、风险分析 |

### 知识库与 RAG

| 文章 | 关键词 | 摘要 |
|------|--------|------|
| [Dify 知识库构建](./learning/dify-knowledge-base) | Dify, RAG, 知识库 | Dify 平台的知识库构建完整指南 |
| [MaxKB 知识库构建](./learning/maxkb-knowledge-base) | MaxKB, 开源知识库 | MaxKB 开源知识库系统的构建与使用 |
| [RAGFlow 知识库构建](./learning/ragflow-knowledge-base) | RAGFlow, 文档解析 | RAGFlow 的深度文档解析和知识库构建方案 |
| [RAPTOR 递归摘要检索](./learning/raptor) | RAPTOR, 递归摘要, 检索 | RAPTOR 递归摘要树的原理与检索优化 |
| [Markdown 知识库方案](./learning/markdown-knowledge-base) | Markdown, 个人知识库 | 基于 Markdown 的个人知识库方案设计 |

### 产品与设计

| 文章 | 关键词 | 摘要 |
|------|--------|------|
| [AI 生成 APP 设计稿](./learning/ai-app-design) | AI UI, 设计稿, 最佳实践 | 使用 AI 生成 APP 设计稿的最佳实践和经验总结 |

## 实战笔记（3 篇）

> 来自 OpenClaw 实战开发的踩坑记录和经验总结。

| 文章 | 关键词 | 摘要 |
|------|--------|------|
| [GitHub Actions 迭代调度](./practice/actions-loop) | GitHub Actions, 轮询, 循环 | 从轮询到循环的 GitHub Actions 自动迭代调度架构改造 |
| [Agent 超时无响应排查](./practice/agent-timeout) | Agent, 超时, Cron 调度 | OpenClaw Agent 超时无响应的排查实录与 Cron 调度机制解析 |
| [Issue 残留与幂等性设计](./practice/issue-idempotent) | Issue, 幂等性, 自动迭代 | 自动迭代 Issue 残留问题分析与幂等性设计方案 |
