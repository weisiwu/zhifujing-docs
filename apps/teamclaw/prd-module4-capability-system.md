---
title: PRD — 模块4：能力系统
---

     1|# PRD — 模块4：能力系统（Capability System）
     2|
     3|> 版本：V1.0  
     4|> 最后更新：2026-04-17  
     5|> 优先级：P1（增强功能）
     6|
     7|---
     8|
     9|## 1. 功能概述
    10|
    11|能力系统是 TeamClaw 多 Agent 协作的底层基座。它定义了每个 Agent「能做什么」——包括 Agent 角色的身份、职责边界、可用工具、通信协议和 Prompt 模板。能力系统为模块 2（多 Agent 编排）和模块 3（任务体系）提供 Agent 实例化与调用的标准接口，确保 Agent 间协作有规可循、有迹可循。
    12|
    13|本模块的核心目标：
    14|- **角色标准化**：8 种 Agent 角色（Main、PM、Designer、Architect、CoderA、CoderB、DBA、DevOps）拥有统一的角色定义结构，可扩展
    15|- **能力可发现**：每个 Agent 的能力以能力卡片（Capability Card）形式注册到全局能力注册中心，其他 Agent 可查询并调用
    16|- **通信规范化**：Agent 间消息传递、事件订阅遵循统一的通信协议，支持同步 invoke 和异步 hook 两种模式
    17|- **Prompt 可管理**：Agent 的系统提示词、角色设定、上下文模板集中管理，支持版本控制和热更新
    18|- **权限可控制**：能力矩阵定义每个 Agent 角色可调用哪些能力和工具，防止越权操作
    19|- **运行时可追踪**：Agent 执行上下文贯穿整个生命周期，支持状态快照、异常恢复和调试回放
    20|
    21|---
    22|
    23|## 2. 核心概念
    24|
    25|### 2.1 Agent 角色（Agent Role）
    26|
    27|Agent 角色是能力系统的基础单元。每个角色定义了一类 Agent 的身份标识、职责范围和可用能力集合。角色是静态定义的，Agent 实例是运行时创建的。
    28|
    29|```
    30|AgentRole (静态定义)          AgentInstance (运行时)
    31|┌──────────────────┐         ┌──────────────────┐
    32|│ role: 'coderA'   │ ──创建──►│ instance_id: uuid │
    33|│ display_name     │         │ role: 'coderA'   │
    34|│ description      │         │ status: running   │
    35|│ capabilities[]   │         │ context: {...}    │
    36|│ permissions[]    │         │ created_at        │
    37|│ prompt_template  │         └──────────────────┘
    38|│ tool_bindings[]  │
    39|│ constraints[]    │
    40|└──────────────────┘
    41|```
    42|
    43|### 2.2 能力卡片（Capability Card）
    44|
    45|能力卡片是 Agent 能力的最小描述单元。一个 Agent 角色可以拥有多张能力卡片，每张卡片描述一个原子能力。
    46|
    47|```typescript
    48|interface CapabilityCard {
    49|  id: string;                  // 能力唯一标识，如 'code_generation'
    50|  name: string;                // 能力名称，如 '代码生成'
    51|  description: string;         // 能力描述
    52|  category: CapabilityCategory;// 能力分类
    53|  input_schema: JSONSchema;    // 输入参数定义
    54|  output_schema: JSONSchema;   // 输出结果定义
    55|  version: string;             // 能力版本号，如 '1.2.0'
    56|  owner_roles: AgentRole[];    // 拥有此能力的角色列表
    57|  required_tools: string[];    // 执行此能力需要的工具列表
    58|  timeout: number;             // 执行超时时间（秒）
    59|  tags: string[];              // 标签，用于检索
    60|}
    61|```
    62|
    63|### 2.3 能力注册中心（Capability Registry）
    64|
    65|能力注册中心是全局单例服务，负责维护所有已注册能力的索引。Agent 启动时注册自身能力，其他 Agent 通过注册中心发现和调用能力。
    66|
    67|```
    68|┌─────────────────────────────────────────────┐
    69|│            Capability Registry               │
    70|│                                             │
    71|│  ┌─────────────────────────────────────┐    │
    72|│  │  能力索引（capability_index）        │    │
    73|│  │  code_generation   → CoderA, CoderB │    │
    74|│  │  prd_writing       → PM             │    │
    75|│  │  ui_design         → Designer       │    │
    76|│  │  architecture      → Architect      │    │
    77|│  │  schema_design     → DBA            │    │
    78|│  │  deployment        → DevOps         │    │
    79|│  │  task_orchestration→ Main           │    │
    80|│  └─────────────────────────────────────┘    │
    81|│                                             │
    82|│  ┌─────────────────────────────────────┐    │
    83|│  │  权限矩阵（permission_matrix）       │    │
    84|│  │  CoderA  → [code_generation, ...]   │    │
    85|│  │  CoderB  → [code_generation, ...]   │    │
    86|│  │  PM      → [prd_writing, ...]       │    │
    87|│  └─────────────────────────────────────┘    │
    88|└─────────────────────────────────────────────┘
    89|```
    90|
    91|### 2.4 通信协议（Communication Protocol）
    92|
    93|Agent 间通信遵循统一的消息格式，支持两种调用模式：
    94|
    95|| 模式 | 标识 | 说明 | 场景 |
    96||------|------|------|------|
    97|| 同步调用 | `invoke` | 调用方等待返回结果 | CoderA 调用 DBA 查询表结构 |
    98|| 异步钩子 | `hook` | 调用方不等待，被调用方自行处理 | 任务完成后通知 DevOps 执行部署 |
    99|
   100|### 2.5 Prompt 模板（Prompt Template）
   101|
   102|Prompt 模板是 Agent 的"灵魂"，定义了 Agent 的行为模式、输出规范和上下文注入方式。
   103|
   104|| 模板类型 | 标识 | 说明 |
   105||---------|------|------|
   106|| 系统提示词 | `system_prompt` | Agent 身份、职责、行为准则 |
   107|| 角色设定 | `persona` | Agent 的性格特征、沟通风格 |
   108|| 上下文模板 | `context_template` | 动态注入的项目信息、任务信息、依赖产物 |
   109|| 输出规范 | `output_format` | Agent 输出的格式要求（如 Markdown、JSON） |
   110|| 工具说明 | `tool_instruction` | Agent 可用工具的使用说明 |
   111|
   112|---
   113|
   114|## 3. 用户故事
   115|
   116|| 编号 | 用户故事 | 优先级 |
   117||------|---------|--------|
   118|| US-01 | 作为用户，我想看到每个 Agent 角色的职责和能力说明 | P1 |
   119|| US-02 | 作为用户，我想查看当前项目中已激活的 Agent 角色列表 | P1 |
   120|| US-03 | 作为用户，我想为项目自定义 Agent 的 Prompt 模板（如增加特定技术栈要求） | P1 |
   121|| US-04 | 作为用户，我想查看 Agent 间的调用关系和通信日志 | P1 |
   122|| US-05 | 作为用户，我想在 Agent 执行过程中查看其上下文信息（当前任务、依赖产物等） | P1 |
   123|| US-06 | 作为用户，我想启用/禁用某些 Agent 能力（如禁止 Agent 直接执行部署） | P1 |
   124|| US-07 | 作为系统管理员，我想配置 Agent 的能力权限矩阵 | P1 |
   125|| US-08 | 作为用户，我想回放 Agent 的执行上下文用于调试 | P2 |
   126|| US-09 | 作为高级用户，我想创建自定义 Agent 角色（如 CodeReviewer） | P2 |
   127|| US-10 | 作为用户，我想导入/导出 Agent 配置（Prompt、权限等） | P2 |
   128|| US-11 | 作为用户，我想查看 Agent 的 Token 消耗统计（按角色、按任务） | P2 |
   129|| US-12 | 作为开发者，我想通过 API 注册自定义能力插件 | P3 |
   130|
   131|---
   132|
   133|## 4. 功能需求清单
   134|
   135|### 4.1 Agent 角色定义与管理 [P1]
   136|
   137|**内置角色定义**：
   138|
   139|| 角色 | 标识 | 职责 | 核心能力 |
   140||------|------|------|---------|
   141|| 主管 | `main` | 任务接收、拆解、调度、汇总提问 | task_orchestration, question_aggregation, progress_monitoring |
   142|| 产品经理 | `pm` | 需求分析、PRD 编写 | requirement_analysis, prd_writing, user_story_generation |
   143|| 设计师 | `designer` | UI/UX 设计、原型制作 | ui_design, prototype_generation, style_guide_creation |
   144|| 架构师 | `architect` | 技术选型、架构设计、API 设计 | architecture_design, api_design, tech_stack_selection |
   145|| 前端开发 | `coderA` | 前端代码开发 | code_generation, component_development, frontend_testing |
   146|| 后端开发 | `coderB` | 后端代码开发 | code_generation, api_implementation, backend_testing |
   147|| 数据库管理员 | `dba` | 数据库设计、迁移脚本 | schema_design, migration_creation, query_optimization |
   148|| 运维工程师 | `devops` | 部署配置、CI/CD、环境管理 | deployment_config, cicd_setup, environment_management |
   149|
   150|**角色定义结构**：
   151|```typescript
   152|interface AgentRoleDefinition {
   153|  role: AgentRole;
   154|  display_name: string;
   155|  emoji: string;                      // 如 🏗️
   156|  description: string;
   157|  responsibilities: string[];
   158|  capabilities: string[];             // 能力 ID 列表
   159|  permissions: PermissionSet;
   160|  constraints: Constraint[];
   161|  prompt_config: PromptConfig;
   162|  tool_bindings: ToolBinding[];
   163|  metadata: RoleMetadata;
   164|}
   165|
   166|interface PermissionSet {
   167|  can_invoke: AgentRole[];            // 可调用的 Agent 角色
   168|  can_be_invoked_by: AgentRole[];     // 可被哪些角色调用
   169|  allowed_tools: string[];
   170|  denied_tools: string[];
   171|  max_concurrent_instances: number;
   172|  requires_user_confirmation: string[];// 需要用户确认的操作
   173|}
   174|```
   175|
   176|**角色管理操作**：
   177|- 查看所有角色定义（只读）
   178|- 查看角色详情（能力、权限、约束）
   179|- 项目级角色配置覆盖（如为特定项目修改 PM 的 Prompt）
   180|- 角色启用/禁用
   181|
   182|### 4.2 能力注册与发现机制 [P1]
   183|
   184|**能力分类体系**：
   185|
   186|| 分类 | 标识 | 说明 |
   187||------|------|------|
   188|| 分析能力 | `analysis` | 需求分析、技术分析、风险评估 |
   189|| 设计能力 | `design` | UI 设计、架构设计、数据建模 |
   190|| 生成能力 | `generation` | 代码生成、文档生成、配置生成 |
   191|| 执行能力 | `execution` | 代码运行、测试执行、部署执行 |
   192|| 审核能力 | `review` | 代码审查、设计审查、PRD 审核 |
   193|| 通信能力 | `communication` | 问题提问、进度汇报、结果汇总 |
   194|| 协调能力 | `coordination` | 任务调度、依赖管理、冲突解决 |
   195|
   196|**注册流程**：
   197|```
   198|Agent 实例启动
   199|    ↓
   200|读取角色定义中的 capabilities 列表
   201|    ↓
   202|向 Capability Registry 注册每张能力卡片
   203|    ↓
   204|Registry 校验能力定义合法性
   205|    ↓
   206|校验通过 → 加入能力索引，通知其他 Agent
   207|校验失败 → 拒绝注册，返回错误信息
   208|    ↓
   209|Agent 就绪，可接受能力调用
   210|```
   211|
   212|**发现接口**：
   213|```typescript
   214|query_capability(capabilityId: string): CapabilityCard
   215|query_capabilities_by_role(role: AgentRole): CapabilityCard[]
   216|query_capabilities_by_category(category: string): CapabilityCard[]
   217|search_capabilities(keyword: string): CapabilityCard[]
   218|get_capability_dependency_graph(): CapabilityGraph
   219|```
   220|
   221|**能力健康检查**：
   222|- 每个 Agent 实例定期（每 30 秒）向 Registry 发送心跳
   223|- 心跳超时（90 秒无响应）→ 标记该 Agent 的能力为「不可用」
   224|- 能力恢复时自动重新标记为「可用」
   225|
   226|### 4.3 Agent 间通信协议 [P1]
   227|
   228|**消息格式**：
   229|```typescript
   230|interface AgentMessage {
   231|  id: string;
   232|  from: { instance_id: string; role: AgentRole };
   233|  to: { instance_id?: string; role?: AgentRole };
   234|  type: MessageType;
   235|  payload: AgentMessagePayload;
   236|  context: {
   237|    task_id: string;
   238|    conversation_id: string;
   239|    correlation_id?: string;
   240|  };
   241|  timestamp: number;
   242|  priority: 'low' | 'normal' | 'high' | 'urgent';
   243|  ttl: number;
   244|}
   245|
   246|type MessageType =
   247|  | 'invoke_request' | 'invoke_response' | 'invoke_error'
   248|  | 'hook_event' | 'hook_ack'
   249|  | 'status_update' | 'progress_report'
   250|  | 'question_broadcast' | 'artifact_share' | 'context_sync';
   251|```
   252|
   253|**invoke（同步调用）流程**：
   254|```
   255|CoderA ── invoke_request ──────► DBA
   256|         { capability: 'schema_query', params: { table: 'users' } }
   257|                                   [DBA 执行]
   258|CoderA ◄── invoke_response ──── DBA
   259|         { result: { columns: [...] } }
   260|```
   261|
   262|**hook（异步钩子）流程**：
   263|```
   264|CoderA ── hook_event ──────► DevOps
   265|         { event: 'code_completed', params: { files: [...] } }
   266|CoderA ◄── hook_ack ──────── DevOps
   267|         { status: 'received' }
   268|                  [DevOps 异步处理]
   269|CoderA ◄── status_update ── DevOps { status: 'deployed' }
   270|```
   271|
   272|**事件订阅**：
   273|```typescript
   274|interface EventSubscription {
   275|  id: string;
   276|  subscriber_instance_id: string;
   277|  event_types: MessageType[];
   278|  filter?: { from_roles?: AgentRole[]; task_ids?: string[] };
   279|}
   280|```
   281|
   282|**消息队列管理**：
   283|- 每个 Agent 实例拥有独立的消息队列，按优先级排序
   284|- 队列容量上限 1000 条，超出后丢弃低优先级消息并告警
   285|- 消息 TTL 到期后自动丢弃
   286|
   287|### 4.4 能力调用接口（invoke/hook 机制） [P1]
   288|
   289|**调用接口**：
   290|```typescript
   291|interface InvokeRequest {
   292|  capability_id: string;
   293|  target_role?: AgentRole;
   294|  target_instance_id?: string;
   295|  params: Record<string, any>;
   296|  timeout?: number;        // 默认 60 秒
   297|  priority?: MessagePriority;
   298|}
   299|
   300|interface InvokeResult {
   301|  success: boolean;
   302|  data?: any;
   303|  error?: AgentError;
   304|  latency_ms: number;
   305|  from_instance: string;
   306|}
   307|
   308|interface HookEvent {
   309|  event_type: string;
   310|  capability_id?: string;
   311|  payload: Record<string, any>;
   312|  broadcast: boolean;
   313|  target_roles?: AgentRole[];
   314|}
   315|```
   316|
   317|**调用路由策略**：
   318|
   319|| 策略 | 标识 | 说明 | 适用场景 |
   320||------|------|------|---------|
   321|| 角色路由 | `by_role` | 按角色找到空闲实例 | 通用场景 |
   322|| 实例直连 | `by_instance` | 指定实例 ID | 需要特定上下文 |
   323|| 负载均衡 | `least_busy` | 选择任务最少的实例 | 多实例并行 |
   324|
   325|### 4.5 Agent Prompt 模板管理 [P1]
   326|
   327|**Prompt 配置结构**：
   328|```typescript
   329|interface PromptConfig {
   330|  system_prompt: PromptTemplate;
   331|  persona: PromptTemplate;
   332|  context_template: PromptTemplate;
   333|  output_format: PromptTemplate;
   334|  tool_instruction: PromptTemplate;
   335|  guardrails: PromptTemplate;
   336|}
   337|
   338|interface PromptTemplate {
   339|  id: string;
   340|  version: string;           // 语义化版本
   341|  content: string;           // 支持 {{variable}} 插值
   342|  variables: TemplateVariable[];
   343|  language: string;
   344|  is_active: boolean;
   345|  created_at: number;
   346|  updated_at: number;
   347|}
   348|```
   349|
   350|**模板变量插值示例**：
   351|```
   352|原始模板：
   353|你是 {{project_name}} 项目的 {{role_display_name}}（{{role_emoji}}）。
   354|项目描述：{{project_description}}
   355|技术栈：{{tech_stack}}
   356|
   357|插值后：
   358|你是 电商后台系统 项目的前端开发（💻）。
   359|项目描述：一个全栈电商管理后台，包含商品管理、订单管理等模块
   360|技术栈：React + TypeScript + TailwindCSS + Node.js + PostgreSQL
   361|```
   362|
   363|**Prompt 版本管理**：
   364|- 每次修改自动创建新版本，旧版本保留
   365|- 支持版本回退和 diff 对比
   366|- 遵循语义化版本（SemVer）
   367|
   368|**项目级 Prompt 覆盖**：
   369|```
   370|系统默认 Prompt（全局）→ 项目级 Prompt 覆盖 → 任务级 Prompt 增强
   371|最终 Prompt = 基础模板 + 项目覆盖 + 任务增强
   372|```
   373|
   374|### 4.6 Agent 执行上下文与状态追踪 [P1]
   375|
   376|**执行上下文结构**：
   377|```typescript
   378|interface AgentExecutionContext {
   379|  instance_id: string;
   380|  role: AgentRole;
   381|  task_id: string;
   382|  task_description: string;
   383|  conversation_id: string;
   384|  project_id: string;
   385|
   386|  status: AgentStatus;
   387|  // initializing | ready | executing | waiting_response
   388|  // waiting_user | paused | completed | failed | terminated
   389|  progress: number;           // 0-100
   390|
   391|  input_context: {
   392|    artifacts: ArtifactReference[];
   393|    messages: ContextMessage[];
   394|    user_instructions: string[];
   395|  };
   396|
   397|  output_state: {
   398|    generated_artifacts: ArtifactReference[];
   399|    pending_questions: string[];
   400|    errors: AgentError[];
   401|  };
   402|
   403|  resource_usage: {
   404|    total_tokens: number;
   405|    input_tokens: number;
   406|    output_tokens: number;
   407|    api_calls: number;
   408|  };
   409|
   410|  snapshots: ContextSnapshot[];
   411|}
   412|```
   413|
   414|**状态快照机制**：
   415|
   416|| 时机 | 类型 | 说明 |
   417||------|------|------|
   418|| Agent 开始执行 | `auto` | 记录初始状态 |
   419|| invoke 调用前/后 | `auto` | 记录调用边界状态 |
   420|| 用户发送补充指令 | `auto` | 记录用户干预点 |
   421|| Agent 遇到错误 | `error` | 记录错误现场 |
   422|| 用户手动触发 | `manual` | 手动保存检查点 |
   423|
   424|### 4.7 能力权限与约束 [P1]
   425|
   426|**权限矩阵**：
   427|
   428|```
   429|              Main  PM  Designer  Architect  CoderA  CoderB  DBA  DevOps
   430|Main           ✅    ✅    ✅        ✅        ✅      ✅      ✅    ✅
   431|PM             ❌    ❌    ✅        ✅        ❌      ❌      ❌    ❌
   432|Designer       ❌    ❌    ❌        ✅        ❌      ❌      ❌    ❌
   433|Architect      ❌    ❌    ❌        ❌        ❌      ❌      ✅    ❌
   434|CoderA         ❌    ❌    ✅        ❌        ❌      ❌      ✅    ❌
   435|CoderB         ❌    ❌    ❌        ✅        ❌      ❌      ✅    ✅
   436|DBA            ❌    ❌    ❌        ❌        ❌      ❌      ❌    ❌
   437|DevOps         ❌    ❌    ❌        ❌        ❌      ❌      ❌    ❌
   438|
   439|✅ = 可调用    ❌ = 不可调用
   440|```
   441|
   442|> 注：Main Agent 作为主管角色，可调用所有角色。具体权限可在项目级配置中覆盖。
   443|
   444|**工具权限矩阵**：
   445|
   446|| 工具 | Main | PM | Designer | Architect | CoderA | CoderB | DBA | DevOps |
   447||------|------|-----|----------|-----------|--------|--------|-----|--------|
   448|| 文件读取 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
   449|| 文件写入 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
   450|| 代码执行 | ⚠️ | ❌ | ❌ | ❌ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
   451|| 数据库操作 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ⚠️ |
   452|| 部署操作 | ⚠️ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
   453|| 网络请求 | ⚠️ | ❌ | ❌ | ❌ | ⚠️ | ⚠️ | ❌ | ⚠️ |
   454|
   455|> ⚠️ = 需要用户确认后才能执行
   456|
   457|**约束条件定义**：
   458|
   459|| 约束类型 | 说明 | 默认值 |
   460||---------|------|-------|
   461|| 超时 | 单次能力调用最大时长 | 60 秒 |
   462|| 重试 | 失败后最大重试次数 | 3 次 |
   463|| 文件范围 | 允许操作的目录范围 | 项目目录内 |
   464|| Token 预算 | 单次任务最大 Token 用量 | 50,000 |
   465|| 并发限制 | 同一角色最大并行实例数 | 4 |
   466|
   467|### 4.8 能力的热加载与配置 [P1]
   468|
   469|**热加载场景**：
   470|1. 运行时更新 Agent Prompt 模板（无需重启）
   471|2. 运行时调整能力权限配置
   472|3. 运行时启用/禁用特定能力
   473|4. 运行时更新工具绑定配置
   474|
   475|**热加载流程**：
   476|```
   477|用户修改配置（Prompt/权限/工具）
   478|    ↓
   479|配置版本号递增
   480|    ↓
   481|写入配置存储（SQLite）
   482|    ↓
   483|通过事件总线广播配置变更事件
   484|    ↓
   485|运行中的 Agent 收到变更通知
   486|    ↓
   487|Agent 在下次任务开始时应用新配置
   488|    ↓
   489|当前正在执行的任务不受影响
   490|```
   491|
   492|**配置变更通知**：
   493|```typescript
   494|interface ConfigChangeEvent {
   495|  config_type: 'prompt' | 'permission' | 'tool_binding' | 'constraint';
   496|  role: AgentRole;
   497|  project_id?: string;               // 项目级变更时指定
   498|  old_version: string;
   499|  new_version: string;
   500|  changed_fields: string[];
   501|