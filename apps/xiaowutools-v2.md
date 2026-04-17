# xiaowutools-v2（小工具箱）

> 基于 Next.js 14 + React + Tailwind CSS 的在线工具箱网站，集成多种实用工具。

## 基本信息

| 项目 | 信息 |
|------|------|
| 名称 | xiaowutools-v2 |
| 框架 | Next.js 14.x (App Router) |
| 语言 | TypeScript + React 18 |
| 样式 | Tailwind CSS |
| UI 组件 | shadcn/ui 风格 |
| 图片处理 | Sharp |
| 部署 | Vercel |
| GitHub | [weisiwu/zhifujing-tools](https://github.com/weisiwu/zhifujing-tools) |

## 功能列表

| 工具 | 说明 |
|------|------|
| 抖音/TikTok 下载器 | 一键提取无水印短视频 |
| 图片转 ICO | 在线转换图片为 ICO 格式 |
| 微信截图生成器 | 自定义对话内容生成微信截图 |
| 更多工具 | 持续迭代添加中... |

## 目录结构

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

## 特色

- **国际化 (i18n)** — 支持中英文切换
- **SEO 优化** — sitemap.xml、robots.txt、Open Graph 元数据
- **AdSense 集成** — 多种广告位组件
- **自动版本管理** — build-version 自动递增
- **Vercel Analytics** — 访问数据与性能监控
