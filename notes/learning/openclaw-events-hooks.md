# OpenClaw 事件体系与钩子体系深度解析

## 概述

拆解 OpenClaw 四层事件面，理解不同层级的职责边界。

## 四层事件架构

```
Layer 1: Runtime Stream    →  Agent 运行时的实时数据流
Layer 2: Internal Hooks    →  OpenClaw 内部生命周期钩子
Layer 3: Plugin Hooks      →  插件系统的扩展钩子
Layer 4: Webhook           →  外部系统的 HTTP 回调
```

### 关键事件类型

| 事件 | 触发时机 | 用途 |
|------|----------|------|
| `agent_end` | Agent 完成一次执行 | 结果处理、通知 |
| `session_end` | 会话结束 | 资源清理、日志 |
| `ACP completion` | ACP 外部 Agent 完成 | 结果回收、状态同步 |

## 设计精髓

> 区分 `agent_end`、`session_end`、ACP completion 的语义边界是理解 OpenClaw 事件体系的关键——它们看似相似，但触发的上下文和语义完全不同。

## 实践建议

1. 不要在 Internal Hooks 中做重 IO 操作
2. Plugin Hooks 适合做轻量扩展
3. 需要调用外部系统时，走 Webhook
4. Runtime Stream 用于实时监控和调试
