---
title: PRD — 模块5：知识库
---

     1|# PRD — 模块5：知识库（Knowledge Base）
     2|
     3|> 版本：V1.0
     4|> 最后更新：2026-04-17
     5|> 优先级：P1（增强功能）
     6|
     7|---
     8|
     9|## 1. 功能概述
    10|
    11|知识库是 TeamClaw 智能能力的核心组件，为 Agent 提供项目上下文、历史经验和领域知识的检索能力。它通过向量化存储和语义搜索，将项目的代码、文档、配置等结构化与非结构化内容转化为可检索的知识片段，支持 RAG（检索增强生成）流程，确保 Agent 在执行任务时能够精准定位相关资料。
    12|
    13|本模块的核心目标：
    14|- **多源索引**：支持代码、文档、配置等多种文件格式的索引和检索
    15|- **语义搜索**：基于向量化存储的语义搜索，而非简单关键词匹配
    16|- **增量更新**：监听文件变更，增量更新索引，避免全量重建
    17|- **RAG 集成**：与 Agent 对话流程无缝集成，自动检索上下文相关内容
    18|- **本地优先**：支持本地嵌入模型（onnxruntime + MiniLM）和 API 嵌入服务切换
    19|- **知识关联**：自动提取知识片段间的关联关系，构建项目知识图谱
    20|- **任务绑定**：知识库与任务、对话关联，支持按任务上下文精准检索
    21|
    22|---
    23|
    24|## 2. 核心概念
    25|
    26|### 2.1 知识片段（Knowledge Fragment）
    27|
    28|知识片段是知识库的最小可检索单元。一个文件被切分为多个片段，每个片段保持语义完整性。
    29|
    30|```typescript
    31|interface KnowledgeFragment {
    32|  id: string;                   // 唯一标识
    33|  file_id: string;              // 所属文件
    34|  content: string;              // 文本内容
    35|  embedding: number[];          // 向量表示（归一化）
    36|  metadata: {
    37|    file_type: string;          // md, py, ts, rs, json, yaml
    38|    language?: string;          // 代码语言（ts, rs, python 等）
    39|    start_line: number;         // 起始行号
    40|    end_line: number;           // 结束行号
    41|    tokens: number;             // Token 数量
    42|    created_at: string;
    43|    updated_at: string;
    44|  };
    45|  tags: string[];              // 自动提取的标签（如「数据库」「API」「前端」）
    46|}
    47|```
    48|
    49|### 2.2 知识库（Knowledge Base）
    50|
    51|知识库是按项目组织的数据集合。每个 TeamClaw 项目对应一个独立知识库。
    52|
    53|```
    54|KnowledgeBase
    55|├── project_id: "project-uuid"
    56|├── status: "active" | "building" | "error"
    57|├── fragments_count: 12345
    58|├── files_count: 256
    59|├── embedding_provider: "local" | "openai" | "zhipu"
    60|├── embedding_model: "sentence-transformers/all-MiniLM-L6-v2"
    61|├── last_indexed_at: "2026-04-17T05:00:00Z"
    62|├── storage_path: "/path/to/knowledge-bases/project-uuid"
    63|└── settings: {
    64|    chunk_size: 512,            // 每片段 Token 数
    65|    chunk_overlap: 50,          // 片段重叠 Token 数
    66|    max_fragments_per_file: 1000,
    67|    enable_auto_index: true
    68|  }
    69|```
    70|
    71|### 2.3 向量索引（Vector Index）
    72|
    73|向量索引用于高效检索相似片段。采用 IVF（Inverted File）索引结构。
    74|
    75|```
    76|Vector Index (IVF)
    77|├── nlist: 256                // 聚类中心数
    78|├── nprobe: 32                // 搜索时检查的聚类数
    79|├── metric: "cosine"           // 余弦相似度
    80|└── dimension: 384            // MiniLM-L6 向量维度
    81|```
    82|
    83|### 2.4 嵌入提供商（Embedding Provider）
    84|
    85|支持本地和远程两种嵌入方式。
    86|
    87|| 提供商 | 模型 | 维度 | 延迟 | 成本 | 用途 |
    88||--------|------|------|------|------|------|
    89|| Local | all-MiniLM-L6-v2 | 384 | ~20ms | 免费 | 离线、隐私敏感场景 |
    90|| OpenAI | text-embedding-3-small | 1536 | ~500ms | 付费 | 高精度需求 |
    91|| 智谱 | embedding-v2 | 1024 | ~300ms | 付费 | 中文优化 |
    92|
    93|---
    94|
    95|## 3. 用户故事
    96|
    97|### P1 优先级
    98|
    99|1. **作为开发者**，我希望首次打开项目时自动索引所有代码和文档，这样 Agent 就能立即检索上下文。
   100|2. **作为 PM**，我希望通过语义搜索查询「支付接口设计」相关内容，而非手动翻阅代码。
   101|3. **作为开发者**，我希望修改代码后知识库自动增量更新，而不是全量重建索引。
   102|4. **作为团队 Leader**，我希望查看知识库的健康状态（片段数量、索引状态、上次更新时间）。
   103|5. **作为开发者**，我希望切换本地和 API 嵌入模型，在离线和在线场景间无缝切换。
   104|6. **作为 PM**，我希望知识库与对话关联，查询时只返回当前对话上下文相关的知识。
   105|7. **作为开发者**，我希望手动触发全量索引重建，在索引损坏时快速恢复。
   106|
   107|### P2 优先级
   108|
   109|8. **作为开发者**，我希望查看知识图谱，了解模块、API、数据表之间的依赖关系。
   110|9. **作为 PM**，我希望导出知识片段为 JSON/CSV，便于外部工具处理。
   111|10. **作为开发者**，我希望排除某些目录（如 `node_modules`, `.git`）不被索引。
   112|11. **作为 QA**，我希望验证知识片段的完整性，确保无重复、无遗漏。
   113|
   114|### P3 优先级
   115|
   116|12. **作为开发者**，我希望自定义切分策略，针对不同文件类型采用不同规则。
   117|
   118|---
   119|
   120|## 4. 功能需求清单
   121|
   122|### 4.1 文件索引与扫描
   123|
   124|- 支持扫描项目目录下所有符合条件的文件
   125|- 按文件类型过滤器（支持 glob 模式：`**/*.md`, `src/**/*.ts`）
   126|- 默认排除目录：`node_modules`, `.git`, `dist`, `build`, `.next`
   127|- 支持自定义排除目录和文件扩展名
   128|- 按文件哈希检测变更，仅处理修改过的文件
   129|
   130|### 4.2 内容切分与片段生成
   131|
   132|- 按语义边界切分（如代码按函数/类，文档按段落）
   133|- 支持可配置的片段 Token 大小（默认 512）和重叠（默认 50）
   134|- 保留片段的元数据：文件路径、行号、语言类型
   135|- 针对不同文件类型应用不同切分策略
   136|
   137|### 4.3 向量化与嵌入
   138|
   139|- 本地嵌入模型：onnxruntime + MiniLM-L6-v2（首次自动下载）
   140|- API 嵌入服务：OpenAI text-embedding-3-small、智谱 embedding-v2
   141|- 支持批量嵌入（每批 100 个片段）
   142|- 嵌入结果缓存，避免重复计算
   143|
   144|### 4.4 语义搜索
   145|
   146|- 支持文本查询，自动向量化查询语句
   147|- 返回 Top-K 相似片段（K 可配置，默认 5）
   148|- 支持按文件类型、语言、标签过滤
   149|- 支持相似度阈值过滤（默认 > 0.7）
   150|
   151|### 4.5 增量索引
   152|
   153|- 基于文件系统监听（fs.watch）或 Git diff 检测变更
   154|- 新增文件：创建知识片段并嵌入
   155|- 修改文件：删除旧片段，重新切分和嵌入
   156|- 删除文件：删除相关片段
   157|- 支持手动触发增量索引
   158|
   159|### 4.6 知识图谱
   160|
   161|- 自动提取知识片段间的关联关系：
   162|  - 代码引用关系（import/require/include）
   163|  - API 调用关系
   164|  - 数据库表关联
   165|  - 文档交叉引用
   166|- 支持可视化图谱展示
   167|
   168|### 4.7 RAG 集成
   169|
   170|- Agent 对话时自动检索相关知识片段
   171|- 支持按对话上下文过滤（project_id, conversation_id）
   172|- 支持检索结果排序和去重
   173|- 支持检索结果摘要生成
   174|
   175|### 4.8 知识库管理
   176|
   177|- 查看知识库状态（片段数、文件数、最后更新时间）
   178|- 切换嵌入提供商
   179|- 配置切分策略
   180|- 手动触发全量重建
   181|- 导出知识片段
   182|
   183|---
   184|
   185|## 5. 数据模型
   186|
   187|### 5.1 SQLite 表结构
   188|
   189|#### knowledge_bases（知识库主表）
   190|
   191|```sql
   192|CREATE TABLE knowledge_bases (
   193|    id              TEXT PRIMARY KEY,
   194|    project_id      TEXT NOT NULL REFERENCES projects(id),
   195|    status          TEXT NOT NULL DEFAULT 'active', -- active, building, error
   196|    fragments_count INTEGER NOT NULL DEFAULT 0,
   197|    files_count     INTEGER NOT NULL DEFAULT 0,
   198|    embedding_provider TEXT NOT NULL DEFAULT 'local',
   199|    embedding_model TEXT NOT NULL DEFAULT 'all-MiniLM-L6-v2',
   200|    last_indexed_at TEXT,
   201|    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
   202|    updated_at      TEXT NOT NULL DEFAULT (datetime('now')),
   203|    UNIQUE(project_id)
   204|);
   205|
   206|CREATE INDEX idx_kb_project ON knowledge_bases(project_id);
   207|CREATE INDEX idx_kb_status ON knowledge_bases(status);
   208|```
   209|
   210|#### knowledge_fragments（知识片段表）
   211|
   212|```sql
   213|CREATE TABLE knowledge_fragments (
   214|    id              TEXT PRIMARY KEY,
   215|    knowledge_base_id TEXT NOT NULL REFERENCES knowledge_bases(id),
   216|    file_id         TEXT NOT NULL,
   217|    content         TEXT NOT NULL,
   218|    file_type       TEXT NOT NULL,
   219|    language        TEXT,
   220|    start_line      INTEGER NOT NULL,
   221|    end_line        INTEGER NOT NULL,
   222|    tokens          INTEGER NOT NULL,
   223|    embedding       BLOB NOT NULL, -- 序列化的浮点数组
   224|    tags            TEXT, -- JSON 数组
   225|    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
   226|    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
   227|);
   228|
   229|CREATE INDEX idx_kb_kb_id ON knowledge_fragments(knowledge_base_id);
   230|CREATE INDEX idx_kb_file_id ON knowledge_fragments(file_id);
   231|CREATE INDEX idx_kb_file_type ON knowledge_fragments(file_type);
   232|CREATE INDEX idx_kb_language ON knowledge_fragments(language);
   233|```
   234|
   235|#### knowledge_files（文件索引表）
   236|
   237|```sql
   238|CREATE TABLE knowledge_files (
   239|    id              TEXT PRIMARY KEY,
   240|    knowledge_base_id TEXT NOT NULL REFERENCES knowledge_bases(id),
   241|    file_path       TEXT NOT NULL,
   242|    file_hash       TEXT NOT NULL, -- SHA-256
   243|    file_size       INTEGER NOT NULL,
   244|    file_type       TEXT NOT NULL,
   245|    last_scanned_at TEXT NOT NULL DEFAULT (datetime('now')),
   246|    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
   247|    updated_at      TEXT NOT NULL DEFAULT (datetime('now')),
   248|    UNIQUE(knowledge_base_id, file_path)
   249|);
   250|
   251|CREATE INDEX idx_kf_kb_id ON knowledge_files(knowledge_base_id);
   252|CREATE INDEX idx_kf_hash ON knowledge_files(file_hash);
   253|```
   254|
   255|#### knowledge_graph_edges（知识图谱边表）
   256|
   257|```sql
   258|CREATE TABLE knowledge_graph_edges (
   259|    id              TEXT PRIMARY KEY,
   260|    knowledge_base_id TEXT NOT NULL REFERENCES knowledge_bases(id),
   261|    source_fragment_id TEXT NOT NULL REFERENCES knowledge_fragments(id),
   262|    target_fragment_id TEXT NOT NULL REFERENCES knowledge_fragments(id),
   263|    edge_type       TEXT NOT NULL, -- 'import', 'call', 'reference', 'related'
   264|    weight          REAL NOT NULL DEFAULT 1.0,
   265|    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
   266|);
   267|
   268|CREATE INDEX idx_kge_kb_id ON knowledge_graph_edges(knowledge_base_id);
   269|CREATE INDEX idx_kge_source ON knowledge_graph_edges(source_fragment_id);
   270|CREATE INDEX idx_kge_target ON knowledge_graph_edges(target_fragment_id);
   271|```
   272|
   273|#### knowledge_search_logs（搜索日志表）
   274|
   275|```sql
   276|CREATE TABLE knowledge_search_logs (
   277|    id              TEXT PRIMARY KEY,
   278|    knowledge_base_id TEXT NOT NULL REFERENCES knowledge_bases(id),
   279|    query           TEXT NOT NULL,
   280|    top_k           INTEGER NOT NULL,
   281|    results_count   INTEGER NOT NULL,
   282|    filters         TEXT, -- JSON
   283|    execution_time_ms INTEGER NOT NULL,
   284|    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
   285|);
   286|
   287|CREATE INDEX idx_ksl_kb_id ON knowledge_search_logs(knowledge_base_id);
   288|CREATE INDEX idx_ksl_created ON knowledge_search_logs(created_at DESC);
   289|```
   290|
   291|---
   292|
   293|## 6. Tauri Commands
   294|
   295|### 6.1 接口定义
   296|
   297|```typescript
   298|// ── 知识库管理 ──
   299|
   300|interface CreateKnowledgeBase {
   301|  project_id: string;
   302|  embedding_provider: 'local' | 'openai' | 'zhipu';
   303|  embedding_model?: string;
   304|}
   305|
   306|interface GetKnowledgeBase {
   307|  project_id: string;
   308|}
   309|
   310|interface UpdateKnowledgeBaseSettings {
   311|  knowledge_base_id: string;
   312|  settings: {
   313|    chunk_size?: number;
   314|    chunk_overlap?: number;
   315|    max_fragments_per_file?: number;
   316|    enable_auto_index?: boolean;
   317|  };
   318|}
   319|
   320|// ── 索引操作 ──
   321|
   322|interface TriggerFullIndex {
   323|  knowledge_base_id: string;
   324|  file_patterns?: string[]; // glob 模式，如 ['**/*.md', 'src/**/*.ts']
   325|  exclude_patterns?: string[]; // 如 ['node_modules', '.git']
   326|}
   327|
   328|interface TriggerIncrementalIndex {
   329|  knowledge_base_id: string;
   330|}
   331|
   332|interface GetIndexStatus {
   333|  knowledge_base_id: string;
   334|}
   335|
   336|// ── 搜索操作 ──
   337|
   338|interface SearchKnowledge {
   339|  knowledge_base_id: string;
   340|  query: string;
   341|  top_k?: number;
   342|  filters?: {
   343|    file_type?: string;
   344|    language?: string;
   345|    tags?: string[];
   346|  };
   347|  conversation_id?: string; // 限制在对话上下文内
   348|}
   349|
   350|// ── 知识图谱 ──
   351|
   352|interface GetKnowledgeGraph {
   353|  knowledge_base_id: string;
   354|  fragment_id?: string; // 可选：查询特定片段的关联
   355|  edge_type?: string;
   356|  max_depth?: number;
   357|}
   358|
   359|// ── 导出操作 ──
   360|
   361|interface ExportFragments {
   362|  knowledge_base_id: string;
   363|  format: 'json' | 'csv';
   364|  filters?: {
   365|    file_type?: string;
   366|    language?: string;
   367|  };
   368|}
   369|
   370|// ── 统计信息 ──
   371|
   372|interface GetKnowledgeStats {
   373|  knowledge_base_id: string;
   374|}
   375|```
   376|
   377|### 6.2 命令清单
   378|
   379|```rust
   380|#[tauri::command]
   381|fn create_knowledge_base(
   382|    state: State<DbState>,
   383|    project_id: String,
   384|    embedding_provider: String,
   385|    embedding_model: Option<String>
   386|) -> ApiResponse<KnowledgeBase>;
   387|
   388|#[tauri::command]
   389|fn get_knowledge_base(
   390|    state: State<DbState>,
   391|    project_id: String
   392|) -> ApiResponse<KnowledgeBase>;
   393|
   394|#[tauri::command]
   395|fn update_knowledge_base_settings(
   396|    state: State<DbState>,
   397|    knowledge_base_id: String,
   398|    settings: Json<Value>
   399|) -> ApiResponse<String>;
   400|
   401|#[tauri::command]
   402|fn trigger_full_index(
   403|    state: State<DbState>,
   404|    knowledge_base_id: String,
   405|    file_patterns: Option<Vec<String>>,
   406|    exclude_patterns: Option<Vec<String>>
   407|) -> ApiResponse<IndexTask>;
   408|
   409|#[tauri::command]
   410|fn trigger_incremental_index(
   411|    state: State<DbState>,
   412|    knowledge_base_id: String
   413|) -> ApiResponse<IndexTask>;
   414|
   415|#[tauri::command]
   416|fn get_index_status(
   417|    state: State<DbState>,
   418|    knowledge_base_id: String
   419|) -> ApiResponse<IndexStatus>;
   420|
   421|#[tauri::command]
   422|fn search_knowledge(
   423|    state: State<DbState>,
   424|    knowledge_base_id: String,
   425|    query: String,
   426|    top_k: Option<i32>,
   427|    filters: Option<Json<Value>>,
   428|    conversation_id: Option<String>
   429|) -> ApiResponse<Vec<SearchResult>>;
   430|
   431|#[tauri::command]
   432|fn get_knowledge_graph(
   433|    state: State<DbState>,
   434|    knowledge_base_id: String,
   435|    fragment_id: Option<String>,
   436|    edge_type: Option<String>,
   437|    max_depth: Option<i32>
   438|) -> ApiResponse<KnowledgeGraph>;
   439|
   440|#[tauri::command]
   441|fn export_fragments(
   442|    state: State<DbState>,
   443|    knowledge_base_id: String,
   444|    format: String,
   445|    filters: Option<Json<Value>>
   446|) -> ApiResponse<String>; // 返回导出内容或文件路径
   447|
   448|#[tauri::command]
   449|fn get_knowledge_stats(
   450|    state: State<DbState>,
   451|    knowledge_base_id: String
   452|) -> ApiResponse<KnowledgeStats>;
   453|```
   454|
   455|---
   456|
   457|## 7. UI 交互流程
   458|
   459|### 7.1 知识库概览界面
   460|
   461|```
   462|┌─────────────────────────────────────────────────────────┐
   463|│  知识库概览                                           │
   464|├─────────────────────────────────────────────────────────┤
   465|│  项目：TeamClaw                                       │
   466|│  状态：🟢 已索引 (12,345 片段)                         │
   467|│  最后更新：2026-04-17 05:00                           │
   468|│  嵌入模型：all-MiniLM-L6-v2 (本地)                    │
   469|├─────────────────────────────────────────────────────────┤
   470|│  [🔄 重建索引]  [⚙️ 设置]  [📊 统计]                  │
   471|├─────────────────────────────────────────────────────────┤
   472|│  搜索框                                            [🔍]│
   473|│  ───────────────────────────────────────────────────── │
   474|│  搜索结果（Top 5）：                                  │
   475|│  1. [src/db/mod.rs:45-78] DB 连接池初始化 (0.92)    │
   476|│  2. [docs/api/payment.md:12-34] 支付接口文档 (0.88) │
   477|│  3. [src/payment/service.ts:102-145] 支付服务 (0.85) │
   478|│  4. [README.md:5-15] 项目介绍 (0.79)               │
   479|│  5. [.env.example:1-8] 环境变量 (0.76)            │
   480|├─────────────────────────────────────────────────────────┤
   481|│  知识图谱预览                                         │
   482|│  ┌──────┐         ┌──────┐         ┌──────┐         │
   483|│  │ API  │────────►│Payment│────────►│  DB  │         │
   484|│  └──────┘         └──────┘         └──────┘         │
   485|└─────────────────────────────────────────────────────────┘
   486|```
   487|
   488|### 7.2 索引任务进度界面
   489|
   490|```
   491|┌─────────────────────────────────────────────────────────┐
   492|│  索引进行中...                                        │
   493|├─────────────────────────────────────────────────────────┤
   494|│  进度：██████████████████░░░░░░░░░ 65%               │
   495|│  已处理：256 / 394 文件                               │
   496|│  已生成：12,345 片段                                  │
   497|│  嵌入中：██████████████░░░░░ 80%                      │
   498|├─────────────────────────────────────────────────────────┤
   499|│  当前文件：src/payment/service.ts                     │
   500|│  状态：嵌入向量中...                                  │
   501|