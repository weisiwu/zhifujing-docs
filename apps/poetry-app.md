# Poetry App（诗词应用）

> 基于 Expo 的跨平台古诗词移动应用，支持 iOS、Android 和 Web。

## 基本信息

| 项目 | 信息 |
|------|------|
| 名称 | poetry-app |
| 框架 | Expo ~54.0 (Expo Router) |
| 语言 | TypeScript + React 19.1 |
| 后端 | Supabase |
| 数据库 | SQLite (本地 poetry.db) |
| 构建 | Expo EAS (Expo Application Services) |
| 状态 | ✅ 运行中 |

## 功能

- **古诗词浏览** — 按朝代、诗人、诗词分类浏览
- **AI 翻译** — 基于 LLM 的古诗词多语言翻译
- **收藏与学习** — 个人收藏夹、学习进度跟踪
- **推送通知** — 每日诗词推送
- **VIP 系统** — 会员订阅功能

## 目录结构

```
poetry-app/
├── app/                  # Expo Router 页面
│   ├── (tabs)/          # 底部 Tab 导航
│   ├── auth/            # 认证相关页面
│   ├── poem/            # 诗词详情页
│   ├── vip/             # VIP 会员页
│   └── _layout.tsx      # 路由布局
├── components/          # UI 组件
├── hooks/               # 自定义 Hooks
│   ├── useAppTheme.ts   # 主题管理
│   └── usePushNotifications.ts  # 推送通知
├── data/                # 本地数据
│   ├── poetry.db        # SQLite 数据库
│   ├── raw/             # 原始数据
│   └── processed/       # 处理后数据
├── lib/                 # Supabase 客户端
├── constants/           # 主题常量
├── android/             # Android 原生代码
└── assets/              # 图片资源
```

## 数据处理流水线

应用包含丰富的 Python 数据处理脚本：

| 脚本 | 用途 |
|------|------|
| `backfill_v2/v3/v4.py` | 数据回填与补全 |
| `translate_*.py` | AI 翻译（多批次并行） |
| `evaluate_poems.py` | 翻译质量评估 |
| `optimize_*.py` | 翻译优化与重试 |
| `fast_top1000*.py` | Top 1000 诗词快速处理 |

## 技术亮点

- **本地优先** — SQLite 本地数据库，离线可用
- **并行处理** — 多 worker 并行翻译，高效处理大规模数据
- **质量评估** — 翻译结果自动评估与回译验证
- **跨平台** — Expo 一套代码覆盖 iOS + Android + Web
