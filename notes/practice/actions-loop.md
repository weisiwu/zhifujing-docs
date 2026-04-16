# GitHub Actions 自动迭代调度：从轮询到循环的架构改造

## 概述

将 Cron 轮询模式改造为 while 循环模式，调度效率提升 **2.5 倍**。

## 性能对比

| 指标 | Cron 轮询 | while 循环 | 提升 |
|------|-----------|------------|------|
| 50 轮总耗时 | 15.5 小时 | 6.3 小时 | **2.5x** |
| 每轮空转等待 | ~12 分钟 | 0 分钟 | - |
| 调度精度 | ±30 分钟 | 即时 | - |

## 问题分析

### Cron 轮询的「盲调度」
```
每 30 分钟触发一次 → 检查是否有任务 → 无任务则空转
        ↓
每轮多等 12 分钟 × 50 轮 = 10 小时空转
```

### while 循环的「即时调度」
```
while (有任务) {
  执行任务 → 检查下一轮 → 立即执行
}
```

## 改造方案

```yaml
# 改造后的 workflow
jobs:
  iterate:
    runs-on: ubuntu-latest
    steps:
      - name: Loop iteration
        env:
          MAX_ITERATIONS: 100
          TIMEOUT_MINUTES: 360
        run: |
          count=0
          while [ $count -lt $MAX_ITERATIONS ]; do
            # 执行迭代逻辑
            result=$(./iterate.sh)
            if [ "$result" = "DONE" ]; then
              break
            fi
            count=$((count + 1))
          done
```

## 关键设计

1. **while 循环** — 替代 Cron 轮询，任务完成后立即进入下一轮
2. **workflow_dispatch** — 支持手动触发和外部触发
3. **timeout 防挂死** — 设置最大运行时间
4. **环境清理** — 每轮结束清理状态，防止状态泄露

## 教训

> Cron 是「定时触发」的设计，不适合「持续迭代」的场景。选择正确的调度原语，比优化调度频率更重要。
