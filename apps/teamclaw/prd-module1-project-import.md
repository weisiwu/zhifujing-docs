---
title: PRD — 模块1：项目导入
---

     1|# PRD — 模块1：项目导入
     2|
     3|> 版本：V1.0  
     4|> 最后更新：2026-04-16  
     5|> 优先级：P0（MVP 核心）
     6|
     7|---
     8|
     9|## 1. 功能概述
    10|
    11|项目导入是 TeamClaw 的入口模块。用户通过创建/导入项目，建立 Agent 协作的工作空间。支持从零创建新项目，或导入已有 Git 仓库，配置 Agent 团队后即可开始多 Agent 协作。
    12|
    13|---
    14|
    15|## 2. 用户故事
    16|
    17|| 编号 | 用户故事 | 优先级 |
    18||------|---------|--------|
    19|| US-01 | 作为用户，我想创建一个新项目并设置基本信息 | P0 |
    20|| US-02 | 作为用户，我想导入本地已有代码仓库 | P0 |
    21|| US-03 | 作为用户，我想通过 Git URL 克隆远程仓库 | P0 |
    22|| US-04 | 作为用户，我想为项目配置 Agent 团队（启用/禁用角色） | P0 |
    23|| US-05 | 作为用户，我想在项目列表中浏览、搜索、筛选项目 | P0 |
    24|| US-06 | 作为用户，我想查看项目详情（概览、对话、任务、知识库） | P0 |
    25|| US-07 | 作为用户，我想删除或归档不再使用的项目 | P1 |
    26|| US-08 | 作为用户，我想为项目设置标签以便分类管理 | P1 |
    27|| US-09 | 作为用户，我想在项目间快速切换 | P1 |
    28|| US-10 | 作为用户，我想编辑项目基本信息 | P2 |
    29|
    30|---
    31|
    32|## 3. 功能需求清单
    33|
    34|### 3.1 创建新项目 [P0]
    35|
    36|**输入**：
    37|- 项目名称（必填，2-50字符）
    38|- 项目描述（选填，最多500字符）
    39|- 标签（选填，最多5个）
    40|- 项目路径（本地存储目录，默认 `~/TeamClaw/projects/{name}`）
    41|
    42|**流程**：
    43|1. 用户点击「新建项目」
    44|2. 填写项目信息表单
    45|3. 系统创建项目目录结构
    46|4. 初始化 SQLite 数据库记录
    47|5. 进入项目配置页面
    48|
    49|**输出**：项目创建成功，进入项目详情页
    50|
    51|### 3.2 导入已有仓库 [P0]
    52|
    53|**方式一：本地路径**
    54|1. 用户选择「导入项目」→「本地目录」
    55|2. 选择本地代码目录（Tauri 文件选择器）
    56|3. 系统扫描目录，识别技术栈（package.json、pom.xml、Cargo.toml 等）
    57|4. 展示识别结果，用户确认
    58|5. 创建项目记录，关联本地路径
    59|
    60|**方式二：Git 克隆**
    61|1. 用户选择「导入项目」→「Git 仓库」
    62|2. 输入 Git URL（支持 HTTPS/SSH）
    63|3. 选择本地克隆目录
    64|4. 系统执行 `git clone`，展示进度
    65|5. 克隆完成后，扫描识别技术栈
    66|6. 创建项目记录
    67|
    68|**技术栈自动识别规则**：
    69|
    70|| 文件 | 识别为 |
    71||------|--------|
    72|| `package.json` | Node.js / 前端项目 |
    73|| `next.config.*` | Next.js |
    74|| `Cargo.toml` | Rust |
    75|| `pyproject.toml` / `requirements.txt` | Python |
    76|| `go.mod` | Go |
    77|| `pom.xml` / `build.gradle` | Java |
    78|| `*.sln` / `*.csproj` | C# / .NET |
    79|
    80|### 3.3 Agent 团队配置 [P0]
    81|
    82|**流程**：
    83|1. 项目创建后进入「配置 Agent」步骤
    84|2. 展示 8 个 Agent 角色卡片：Main、PM、Designer、Architect、CoderA、CoderB、DBA、DevOps
    85|3. 用户勾选需要的 Agent（Main Agent 始终启用，不可取消）
    86|4. 配置 OpenClaw 连接：
    87|   - 连接方式：本地内嵌 / 远程 API
    88|   - API Key（如远程）
    89|   - 模型选择（如可选）
    90|5. 确认配置
    91|
    92|**默认配置**：
    93|- 首次使用推荐启用：Main + PM + Architect + CoderA + CoderB（5 个）
    94|- 提供预设模板：「全栈开发」「前端项目」「后端服务」
    95|
    96|### 3.4 项目列表 [P0]
    97|
    98|**视图**：
    99|- 卡片视图（默认）：项目名、描述、标签、状态、最近活动时间
   100|- 列表视图：紧凑展示
   101|
   102|**操作**：
   103|- 搜索：按项目名/描述搜索
   104|- 筛选：按标签、状态（活跃/归档）、技术栈
   105|- 排序：最近更新、创建时间、名称
   106|
   107|### 3.5 项目详情页 [P0]
   108|
   109|**Tab 结构**：
   110|
   111|| Tab | 内容 |
   112||-----|------|
   113|| 概览 | 项目信息、Agent 配置、技术栈、统计（对话数/任务数/代码量） |
   114|| 对话 | 对话列表，支持新建对话、查看归档 |
   115|| 任务 | 任务看板（待办/进行中/审核中/已完成） |
   116|| 知识库 | 项目文档、RAG 索引管理（P1 功能） |
   117|| 设置 | 项目信息编辑、Agent 配置修改、删除项目 |
   118|
   119|---
   120|
   121|## 4. 数据模型
   122|
   123|```sql
   124|-- 项目表
   125|CREATE TABLE projects (
   126|  id            TEXT PRIMARY KEY,          -- UUID
   127|  name          TEXT NOT NULL,             -- 项目名称
   128|  description   TEXT DEFAULT '',           -- 项目描述
   129|  path          TEXT NOT NULL,             -- 本地路径
   130|  git_url       TEXT,                      -- Git 远程地址（可选）
   131|  tech_stack    TEXT DEFAULT '[]',         -- 技术栈 JSON 数组
   132|  tags          TEXT DEFAULT '[]',         -- 标签 JSON 数组
   133|  status        TEXT DEFAULT 'active',     -- active | archived
   134|  agent_config  TEXT DEFAULT '{}',         -- Agent 配置 JSON
   135|  openclaw_config TEXT DEFAULT '{}',       -- OpenClaw 连接配置 JSON
   136|  created_at    INTEGER NOT NULL,          -- Unix timestamp
   137|  updated_at    INTEGER NOT NULL           -- Unix timestamp
   138|);
   139|
   140|-- 项目统计缓存
   141|CREATE TABLE project_stats (
   142|  project_id    TEXT PRIMARY KEY REFERENCES projects(id),
   143|  conversation_count INTEGER DEFAULT 0,
   144|  task_count         INTEGER DEFAULT 0,
   145|  agent_run_count    INTEGER DEFAULT 0,
   146|  code_lines         INTEGER DEFAULT 0,
   147|  updated_at    INTEGER NOT NULL
   148|);
   149|```
   150|
   151|---
   152|
   153|## 5. Tauri Commands 接口
   154|
   155|```typescript
   156|// 项目 CRUD
   157|create_project(payload: CreateProjectInput): Promise<Project>
   158|get_project(id: string): Promise<Project>
   159|list_projects(filter?: ProjectFilter): Promise<Project[]>
   160|update_project(id: string, payload: UpdateProjectInput): Promise<Project>
   161|delete_project(id: string): Promise<void>
   162|archive_project(id: string): Promise<void>
   163|
   164|// 仓库导入
   165|import_local_project(path: string): Promise<Project>
   166|import_git_project(url: string, targetPath: string): Promise<ImportProgress>
   167|
   168|// 技术栈识别
   169|detect_tech_stack(path: string): Promise<TechStackResult>
   170|
   171|// Agent 配置
   172|update_agent_config(projectId: string, config: AgentConfig): Promise<void>
   173|get_agent_config(projectId: string): Promise<AgentConfig>
   174|
   175|// 项目统计
   176|get_project_stats(projectId: string): Promise<ProjectStats>
   177|```
   178|
   179|---
   180|
   181|## 6. UI 交互流程
   182|
   183|### 6.1 新建项目
   184|
   185|```
   186|[项目列表页]
   187|    │
   188|    ├─ 点击「新建项目」
   189|    │
   190|    ▼
   191|[新建项目弹窗/页面]
   192|    ├─ 填写：名称、描述、标签
   193|    ├─ 选择存储路径（默认值可改）
   194|    │
   195|    ▼
   196|[Agent 配置步骤]
   197|    ├─ 选择 Agent 角色（8 选 N，Main 必选）
   198|    ├─ 选择预设模板 或 自定义
   199|    ├─ 配置 OpenClaw 连接
   200|    │
   201|    ▼
   202|[项目详情页] ← 创建完成
   203|```
   204|
   205|### 6.2 导入仓库
   206|
   207|```
   208|[项目列表页]
   209|    │
   210|    ├─ 点击「导入项目」
   211|    │
   212|    ▼
   213|[选择导入方式]
   214|    ├─ 本地目录
   215|    │   ├─ 打开文件选择器
   216|    │   ├─ 选择目录
   217|    │   ├─ 自动识别技术栈
   218|    │   └─ 确认导入
   219|    │
   220|    └─ Git 仓库
   221|        ├─ 输入 Git URL
   222|        ├─ 选择克隆目录
   223|        ├─ 进度条展示克隆进度
   224|        ├─ 自动识别技术栈
   225|        └─ 确认导入
   226|```
   227|
   228|---
   229|
   230|## 7. 边界条件与异常处理
   231|
   232|| 场景 | 处理方式 |
   233||------|---------|
   234|| 项目名重复 | 提示名称已存在，建议后缀编号 |
   235|| 本地路径不存在 | 自动创建（需确认） |
   236|| 本地路径已有文件 | 警告用户，提供合并/覆盖/取消选项 |
   237|| Git URL 无效 | 提示 URL 格式错误 |
   238|| Git 克隆失败（网络） | 提示网络错误，支持重试 |
   239|| Git 克隆失败（权限） | 提示认证信息，支持输入凭据 |
   240|| 目录无写权限 | 提示权限不足，建议更换路径 |
   241|| 磁盘空间不足 | 检测并提前警告 |
   242|| 技术栈识别失败 | 标记为「未知」，允许用户手动选择 |
   243|
   244|---
   245|
   246|## 8. 验收标准
   247|
   248|### P0 验收（MVP）
   249|- [ ] 能创建新项目，信息完整保存到 SQLite
   250|- [ ] 能通过本地路径导入已有代码目录
   251|- [ ] 能通过 Git URL 克隆远程仓库
   252|- [ ] 技术栈自动识别至少支持 5 种（Node/Next/Rust/Python/Go）
   253|- [ ] Agent 配置可保存和修改，Main Agent 不可取消
   254|- [ ] 项目列表支持卡片展示、搜索、筛选
   255|- [ ] 项目详情页展示概览信息
   256|- [ ] 项目删除需二次确认
   257|- [ ] 所有异常场景有友好提示
   258|
   259|### P1 验收
   260|- [ ] 项目标签管理
   261|- [ ] 项目归档功能
   262|- [ ] 项目间快速切换
   263|- [ ] 项目统计信息展示
   264|
   265|---
   266|
   267|*文档维护者：TeamClaw 项目组*
   268|