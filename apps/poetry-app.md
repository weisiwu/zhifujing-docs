# poetry-app（诗词应用）

> 基于 Expo 的跨平台诗词学习应用，支持 iOS、Android 和 Web 三端。

## 技术栈

| 类别 | 技术 |
|------|------|
| 框架 | Expo **54** (React Native 0.81) |
| 语言 | TypeScript + React **19.1** |
| 路由 | Expo Router **6**（文件路由） |
| 导航 | React Navigation 7 + Bottom Tabs |
| UI 库 | React Native Paper（Material Design） |
| 状态管理 | Zustand **5** |
| 后端 | Supabase **2.98** |
| 本地存储 | better-sqlite3 |
| 通知 | expo-notifications |
| 手势动画 | react-native-reanimated + gesture-handler |

## 核心功能

### 📱 跨平台支持
- iOS / Android / Web 三端统一代码
- Expo Router 文件路由系统
- 原生性能体验

### 📖 诗词数据库
- Supabase 云端数据库
- 本地 SQLite 离线缓存
- 中英双语翻译（AI 辅助）

### 🔄 数据处理管线
项目包含大量数据处理脚本，覆盖：
- **翻译**: `translate_*.py`, `retranslate_*.py` — AI 辅助诗词翻译
- **质量评估**: `quality_*.py`, `eval_*.py`, `quality_score.py` — 翻译质量评分
- **数据回填**: `backfill_*.py` — 增量数据补充
- **修复脚本**: `fix_*.py`, `emergency_fix_*.py` — 数据修正

### 🔔 推送通知
- expo-notifications 集成
- 触觉反馈（expo-haptics）

## 项目结构

```
poetry-app/
├── app/              # Expo Router 页面
├── components/       # React Native 组件
├── constants/        # 常量定义
├── hooks/            # 自定义 Hooks
├── lib/              # 工具库
├── supabase/         # Supabase 配置与迁移
├── scripts/          # 构建脚本
├── docs/             # 项目文档
└── *.py              # 数据处理脚本
```

## 开发命令

```bash
# 安装依赖
npm install

# 启动 Expo 开发服务器
npx expo start

# 运行 Web 版
npx expo start --web

# 构建
npx expo build
```
