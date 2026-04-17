---
title: TeamClaw 技术方案设计合集
---

# 技术方案设计合集

> TeamClaw 项目在开发过程中形成的技术方案设计文档，覆盖版本管理、分支管理、变更追踪等核心功能。

---

## 1. 产物下载功能

### 需求背景
针对版本产物的下载功能增强，支持多格式下载和下载历史记录。

### 技术选型

| 选型 | 方案 | 理由 |
|------|------|------|
| 状态管理 | React Query + localStorage | 下载历史本地存储，无需后端 |
| 产物存储 | Version.artifactUrl 扩展为数组 | 一个版本可有多个产物文件 |
| 下载追踪 | localStorage | 轻量级方案 |

### 核心数据结构

```typescript
// 产物格式
type ArtifactFormat = 'zip' | 'apk' | 'exe' | 'dmg' | 'pkg' | 'ipa';

// 产物信息
interface Artifact {
  id: string;
  format: ArtifactFormat;
  url: string;
  fileName: string;
  fileSize: number;
  createdAt: string;
}

// 下载历史记录（本地存储）
interface DownloadRecord {
  id: string;
  versionId: string;
  artifactId: string;
  downloadedAt: string;
}
```

---

## 2. 辅助能力模块（iter-25）

### 需求背景
智能搜索增强、文档在线预览、批量下载管理三个辅助能力。

### 技术选型

| 技术决策 | 选择 | 理由 |
|---------|------|------|
| PDF 预览 | pdf-lib + 自建渲染 | 不依赖外部服务 |
| 批量下载队列 | Node.js Stream + archiver | 流式处理，内存友好 |
| 下载进度 | SSE (Server-Sent Events) | 单向实时推送，比 WebSocket 轻量 |
| 搜索历史 | SQLite + 内存缓存 | 重启不丢失 |

### 已有基础设施

| 模块 | 当前能力 |
|------|---------|
| 文档服务 | CRUD、版本快照、收藏 |
| 搜索增强 | ChromaDB 向量搜索 |
| 产物存储 | 存储、列表、下载 |

---

## 3. 版本回退功能（iter-75）

### 技术选型

| 技术决策 | 选择 | 理由 |
|---------|------|------|
| 回退方式 | `git reset --hard` | 直接重置到指定 commit |
| 数据持久化 | SQLite versions 表扩展 | 与现有架构一致 |
| 安全防护 | 确认对话框 + 非 HEAD 检查 | 防止误操作 |
| 并发控制 | 版本状态锁 | 防止并发冲突 |

### 数据模型

```sql
-- versions 表新增字段
ALTER TABLE versions ADD COLUMN rollback_count INTEGER DEFAULT 0;
ALTER TABLE versions ADD COLUMN last_rollback_at TEXT;
-- status 扩展: draft/published/archived/rolled_back
```

---

## 4. 分支管理功能（iter-76）

### 需求背景
将纯内存存储的分支数据与 Git 实际分支同步。

### 技术选型

| 技术决策 | 选择 | 理由 |
|---------|------|------|
| Git 操作 | gitService.ts 扩展 | 复用已有封装 |
| 数据存储 | SQLite + Git 双写 | DB 存元数据，Git 存实际分支 |
| 默认分支 | projects 表 defaultBranch 字段 | 项目级配置 |
| 同步策略 | 启动时同步 + 操作时双写 | 确保 DB 和 Git 一致 |

### 数据模型

```sql
ALTER TABLE projects ADD COLUMN default_branch TEXT DEFAULT 'main';

CREATE TABLE IF NOT EXISTS branches (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  is_main INTEGER DEFAULT 0,
  is_remote INTEGER DEFAULT 0,
  is_protected INTEGER DEFAULT 0,
  project_id TEXT REFERENCES projects(id),
  base_branch TEXT,
  description TEXT
);
```

---

## 5. 变更追踪（iter-87）

### 需求背景
为版本建立完整变更档案：关联飞书消息截图、存储 AI 生成的变更摘要。

### 事件类型

| 事件 | 截图需求 | 摘要需求 |
|------|---------|---------|
| version_created | 可选 | 自动 |
| version_published | 必须 | 自动 |
| version_rollback | 可选 | 必须 |
| screenshot_linked | 必须 | - |
| changelog_generated | - | 必须 |

### 架构

```
事件触发器 → 变更记录器 → 时间线存储
     ↓             ↓            ↓
消息截图服务   摘要生成服务   前端时间线
```

### 已有基础设施

| 模块 | 状态 |
|------|------|
| 截图模型（内存） | ✅ |
| 截图 API (CRUD) | ✅ |
| Changelog 生成器 | ✅ |
| 前端组件 | ✅ |

---

## 6. Tag 信息展示（iter-72）

### 需求背景
在版本面板展示所有 Tag 的详细信息，包括 commit 信息和来源标识。

### 技术选型

| 决策 | 选择 | 理由 |
|------|------|------|
| 数据来源 | Git + DB 合并 | Tag 基础信息存 DB，commit 信息实时获取 |
| source 字段 | SQLite tags 表 | 简单可靠 |
| 展开详情 | Collapsible Table Row | 在现有列表页直接扩展 |

### 数据模型

```sql
ALTER TABLE tags ADD COLUMN source TEXT DEFAULT 'manual';
-- 取值: 'auto' | 'manual'
CREATE INDEX IF NOT EXISTS idx_tags_source ON tags(source);
```

---

## 7. 迭代 69 PRD — 变更追踪（版本关联消息截图 + 变更摘要）

### 任务拆解（Sprint 69）

| 任务 | 描述 | 依赖 | 状态 |
|------|------|------|------|
| TASK-6901 | 后端：截图关联 API | 无 | 待开始 |
| TASK-6902 | 后端：变更摘要 API | 无 | 待开始 |
| TASK-6903 | 后端：版本时间线 API | 6901, 6902 | 待开始 |
| TASK-6904 | 前端：MessageSelector 组件 | 后端 API | 待开始 |
| TASK-6905 | 前端：ScreenshotGallery 组件 | 6901 | 待开始 |
| TASK-6906 | 前端：ChangelogPanel 组件 | 6902 | 待开始 |
| TASK-6907 | 前端：VersionTimeline 组件 | 6903 | 待开始 |
| TASK-6908 | 前端：版本详情 Dialog 集成 | 6904-6907 | 待开始 |
| TASK-6909 | 数据模型：数据库表设计 | 无 | 待开始 |

### 验收标准要点
- 消息选择器支持搜索和翻页
- 截图画廊缩略图网格（3-4列）+ 点击放大
- AI 生成分类摘要（features/changes/fixes/breaking）
- Markdown 编辑 + 保存
- 时间线按时间倒序
