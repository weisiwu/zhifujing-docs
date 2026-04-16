import { defineConfig } from 'vitepress'

export default defineConfig({
  title: '致富经',
  description: '项目文档中心 — 学习、实践与项目沉淀',
  lang: 'zh-CN',

  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }]
  ],

  themeConfig: {
    logo: '/logo.svg',

    nav: [
      { text: '首页', link: '/' },
      { text: '应用项目', link: '/apps/' },
      { text: '学习笔记', link: '/notes/' },
    ],

    sidebar: {
      '/apps/': [
        {
          text: '应用项目',
          items: [
            { text: '项目总览', link: '/apps/' },
            { text: 'xiaowutools-v2（小工具箱）', link: '/apps/xiaowutools-v2' },
            { text: 'teamclaw（团队协作）', link: '/apps/teamclaw' },
            {
              text: 'TeamClaw 设计文档',
              collapsed: true,
              items: [
                { text: '项目总览', link: '/apps/teamclaw-project' },
                { text: '系统架构', link: '/apps/teamclaw/architecture' },
                { text: '对话生命周期', link: '/apps/teamclaw/conversation-lifecycle' },
                {
                  text: 'PRD 文档',
                  items: [
                    { text: '模块1：项目导入', link: '/apps/teamclaw/project/prd-module1-project-import' },
                    { text: '模块2：多Agent编排', link: '/apps/teamclaw/project/prd-module2-agent-orchestration' },
                  ]
                },
              ]
            },
            { text: 'projects-dashboard（项目仪表盘）', link: '/apps/projects-dashboard' },
            { text: 'poetry-app（诗词应用）', link: '/apps/poetry-app' },
          ]
        }
      ],
      '/notes/': [
        {
          text: '个人学习',
          collapsed: false,
          items: [
            { text: '笔记总览', link: '/notes/' },
            { text: 'ACP 协议解析', link: '/notes/learning/acp' },
            { text: 'AI 生成 APP 设计稿', link: '/notes/learning/ai-app-design' },
            { text: 'Claude Code 源码架构', link: '/notes/learning/claude-code-arch' },
            { text: 'Dify 知识库构建', link: '/notes/learning/dify-knowledge-base' },
            { text: 'MaxKB 知识库构建', link: '/notes/learning/maxkb-knowledge-base' },
            { text: 'OpenClaw Subagent 体系', link: '/notes/learning/openclaw-subagent' },
            { text: 'OpenClaw 事件与钩子', link: '/notes/learning/openclaw-events-hooks' },
            { text: 'OpenClaw 能力地图', link: '/notes/learning/openclaw-tools' },
            { text: 'OpenClaw CLI 强化 Agent', link: '/notes/learning/openclaw-cli' },
            { text: 'RAGFlow 知识库构建', link: '/notes/learning/ragflow-knowledge-base' },
            { text: 'RAPTOR 递归摘要检索', link: '/notes/learning/raptor' },
            { text: 'Token 中转站解析', link: '/notes/learning/token-gateway' },
            { text: '个人 Markdown 知识库方案', link: '/notes/learning/markdown-knowledge-base' },
          ]
        },
        {
          text: '实战笔记',
          collapsed: false,
          items: [
            { text: 'Agent 超时排查实录', link: '/notes/practice/agent-timeout' },
            { text: '自动迭代 Issue 幂等性分析', link: '/notes/practice/issue-idempotent' },
            { text: 'GitHub Actions 调度改造', link: '/notes/practice/actions-loop' },
          ]
        }
      ],
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com' }
    ],

    search: {
      provider: 'local',
      options: {
        locales: {
          root: {
            translations: {
              button: { buttonText: '搜索', buttonAriaLabel: '搜索文档' },
              modal: {
                noResultsText: '无法找到相关结果',
                resetButtonTitle: '清除查询条件',
                footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' }
              }
            }
          }
        }
      }
    },

    footer: {
      message: '致富经项目文档',
      copyright: '© 2024-2026'
    },
  },

  lastUpdated: true,
  cleanUrls: true,
})
