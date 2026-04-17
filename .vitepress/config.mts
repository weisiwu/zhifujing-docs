import { defineConfig } from 'vitepress'

export default defineConfig({
  title: '致富经',
  description: '个人项目开发与技术文档中心',
  lang: 'zh-CN',

  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }]
  ],

  themeConfig: {
    logo: '/logo.svg',

    nav: [
      { text: '首页', link: '/' },
      {
        text: '应用项目',
        items: [
          { text: '🛠️ 小伍工具箱 (xiaowutools)', link: '/apps/xiaowutools' },
          { text: '🤝 TeamClaw 协作平台', link: '/apps/teamclaw' },
          { text: '📊 项目仪表盘 (Dashboard)', link: '/apps/projects-dashboard' },
          { text: '📜 诗词应用 (Poetry App)', link: '/apps/poetry-app' },
        ]
      },
      { text: '学习笔记', link: '/notes/' },
    ],

    sidebar: {
      '/apps/teamclaw': [
        {
          text: 'TeamClaw 协作平台',
          items: [
            { text: '📋 项目总览', link: '/apps/teamclaw' },
          ]
        },
        {
          text: '🏗️ 设计文档',
          items: [
            { text: '系统架构设计', link: '/apps/teamclaw/architecture' },
            { text: '对话生命周期', link: '/apps/teamclaw/conversation-lifecycle' },
          ]
        },
        {
          text: '📝 PRD 文档',
          collapsible: true,
          items: [
            { text: '模块1：项目导入', link: '/apps/teamclaw/prd-module1-project-import' },
            { text: '模块2：Agent 编排', link: '/apps/teamclaw/prd-module2-agent-orchestration' },
            { text: '模块3：任务体系', link: '/apps/teamclaw/prd-module3-task-system' },
            { text: '模块4：能力系统', link: '/apps/teamclaw/prd-module4-capability-system' },
            { text: '模块5：知识库', link: '/apps/teamclaw/prd-module5-knowledge-base' },
            { text: '模块6：对话生命周期', link: '/apps/teamclaw/prd-module6-conversation-lifecycle' },
          ]
        },
        {
          text: '🔧 技术分析',
          items: [
            { text: '技术栈深度分析', link: '/apps/teamclaw/tech-stack' },
            { text: '技术方案设计合集', link: '/apps/teamclaw/tech-plans' },
          ]
        },
        {
          text: '🔙 返回',
          items: [
            { text: '← 项目一览', link: '/apps/' },
          ]
        }
      ],
      '/apps/': [
        {
          text: '应用项目',
          items: [
            { text: '项目一览', link: '/apps/' },
            { text: '小伍工具箱 (xiaowutools)', link: '/apps/xiaowutools' },
            { text: 'TeamClaw 协作平台', link: '/apps/teamclaw' },
            { text: '项目仪表盘 (Dashboard)', link: '/apps/projects-dashboard' },
            { text: '诗词应用 (Poetry App)', link: '/apps/poetry-app' },
          ]
        },
        {
          text: 'TeamClaw 设计文档',
          items: [
            { text: '系统架构', link: '/apps/teamclaw/architecture' },
            { text: '对话生命周期', link: '/apps/teamclaw/conversation-lifecycle' },
            { text: 'PRD: Agent 编排', link: '/apps/teamclaw/prd-module2-agent-orchestration' },
          ]
        }
      ],
      '/notes/': [
        {
          text: '技术学习',
          items: [
            { text: '学习笔记索引', link: '/notes/' },
            { text: 'ACP 协议解析', link: '/notes/learning/acp' },
            { text: 'AI 生成 APP 设计稿', link: '/notes/learning/ai-app-design' },
            { text: 'Claude Code 源码架构', link: '/notes/learning/claude-code-arch' },
            { text: 'Dify 知识库构建', link: '/notes/learning/dify-knowledge-base' },
            { text: 'MaxKB 知识库构建', link: '/notes/learning/maxkb-knowledge-base' },
            { text: 'OpenClaw CLI 强化 Agent', link: '/notes/learning/openclaw-cli' },
            { text: 'OpenClaw 事件与钩子', link: '/notes/learning/openclaw-events-hooks' },
            { text: 'OpenClaw Subagent 体系', link: '/notes/learning/openclaw-subagent' },
            { text: 'OpenClaw 能力地图', link: '/notes/learning/openclaw-tools' },
            { text: 'RAGFlow 知识库构建', link: '/notes/learning/ragflow-knowledge-base' },
            { text: 'RAPTOR 递归摘要检索', link: '/notes/learning/raptor' },
            { text: 'Token 中转站解析', link: '/notes/learning/token-gateway' },
            { text: 'Markdown 知识库方案', link: '/notes/learning/markdown-knowledge-base' },
          ]
        },
        {
          text: '实战笔记',
          items: [
            { text: 'GitHub Actions 迭代调度', link: '/notes/practice/actions-loop' },
            { text: 'Agent 超时无响应排查', link: '/notes/practice/agent-timeout' },
            { text: 'Issue 残留与幂等性设计', link: '/notes/practice/issue-idempotent' },
          ]
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/weisiwu/zhifujing-docs' }
    ],

    footer: {
      message: '致富经 — 项目开发 & 技术沉淀',
      copyright: '© 2025-2026 致富经项目'
    },

    search: {
      provider: 'local'
    }
  }
})
