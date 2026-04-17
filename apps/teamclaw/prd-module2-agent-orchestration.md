---
title: PRD — 模块2：多 Agent 编排
---

     1|# PRD — 模块2：多 Agent 编排
     2|
     3|> 版本：V1.0  
     4|> 最后更新：2026-04-16  
     5|> 优先级：P0（MVP 核心）
     6|
     7|---
     8|
     9|## 1. 功能概述
    10|
    11|多 Agent 编排是 TeamClaw 的核心引擎。Main Agent 将用户需求拆解为任务 DAG，调度多个专业 Agent 并行/串行执行，在关键节点汇总问题统一提问用户，支持 7 种用户干预操作。内嵌 OpenClaw 实现 Agent 运行时，不重复造轮子。
    12|
    13|---
    14|
    15|## 2. 用户故事
    16|
    17|| 编号 | 用户故事 | 优先级 |
    18||------|---------|--------|
    19|| US-01 | 作为用户，我想看到 Main Agent 自动将需求拆分为任务 DAG | P0 |
    20|| US-02 | 作为用户，我想查看 Agent 实时执行进度和日志 | P0 |
    21|| US-03 | 作为用户，我想在 Agent 执行过程中暂停所有任务 | P0 |
    22|| US-04 | 作为用户，我想修改正在执行任务的参数或方向 | P0 |
    23|| US-05 | 作为用户，我想跳过当前任务，继续后续任务 | P0 |
    24|| US-06 | 作为用户，我想回滚到上一个检查点 | P0 |
    25|| US-07 | 作为用户，我想中途终止整个对话 | P0 |
    26|| US-08 | 作为用户，我想在 DAG 中插入新任务 | P0 |
    27|| US-09 | 作为用户，我想向执行中的 Agent 发送补充指令 | P0 |
    28|| US-10 | 作为用户，我想让多个 Agent 的问题被统一汇总提问，避免被轰炸 | P0 |
    29|| US-11 | 作为用户，我想查看任务依赖关系图 | P1 |
    30|| US-12 | 作为用户，我想调整任务优先级 | P1 |
    31|| US-13 | 作为用户，我想手动触发某个任务的重新执行 | P1 |
    32|| US-14 | 作为用户，我想为任务设置超时时间 | P2 |
    33|
    34|---
    35|
    36|## 3. 功能需求清单
    37|
    38|### 3.1 任务 DAG 生成 [P0]
    39|
    40|**触发**：用户确认 PRD 后（阶段 ② → ③）
    41|
    42|**流程**：
    43|1. Architect Agent 分析 PRD，输出技术方案草案
    44|2. Main Agent 将方案拆解为可执行任务
    45|3. 为每个任务分配 Agent 角色
    46|4. 建立任务间依赖关系（DAG）
    47|5. 预估每个任务的执行时间
    48|6. 展示 DAG 给用户确认
    49|
    50|**任务定义结构**：
    51|```typescript
    52|interface Task {
    53|  id: string;                    // UUID
    54|  title: string;                 // 任务标题
    55|  description: string;           // 详细描述
    56|  agent_role: AgentRole;         // 分配的 Agent
    57|  status: TaskStatus;           // pending | assigned | in_progress | blocked | done | failed
    58|  depends_on: string[];          // 依赖的任务 ID 列表
    59|  estimated_time: number;        // 预估时间（分钟）
    60|  timeout: number;               // 超时时间（分钟）
    61|  artifacts: Artifact[];         // 产物列表
    62|  created_at: number;            // 创建时间戳
    63|  started_at?: number;           // 开始时间戳
    64|  completed_at?: number;         // 完成时间戳
    65|}
    66|
    67|type AgentRole = 'main' | 'pm' | 'designer' | 'architect' | 'coderA' | 'coderB' | 'dba' | 'devops';
    68|```
    69|
    70|**DAG 可视化**：
    71|- 使用 Mermaid.js 或类似库展示 DAG
    72|- 不同 Agent 角色用不同颜色标记
    73|- 当前执行中任务高亮
    74|- 已完成任务用灰色标记
    75|- 失败任务用红色标记
    76|
    77|### 3.2 Agent 调度引擎 [P0]
    78|
    79|**调度策略**：
    80|1. **拓扑排序**：按照依赖关系确定执行顺序
    81|2. **并行执行**：无依赖关系的任务同时启动
    82|3. **资源管理**：控制同时运行的最大 Agent 数量（默认 4 个）
    83|4. **超时处理**：任务超时后标记失败，进入异常处理流程
    84|
    85|**调度流程**：
    86|```
    87|1. 初始化：所有无依赖任务标记为「ready」
    88|2. 循环调度：
    89|   a. 从「ready」队列取任务，分配给对应 Agent
    90|   b. 监听 Agent 进度更新
    91|   c. 任务完成后，检查其依赖任务是否全部完成
    92|   d. 如果依赖满足，将后置任务加入「ready」队列
    93|3. 所有任务完成 → 进入阶段 ⑤（中间审核）
    94|```
    95|
    96|**Agent 实例管理**：
    97|- 每个 Agent 角色对应一个 OpenClaw Agent 实例
    98|- 实例生命周期：分配 → 启动 → 运行 → 完成/失败 → 销毁
    99|- 支持同一角色多个实例并行（如 CoderA 和 CoderB 可同时运行）
   100|
   101|### 3.3 并发提问汇总 [P0]
   102|
   103|**问题收集**：
   104|- 各 Agent 遇到问题时，将问题发送给 Main Agent
   105|- Main Agent 维护一个待提问队列
   106|
   107|**汇总规则**：
   108|- 每累积 3 个问题或每隔 30 秒（取先到），统一向用户提问
   109|- 相关问题归类：技术选型、功能确认、边界条件等
   110|- 避免重复问题：相似问题合并提问
   111|
   112|**提问格式（桌面端）**：
   113|```
   114|📋 Agent 汇总提问 (3 个)
   115|
   116|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   117|
   118|🎨 Designer Agent:
   119|「登录页是否需要记住密码功能？」
   120|
   121|🏗️ Architect Agent:
   122|「后端用什么数据库？PostgreSQL / MySQL / 其他？」
   123|
   124|💻 CoderA Agent:
   125|「是否需要做单元测试？」
   126|
   127|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   128|
   129|回复格式：编号+答案（可多选），如「1 需要 2 PostgreSQL 3 需要」
   130|或「跳过该问题」
   131|```
   132|
   133|**提问格式（微信端）**：
   134|```
   135|📋 有 3 个问题需确认
   136|
   137|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   138|
   139|1️⃣ 登录页是否需要记住密码功能？
   140|   [需要] [不需要]
   141|
   142|2️⃣ 后端用什么数据库？
   143|   [PostgreSQL] [MySQL] [其他]
   144|
   145|3️⃣ 是否需要做单元测试？
   146|   [是] [否]
   147|
   148|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   149|
   150|回复编号，如「123」或「1 需要 3 是」
   151|```
   152|
   153|### 3.4 用户干预操作 [P0]
   154|
   155|**7 种操作定义**：
   156|
   157|| 操作 | 图标 | 触发时机 | 效果 |
   158||------|------|---------|------|
   159|| 暂停 | ⏸️ | 任何时候 | 暂停所有正在运行的 Agent，状态变为 `paused` |
   160|| 修改 | ✏️ | 任务执行中 | 修改当前任务的参数或方向，Agent 重新执行 |
   161|| 跳过 | ⏭️ | 任务执行中 | 跳过当前任务，标记为 `skipped`，继续后续任务 |
   162|| 回滚 | ↩️ | 任务完成后 | 回滚到上一个检查点，撤销产物变更 |
   163|| 中止 | 🛑 | 任何时候 | 终止整个对话，所有任务停止，对话状态变为 `aborted` |
   164|| 插入 | 📝 | 任何时候 | 在 DAG 中插入新任务，自动计算依赖关系 |
   165|| 提问 | 💬 | 任务执行中 | 向执行中的 Agent 发送补充指令 |
   166|
   167|**暂停/恢复流程**：
   168|```
   169|用户点击「暂停」
   170|    ↓
   171|Main Agent 发送暂停信号给所有运行中的 Agent
   172|    ↓
   173|Agent 保存当前状态，停止执行
   174|    ↓
   175|用户点击「恢复」
   176|    ↓
   177|Main Agent 唤醒 Agent，从暂停点继续
   178|```
   179|
   180|**修改任务流程**：
   181|```
   182|用户点击任务卡片 →「修改」
   183|    ↓
   184|弹窗显示任务详情，可修改：标题、描述、参数
   185|    ↓
   186|用户提交修改
   187|    ↓
   188|Main Agent 重新分配任务给对应 Agent
   189|    ↓
   190|Agent 重新执行，覆盖原产物
   191|```
   192|
   193|**回滚流程**：
   194|```
   195|用户点击「回滚」
   196|    ↓
   197|选择回滚目标（检查点列表）
   198|    ↓
   199|系统执行回滚操作：
   200|   - 代码恢复到 Git commit
   201|   - 数据库执行 down migration
   202|   - 文件恢复快照
   203|    ↓
   204|任务状态变为 `pending`，可重新执行
   205|```
   206|
   207|### 3.5 任务进度监控 [P0]
   208|
   209|**实时信息展示**：
   210|
   211|| 元素 | 说明 |
   212||------|------|
   213|| Agent 头像 | 当前 Agent 角色 |
   214|| 进度条 | 0-100% |
   215|| 状态标签 | 执行中 / 等待中 / 已完成 / 失败 |
   216|| 日志流 | 实时输出的 Agent 日志 |
   217|| 产物预览 | 生成的文件、代码片段 |
   218|| 预估剩余时间 | 根据当前进度计算 |
   219|
   220|**任务看板视图**：
   221|- 列：待办、进行中、审核中、已完成、失败
   222|- 卡片：任务标题、Agent、进度、时间
   223|
   224|**DAG 可视化视图**：
   225|- 节点：任务
   226|- 边：依赖关系
   227|- 实时更新：任务状态变化时动态刷新
   228|
   229|### 3.6 OpenClaw 集成 [P0]
   230|
   231|**Agent 启动流程**：
   232|```
   233|Main Agent 请求 OpenClaw 启动指定角色 Agent
   234|    ↓
   235|OpenClaw 创建 Agent 实例，注入任务上下文
   236|    ↓
   237|Agent 连接到 OpenClaw Runtime
   238|    ↓
   239|Agent 开始执行，调用工具（代码生成、文件读写等）
   240|    ↓
   241|Main Agent 监听 Agent 事件（进度、产物、错误）
   242|    ↓
   243|任务完成 → OpenClaw 销毁 Agent 实例
   244|```
   245|
   246|**事件通信**：
   247|```typescript
   248|// Main Agent → OpenClaw
   249|interface AgentStartRequest {
   250|  task_id: string;
   251|  agent_role: AgentRole;
   252|  task_context: {
   253|    description: string;
   254|    dependencies: Artifact[];
   255|    constraints: string[];
   256|  };
   257|}
   258|
   259|// OpenClaw → Main Agent
   260|interface AgentEvent {
   261|  task_id: string;
   262|  event_type: 'progress' | 'artifact' | 'question' | 'error' | 'completed';
   263|  payload: any;
   264|  timestamp: number;
   265|}
   266|```
   267|
   268|**工具调用限制**：
   269|- Agent 只能操作项目目录内的文件
   270|- 禁止系统级操作（如 rm -rf /）
   271|- 关键操作需用户确认（如数据库迁移）
   272|
   273|### 3.7 异常处理 [P0]
   274|
   275|**场景 1：Agent 执行失败**
   276|1. 任务标记为 `failed`
   277|2. 收集错误日志和堆栈信息
   278|3. Main Agent 分析失败原因
   279|4. 提示用户：重试 / 跳过 / 修改任务后重试
   280|
   281|**场景 2：依赖任务失败**
   282|1. 后置任务自动进入 `blocked` 状态
   283|2. 等待前置任务修复
   284|3. 用户修复前置任务后，阻塞任务自动恢复
   285|
   286|**场景 3：网络断开**
   287|1. 检测到连接断开
   288|2. 尝试重连（最多 3 次）
   289|3. 重连失败 → 暂停所有任务，等待用户操作
   290|
   291|**场景 4：超时**
   292|1. 任务超时后标记为 `failed`
   293|2. 可配置是否自动重试
   294|3. 记录超时日志供后续分析
   295|
   296|### 3.8 检查点机制 [P1]
   297|
   298|**检查点创建时机**：
   299|- 每个 Agent 完成后自动创建
   300|- 用户手动创建（在关键节点）
   301|
   302|**检查点内容**：
   303|- 当前任务产物快照
   304|- 数据库状态（migration 版本）
   305|- Git commit hash
   306|- 任务状态快照
   307|
   308|**恢复检查点**：
   309|```
   310|用户选择检查点 →「恢复」
   311|    ↓
   312|系统验证检查点完整性
   313|    ↓
   314|执行恢复操作：
   315|   - 代码恢复到指定 commit
   316|   - 数据库回滚到指定 migration
   317|   - 文件恢复快照
   318|    ↓
   319|任务状态恢复到检查点时刻
   320|```
   321|
   322|### 3.9 任务优先级调整 [P1]
   323|
   324|**优先级定义**：
   325|- P0：核心功能，阻塞其他任务
   326|- P1：重要功能
   327|- P2：次要功能
   328|
   329|**调整规则**：
   330|- 同优先级任务按依赖顺序执行
   331|- 高优先级任务优先分配资源
   332|- 用户可手动调整任务优先级
   333|
   334|### 3.10 手动触发任务 [P1]
   335|
   336|**场景**：
   337|- 用户想重新执行某个已完成的任务
   338|- 用户想强制执行某个失败的任务
   339|
   340|**流程**：
   341|1. 用户点击任务卡片 →「重新执行」
   342|2. 系统重置任务状态为 `pending`
   343|3. 重新分配 Agent 执行
   344|4. 覆盖原产物（或生成新版本）
   345|
   346|---
   347|
   348|## 4. 数据模型
   349|
   350|```sql
   351|-- 任务表
   352|CREATE TABLE tasks (
   353|  id              TEXT PRIMARY KEY,          -- UUID
   354|  project_id      TEXT NOT NULL,
   355|  conversation_id TEXT NOT NULL,
   356|  parent_id       TEXT,                      -- 父任务 ID
   357|  title           TEXT NOT NULL,
   358|  description     TEXT NOT NULL,
   359|  agent_role      TEXT NOT NULL,             -- main | pm | designer | architect | coderA | coderB | dba | devops
   360|  status          TEXT DEFAULT 'pending',     -- pending | assigned | in_progress | blocked | paused | done | failed | skipped
   361|  priority        INTEGER DEFAULT 1,         -- 0=P0, 1=P1, 2=P2
   362|  depends_on      TEXT DEFAULT '[]',         -- 依赖任务 ID 数组 JSON
   363|  estimated_time  INTEGER,                   -- 预估时间（分钟）
   364|  timeout         INTEGER DEFAULT 60,        -- 超时时间（分钟）
   365|  progress        INTEGER DEFAULT 0,         -- 进度 0-100
   366|  created_at      INTEGER NOT NULL,
   367|  started_at      INTEGER,
   368|  completed_at    INTEGER,
   369|  FOREIGN KEY (project_id) REFERENCES projects(id),
   370|  FOREIGN KEY (conversation_id) REFERENCES conversations(id),
   371|  FOREIGN KEY (parent_id) REFERENCES tasks(id)
   372|);
   373|
   374|-- 产物表
   375|CREATE TABLE artifacts (
   376|  id          TEXT PRIMARY KEY,              -- UUID
   377|  task_id     TEXT NOT NULL,
   378|  type        TEXT NOT NULL,                 -- code | doc | design | config | db_schema
   379|  path        TEXT NOT NULL,                 -- 文件路径
   380|  version     INTEGER DEFAULT 1,             -- 版本号
   381|  checksum    TEXT,                          -- 文件校验和
   382|  created_at  INTEGER NOT NULL,
   383|  FOREIGN KEY (task_id) REFERENCES tasks(id)
   384|);
   385|
   386|-- 检查点表
   387|CREATE TABLE checkpoints (
   388|  id          TEXT PRIMARY KEY,              -- UUID
   389|  task_id     TEXT NOT NULL,
   390|  name        TEXT NOT NULL,                 -- 检查点名称
   391|  snapshot    TEXT NOT NULL,                 -- 快照数据 JSON
   392|  git_commit  TEXT,                          -- Git commit hash
   393|  db_version  INTEGER,                       -- 数据库版本
   394|  created_at  INTEGER NOT NULL,
   395|  FOREIGN KEY (task_id) REFERENCES tasks(id)
   396|);
   397|
   398|-- Agent 执行日志
   399|CREATE TABLE agent_logs (
   400|  id          TEXT PRIMARY KEY,              -- UUID
   401|  task_id     TEXT NOT NULL,
   402|  agent_role  TEXT NOT NULL,
   403|  level       TEXT NOT NULL,                 -- info | warn | error | debug
   404|  message     TEXT NOT NULL,
   405|  created_at  INTEGER NOT NULL,
   406|  FOREIGN KEY (task_id) REFERENCES tasks(id)
   407|);
   408|
   409|-- 待提问队列
   410|CREATE TABLE pending_questions (
   411|  id          TEXT PRIMARY KEY,              -- UUID
   412|  task_id     TEXT NOT NULL,
   413|  agent_role  TEXT NOT NULL,
   414|  question    TEXT NOT NULL,
   415|  category    TEXT,                          -- 分类：技术选型 | 功能确认 | 边界条件
   416|  status      TEXT DEFAULT 'pending',       -- pending | asked | answered
   417|  batch_id    TEXT,                          -- 批次 ID（同一批次的提问）
   418|  created_at  INTEGER NOT NULL,
   419|  answered_at INTEGER,
   420|  FOREIGN KEY (task_id) REFERENCES tasks(id)
   421|);
   422|```
   423|
   424|---
   425|
   426|## 5. Tauri Commands 接口
   427|
   428|```typescript
   429|// DAG 管理
   430|generate_task_dag(conversationId: string, prd: string): Promise<Task[]>
   431|get_task_dag(conversationId: string): Promise<TaskDag>
   432|update_task_dependencies(taskId: string, dependsOn: string[]): Promise<void>
   433|
   434|// 任务执行
   435|start_task(taskId: string): Promise<void>
   436|pause_task(taskId: string): Promise<void>
   437|resume_task(taskId: string): Promise<void>
   438|cancel_task(taskId: string): Promise<void>
   439|skip_task(taskId: string): Promise<void>
   440|
   441|// 任务修改
   442|update_task(taskId: string, payload: UpdateTaskInput): Promise<Task>
   443|retry_task(taskId: string): Promise<void>
   444|
   445|// 用户干预
   446|rollback_to_checkpoint(checkpointId: string): Promise<void>
   447|insert_task(parentId: string, payload: CreateTaskInput): Promise<Task>
   448|send_agent_instruction(taskId: string, instruction: string): Promise<void>
   449|
   450|// 进度监控
   451|get_task_progress(taskId: string): Promise<TaskProgress>
   452|subscribe_task_events(taskId: string): EventChannel<TaskEvent>
   453|get_agent_logs(taskId: string, limit?: number): Promise<AgentLog[]>
   454|
   455|// 检查点
   456|create_checkpoint(taskId: string, name?: string): Promise<Checkpoint>
   457|list_checkpoints(taskId: string): Promise<Checkpoint[]>
   458|restore_checkpoint(checkpointId: string): Promise<void>
   459|
   460|// 问题汇总
   461|batch_questions(conversationId: string): Promise<QuestionBatch>
   462|answer_question_batch(batchId: string, answers: Record<string, string>): Promise<void>
   463|```
   464|
   465|---
   466|
   467|## 6. UI 交互流程
   468|
   469|### 6.1 DAG 确认流程
   470|
   471|```
   472|[需求澄清完成]
   473|    │
   474|    ▼
   475|[Main Agent 生成任务 DAG]
   476|    │
   477|    ▼
   478|[DAG 可视化页面]
   479|    ├─ 展示任务节点和依赖关系
   480|    ├─ 点击节点查看任务详情
   481|    ├─ 可拖拽调整节点位置
   482|    │
   483|    ▼
   484|[用户确认]
   485|    ├─ ✅ 确认 → 进入执行阶段
   486|    └─ ✏️ 修改 → 调整任务后重新确认
   487|```
   488|
   489|### 6.2 执行监控流程
   490|
   491|```
   492|[DAG 执行页面]
   493|    │
   494|    ├─ 左侧：任务列表（看板）
   495|    ├─ 中间：DAG 可视化（实时更新）
   496|    └─ 右侧：当前任务详情 + 日志流
   497|    │
   498|    ├─ 点击任务卡片
   499|    │   ▼
   500|    │   [查看详细日志]
   501|