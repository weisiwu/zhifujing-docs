# xiaowutools-v2（小工具箱）

> 一个在线工具网站，提供短视频下载、图片格式转换、微信截图生成等实用小工具。面向普通用户和自媒体创作者。

## 技术栈

| 类别 | 技术 |
|------|------|
| 框架 | Next.js 14 (App Router) |
| 语言 | TypeScript + React 18 |
| 样式 | Tailwind CSS + shadcn/ui 风格 |
| 图片处理 | Sharp（图片/ICO 转换） |
| 视频解析 | Puppeteer（抖音/TikTok） |
| PDF 工具 | jsPDF / pdf-lib / pdfjs-dist |
| 码相关 | QRCode / jsQR / JsBarcode |
| 部署 | Vercel + Analytics + Speed Insights |

## 核心功能

### 🎬 抖音/TikTok 下载器
- 输入视频链接，解析无水印视频
- 支持 MP3 音频提取
- 基于 Puppeteer 的服务端解析

### 🖼️ 图片转 ICO
- 上传图片，选择输出尺寸（16~256px）
- 基于 Sharp 的高质量转换
- 支持批量尺寸输出

### 💬 微信聊天截图生成
- 自定义头像、昵称、对话内容
- 支持文字/图片/红包/转账消息类型
- 实时预览，所见即所得

### 🎨 设计特色
- 渐变紫粉主色调
- 响应式布局（Mobile / Tablet / Desktop 三断点）
- 暗色模式支持

## 项目结构

```
xiaowutools-v2/
├── app/              # Next.js App Router 页面
├── components/       # React 组件
├── public/           # 静态资源
├── scripts/          # 构建与部署脚本
├── docs/             # 项目文档
├── SPEC.md           # 功能规格说明
├── AGENTS.md         # Agent 协作指南
└── squirrel.toml     # 配置文件
```

## 相关链接

- 已部署至 Vercel（`.vercel` 目录已存在）
- 包含自动化版本 bump 脚本
- 配置了 lint + build 质量门禁
