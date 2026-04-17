# 小伍工具箱 (xiaowutools)

## ① 项目介绍

> 基于 Next.js 14 + React + Tailwind CSS 的在线工具箱网站，集成多种实用工具。

小伍工具箱是一个 AI 工具导航网站，收录 370+ 在线工具，涵盖短视频下载、图片格式转换、微信截图生成等日常实用功能。

| 项目 | 信息 |
|------|------|
| 名称 | xiaowutools (xiaowutools-v2) |
| 框架 | Next.js 14.x (App Router) |
| 语言 | TypeScript + React 18 |
| 样式 | Tailwind CSS |
| UI 组件 | shadcn/ui 风格 |
| 图片处理 | Sharp |
| 部署 | Vercel |
| GitHub | [weisiwu/zhifujing-tools](https://github.com/weisiwu/zhifujing-tools) |
| 在线地址 | [xiaowutools.com](https://xiaowutools.com) |

### 功能列表

| 工具 | 说明 |
|------|------|
| 抖音/TikTok 下载器 | 一键提取无水印短视频 |
| 图片转 ICO | 在线转换图片为 ICO 格式 |
| 微信截图生成器 | 自定义对话内容生成微信截图 |
| 更多工具 | 持续迭代添加中... |

## ② 应用截图

<!-- 截图待补充，请将截图放入 docs/public/screenshots/xiaowutools/ 目录 -->
<!-- 示例格式：
![首页](/screenshots/xiaowutools/home.png)
![工具页](/screenshots/xiaowutools/tools.png)
-->

:::info 截图待添加
请将应用截图放入 `docs/public/screenshots/xiaowutools/` 目录，然后在此处引用。
:::

## ③ 项目结构

:::details 点击展开完整目录树
```
xiaowutools/
├── app/                  # Next.js App Router 页面
│   ├── tools/           # 各工具页面
│   ├── about/           # 关于页面
│   ├── contact/         # 联系方式
│   ├── privacy/         # 隐私政策
│   └── terms/           # 使用条款
├── components/          # React 组件
│   ├── Header.tsx       # 顶部导航
│   ├── Footer.tsx       # 页脚
│   ├── ToolsGrid.tsx    # 工具网格
│   └── LanguageSwitcher.tsx  # 语言切换
├── scripts/             # 构建与运维脚本
│   ├── auto-upgrade.sh  # 自动升级脚本
│   └── batch-translate.js  # 批量翻译
└── public/              # 静态资源
```
:::

## ④ 项目现状

**整体进度：90% ✅ 已上线运行**

- ✅ 核心工具功能完整（短视频下载、ICO 转换、截图生成）
- ✅ 国际化 (i18n) 中英文切换
- ✅ SEO 优化（sitemap.xml、robots.txt、Open Graph）
- ✅ AdSense 广告集成
- ✅ Vercel Analytics 性能监控
- ✅ 自动版本管理（build-version 递增）
- ✅ 已部署至 Vercel，绑定域名 xiaowutools.com

## ⑤ 项目待办

### 待办事项
- [ ] 添加更多实用工具（JSON 格式化、Base64 编解码等）
- [ ] 优化移动端适配体验
- [ ] 添加用户反馈入口

### 可优化项
- [ ] 工具页面加载性能优化（lazy loading）
- [ ] 搜索功能增强（全文检索）
- [ ] 暗色模式支持

### 存在问题
- 暂无已知阻塞问题

## ⑥ 全链路技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **前端框架** | Next.js 14 (App Router) | SSR/SSG 混合渲染 |
| **UI 层** | React 18 + TypeScript | 组件化开发 |
| **样式方案** | Tailwind CSS | 原子化 CSS |
| **UI 组件库** | shadcn/ui 风格 | 可定制组件 |
| **图片处理** | Sharp | 服务端图片转换（ICO 等） |
| **国际化** | next-intl / 自建 i18n | 中英文切换 |
| **广告** | Google AdSense | 多广告位组件 |
| **部署** | Vercel | 自动 CI/CD + Edge Network |
| **监控** | Vercel Analytics | Web Vitals + 访问统计 |
| **版本管理** | build-version 脚本 | 自动递增版本号 |
| **SEO** | Sitemap + robots + OG | 搜索引擎优化全套 |

## ⑦ 文档合集

<!-- 后续可在此添加更多文档链接 -->

| 文档 | 链接 |
|------|------|
| GitHub 仓库 | [weisiwu/zhifujing-tools](https://github.com/weisiwu/zhifujing-tools) |
| 在线访问 | [xiaowutools.com](https://xiaowutools.com) |

---

*最后更新: 2026-04-18*
