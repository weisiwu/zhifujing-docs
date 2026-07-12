# 本机 Docker 服务与镜像运行手册

> 最后核对：2026-07-12（Apple M4 / Docker Desktop linux/arm64）  
> 统一控制脚本：`~/.local/bin/local-services`  
> 配置源：`~/Desktop/致富经/infra/local-services/`

## 运行策略

本机采用“三个 Hermes 消息实例与 Sub2API 常驻，其他 Docker 服务按需”的策略：

- 常驻消息实例是宿主机 LaunchAgent `ai.hermes.gateway`、`ai.hermes.gateway.xst` 和 `ai.hermes.gateway.teamclaw`，不运行在 Docker 中。
- Sub2API 及其专用 Redis/PostgreSQL 常驻，由 Docker 重启策略和 Startup Governance 双重保障。
- RapidOCR、Firecrawl、New API、Open Design、TeamClaw 和本地数据库默认停止。
- OpenClaw 消息网关默认停止，需要时通过统一命令临时启动。
- 按需容器统一使用 `restart=no`；Docker Desktop 或电脑重启后不会自行恢复。
- `com.user.startup-governance` 每 300 秒运行一次，确保 main、XST、TeamClaw 三个 Hermes 和 Sub2API；它明确跳过 OpenClaw 网关和 New API keepalive。
- 各应用的 Redis/PostgreSQL 是应用私有依赖，不跨应用混用，避免数据结构、版本和生命周期互相影响。
- 停止容器不会删除镜像或业务数据；任何卷删除都必须单独确认。

## 常用命令

```bash
# 查看全部服务
local-services status all

# 手动启动和停止
local-services start ocr
local-services stop ocr
local-services start firecrawl
local-services stop firecrawl

# 启动服务、等待就绪、执行命令、自动停止
local-services run ocr -- curl -sS http://127.0.0.1:9003/health

# 停止全部按需服务
local-services stop ondemand
```

可管理的名称：

| 名称 | 作用 |
|---|---|
| `ocr` | RapidOCR 中文 OCR API |
| `firecrawl` | Firecrawl 及其五个容器 |
| `sub2api` | 常驻的 Sub2API、Redis、PostgreSQL；也可手动重启 |
| `new-api` | New API、生图桥接和宿主机 keepalive |
| `open-design` | Open Design |
| `teamclaw` | 当前 TeamClaw Compose |
| `local-db` | 本地数据库工具 |
| `message-xst` | XST Hermes 消息配置 |
| `message-teamclaw` | TeamClaw Hermes 消息配置 |
| `message-openclaw` | OpenClaw 消息网关 |
| `ondemand` | 全部按需 Docker 服务 |

## 服务拓扑

### RapidOCR

| 属性 | 当前配置 |
|---|---|
| 容器 | `local-rapidocr` |
| 镜像 | `android-xianyu-auto-checkin-ocr:latest`，约 786MB |
| 模型 | RapidOCR 3.9.1 / PP-OCRv6 small / ONNX Runtime |
| 地址 | `http://127.0.0.1:9003` |
| 健康检查 | `GET /health` |
| OCR 接口 | `POST /ocr`，multipart 字段名 `file` |
| 数据卷 | 无；模型随镜像保存 |
| Compose | `~/Desktop/致富经/apps/android-xianyu-auto-checkin/docker-compose.ocr.yml` |
| 策略 | 按需；`restart=no` |

用途是开发期批量截图识别和 Android ML Kit 结果交叉验证。Android 应用运行时不依赖这个服务。

宿主机闲鱼执行器在 OCR 不可用时会通过 `local-services start ocr` 临时启动；如果是它启动的服务，会在执行结束或异常退出的 `finally` 阶段自动停止。若 OCR 原本已由其他任务启动，则不会越权关闭。

### Firecrawl

Firecrawl 必须作为一个整体启动，不能只启 API：

| 容器 | 镜像 | 作用 |
|---|---|---|
| `firecrawl-api-1` | `ghcr.nju.edu.cn/firecrawl/firecrawl:latest`，约 1.35GB | 抓取 API 和任务协调 |
| `firecrawl-playwright-service-1` | `ghcr.nju.edu.cn/firecrawl/playwright-service:latest`，约 2.29GB | 浏览器渲染 |
| `firecrawl-nuq-postgres-1` | `ghcr.nju.edu.cn/firecrawl/nuq-postgres:latest`，约 644MB | 队列/任务数据库 |
| `firecrawl-rabbitmq-1` | `rabbitmq:3-management`，约 408MB | 消息队列 |
| `firecrawl-redis-1` | `redis:alpine`，约 133MB | 缓存与限流 |

- Compose：`~/Desktop/firecrawl/docker-compose.yaml` 与 `docker-compose.images.yaml`。
- 默认 API 端口为 `3002`。
- PostgreSQL 和 RabbitMQ 使用 Docker 卷保存数据；Redis 没有持久卷。
- 这是当前最重的服务组，使用后应及时执行 `local-services stop firecrawl`。
- 现有 Compose 把 API 发布到所有网卡；若没有局域网调用需求，应后续收紧为 `127.0.0.1:3002:3002`。

### Sub2API

| 属性 | 当前配置 |
|---|---|
| 主容器 | `sub2api`，镜像 `sub2api:latest`，约 138MB |
| 依赖 | `sub2api-redis`（Redis 8）和 `sub2api-postgres`（PostgreSQL 18） |
| 地址 | `http://127.0.0.1:8080` |
| 应用数据 | `~/.local/share/sub2api/deploy/data` |
| Redis 数据 | `~/.local/share/sub2api/deploy/redis_data` |
| PostgreSQL 数据 | `~/.local/share/sub2api/deploy/postgres_data` |
| 策略 | 三个容器成组常驻；数据库健康后再启动 API；`restart=unless-stopped` |

该服务不是闲鱼自动化每日主链路依赖；账户余额或模型可用性不足时不能用于无人值守关键路径。`com.user.startup-governance` 每 300 秒检查一次，停止或 Docker 恢复后会重新启动整组服务。

### New API 与生图桥接

| 属性 | 当前配置 |
|---|---|
| 容器 | `new-api-local` |
| 镜像 | `calciumion/new-api:latest`，约 276MB |
| 容器端口 | 当前为宿主机 `3000` |
| 数据目录 | `~/.hermes/new-api-runtime/local-data` |
| Keepalive | `~/Library/LaunchAgents/com.zfj.new-api.keepalive.plist` |
| 生图桥接 | `codex_image_bridge.py`，默认端口 `18080` |
| 策略 | `start new-api` 同时加载 keepalive；`stop new-api` 同时卸载桥接和容器 |

New API 和生图桥接不属于消息接收主线。现有容器和桥接监听所有网卡，若只在本机调用，应后续改为 `127.0.0.1`。

### Open Design

| 属性 | 当前配置 |
|---|---|
| 容器 | `our-open-design` |
| 镜像 | `our-opendesign:local`，约 747MB |
| 地址 | `http://127.0.0.1:7456` |
| 数据卷 | `our-open-design_our_open_design_data`，挂载到 `/app/.od` |
| 策略 | 按需 |

`open-design-upstream:local` 是构建/对照镜像，没有运行容器；不要把它误认为第二个常驻服务。

### TeamClaw

- 当前 Compose：`~/Desktop/致富经/apps/teamclaw/docker-compose.yml`。
- 当前定义的是 `teamclaw-runtime` Web Admin 和 Runtime API placeholder。
- 默认端口为 `14211` 和 `14210`；启动前应确认是否需要限制为本机地址。
- 旧 `_legacy-nextjs` 的 `teamclaw-redis` 与 `teamclaw-chroma` 孤儿容器已经移除。
- 历史卷 `teamclaw_redis-data`、`teamclaw_chroma-data`、`teamclaw_postgres-data` 暂时保留作为回滚保险。

### 本地数据库工具

| 属性 | 当前配置 |
|---|---|
| 容器 | `local-db` |
| 镜像 | `local-db:latest`，约 252MB |
| 数据目录 | `~/Documents/work/本地数据库/data` |
| Compose | `~/Documents/work/本地数据库/docker-compose.yml` |
| 策略 | 按需 |

## 消息主线

Hermes 消息实例运行于 macOS LaunchAgent，不在 Docker 中。当前常驻：

```text
ai.hermes.gateway
ai.hermes.gateway.xst
ai.hermes.gateway.teamclaw
```

以下附加消息线默认卸载，但 plist 文件保留：

- `ai.openclaw.gateway`

不要把 New API、ntfy、Redis 或 RabbitMQ 误认为主消息线；它们分别是模型网关、通知工具或应用内部队列。

## 构建与工具镜像

以下镜像没有常驻容器，主要用于构建、测试或作为基础层：

| 镜像 | 大小 | 用途/判断 |
|---|---:|---|
| `wei123098/capnograph-android-builder:android-35-agp-8.8.0` | 约 2.26GB | Android 构建环境，保留 |
| `packflow:codex-check` | 约 1.58GB | Packflow/Codex 检查环境，按需 |
| `golang:1.25` | 约 1.27GB | Go 构建基础镜像 |
| `golang:1.26.4-alpine` | 约 357MB | Go Alpine 构建基础镜像 |
| `node:24-alpine` | 约 230MB | Node 构建基础镜像 |
| `python:3.11-slim-bookworm` | 约 224MB | OCR 构建基础镜像；与 ECR 标签指向同一 image ID，不是两份数据 |
| `public.ecr.aws/docker/library/python:3.11-slim-bookworm` | 约 224MB | 上一项的镜像源别名，共享层 |
| `python:3.13-slim` | 约 203MB | Python 构建基础镜像 |
| `ainovel-cli:local` | 约 32MB | AI 小说 CLI 工具镜像 |
| `alpine:3.21` / `alpine:3.22` | 约 13MB | 通用基础镜像 |

判断“重复镜像”时应看 image ID 和共享层，而不是只看标签。两个标签指向同一 image ID 不会占用两份完整空间。

## 数据卷边界

当前业务卷包括：

- Firecrawl PostgreSQL 与 RabbitMQ 卷。
- Sub2API 的宿主机绑定目录和 PostgreSQL 匿名兼容卷。
- Open Design 数据卷。
- Capnograph Gradle 缓存卷。
- TeamClaw 三个历史回滚卷。

安全清理顺序：

1. `docker ps -a` 确认服务已停止。
2. `docker system df -v` 确认镜像、卷和缓存的引用关系。
3. 先清理悬空镜像：`docker image prune`。
4. 构建缓存只按时间清理，例如 `docker builder prune --filter 'until=168h'`。
5. 不使用 `docker volume prune`，除非已经逐个确认业务数据可以永久删除。
6. 不使用 `docker image prune -a` 作为日常操作，否则按需服务下次启动需要重新下载大镜像。

## 排障

### 服务启动后下次开机又自动运行

```bash
docker inspect <容器> --format '{{.HostConfig.RestartPolicy.Name}}'
docker update --restart=no <容器>
```

统一入口会在每次启动后自动执行这一约束。

### New API 停止后又自动复活

检查并卸载宿主机 keepalive：

```bash
launchctl list | grep com.zfj.new-api.keepalive
local-services stop new-api
```

若附加消息网关或 New API 每五分钟重新出现，检查 `~/.local/bin/ensure-startup-services.sh`。它不应再调用这些可选 LaunchAgent；对应日志位于 `~/Library/Logs/startup-governance/ensure.log`。

### OCR 调用失败

```bash
local-services start ocr
curl -sS http://127.0.0.1:9003/health
docker logs --tail 100 local-rapidocr
```

### 确认当前只有消息主线常驻

```bash
docker ps
launchctl list | grep -E 'ai\.hermes\.gateway|ai\.openclaw\.gateway'
```

空闲基线下，预期 Docker 只运行 `sub2api`、`sub2api-redis` 和 `sub2api-postgres`，LaunchAgent 出现 main、XST、TeamClaw 三个 Hermes。RapidOCR 等按需服务在任务执行期间临时出现属于正常情况。

## 维护规则

- 新增服务时必须登记镜像、端口、数据目录、健康检查、启动依赖和停止方式。
- 本机服务默认绑定 `127.0.0.1`；确需局域网访问时单独记录原因和认证方式。
- 默认 `restart=no`；只有消息接收主线和 Sub2API 服务组允许常驻。
- Compose 文件与本手册不写 Token、密码、Cookie、账号或完整请求日志。
- 修改统一控制脚本后，至少验证一次 `bash -n`、服务启动、健康检查、停止和最终常驻状态。
