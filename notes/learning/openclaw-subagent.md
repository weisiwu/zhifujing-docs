# OpenClaw Subagent 体系与并发任务能力深度调研

## 概述

OpenClaw 的并发不是无限并行，而是基于受控并发模型的架构设计。

## 并发控制架构

```
sessions_spawn  →  ACP Harness  →  sessions_send
     ↓                ↓                ↓
  创建子会话      管理生命周期      跨会话通信
```

### 核心组件

| 组件 | 职责 |
|------|------|
| Session | 单个 Agent 的会话上下文 |
| Queue Lane | 任务队列，控制并发度 |
| Task Ledger | 任务账本，记录状态转移 |
| Flow State | 流程状态机，协调多 Agent |

## 关键洞察

> OpenClaw 的并发模型是「受控并发」——通过 Session、Queue Lane、Task Ledger、Flow State 四层机制，确保多 Agent 协作的可靠性和可观测性。

## 设计启示

1. 并发不等于并行——先定义并发模型，再谈实现
2. 每一层都有自己的职责边界，不要跨层操作
3. Task Ledger 是分布式系统的关键——让状态转移可审计
