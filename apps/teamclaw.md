# teamclaw（TeamClaw）

> This template should help get you started developing with Tauri, React and Typescript in Vite.

## 技术栈

| 类别 | 技术 |
|------|------|
| 语言 | React ^19.1.0 |
| 语言 | TypeScript |
| 样式 | Tailwind CSS |
| 状态管理 | Zustand |

## 关键依赖

| 包名 | 版本 |
|------|------|
| `@tauri-apps/api` | ^2 |
| `@tauri-apps/plugin-opener` | ^2 |
| `clsx` | ^2.1.1 |
| `lucide-react` | ^0.511.0 |
| `react` | ^19.1.0 |
| `react-dom` | ^19.1.0 |
| `tailwind-merge` | ^3.3.0 |
| `zustand` | ^5.0.5 |

## 项目结构

```
teamclaw/
├── .hermes/
│   ├── plans/
│   │   ├── 2026-05-21_154234-v3-architecture-robust-implementation.md
│   │   ├── 2026-05-21_164911-yuque-knowledge-base-taxonomy-optimization.md
│   ├── scripts/
│   │   ├── yuque_adjust_teamclaw_toc_v2.py
│   │   ├── yuque_audit_current.py
│   │   ├── yuque_cleanup_enrich_20260521.py
│   │   ├── yuque_prune_enrich_teamclaw.py
│   │   ├── yuque_remove_toc_numeric_prefixes.py
│   │   ├── yuque_reorder_teamclaw_toc.py
│   │   ├── yuque_repair_teamclaw_toc_runtime_docs_20260522.py
│   │   ├── yuque_restore_grouped_toc_20260521.py
│   ├── yuque-backups/
│   │   ├── cleanup-enrich-2026-05-21_172832/
│   │   ├── cleanup-enrich-2026-05-21_172852/
│   │   ├── cleanup-enrich-2026-05-21_173028/
│   │   ├── prune-enrich-2026-05-21_171633/
│   │   ├── prune-enrich-2026-05-21_171655/
│   │   ├── repair-runtime-docs-toc-2026-05-22_151249/
│   │   ├── repair-runtime-docs-toc-2026-05-22_151448/
│   │   ├── repair-runtime-docs-toc-2026-05-22_152018/
│   │   ├── repair-runtime-docs-toc-2026-05-22_152034/
│   │   ├── repair-runtime-docs-toc-2026-05-22_152311/
│   │   ├── repair-runtime-docs-toc-2026-05-22_162750/
│   │   ├── repair-runtime-docs-toc-2026-05-22_162917/
│   │   ├── repair-runtime-docs-toc-2026-05-22_163152/
│   │   ├── repair-runtime-docs-toc-2026-05-22_163623/
│   │   ├── repair-runtime-docs-toc-2026-05-22_165458/
│   │   ├── repair-runtime-docs-toc-2026-05-22_170130/
│   │   ├── repair-runtime-docs-toc-2026-05-22_170142/
│   │   ├── repair-runtime-docs-toc-2026-05-22_170857/
│   │   ├── repair-runtime-docs-toc-2026-05-22_170903/
│   │   ├── repair-runtime-docs-toc-2026-05-22_171508/
│   │   ├── repair-runtime-docs-toc-2026-05-22_171516/
│   │   ├── repair-runtime-docs-toc-2026-05-22_172111/
│   │   ├── repair-runtime-docs-toc-2026-05-22_172118/
│   │   ├── repair-runtime-docs-toc-2026-05-22_172802/
│   │   ├── repair-runtime-docs-toc-2026-05-22_172956/
│   │   ├── repair-runtime-docs-toc-2026-05-22_173611/
│   │   ├── repair-runtime-docs-toc-2026-05-22_173616/
│   │   ├── repair-runtime-docs-toc-2026-05-22_174135/
│   │   ├── repair-runtime-docs-toc-2026-05-22_174136/
│   │   ├── repair-runtime-docs-toc-2026-05-22_174714/
│   │   ├── repair-runtime-docs-toc-2026-05-22_174720/
│   │   ├── repair-runtime-docs-toc-2026-05-22_175344/
│   │   ├── repair-runtime-docs-toc-2026-05-22_175345/
│   │   ├── repair-runtime-docs-toc-2026-05-22_175921/
│   │   ├── repair-runtime-docs-toc-2026-05-22_175931/
│   │   ├── repair-runtime-docs-toc-2026-05-22_180518/
│   │   ├── repair-runtime-docs-toc-2026-05-22_180519/
│   │   ├── repair-runtime-docs-toc-2026-05-22_181157/
│   │   ├── repair-runtime-docs-toc-2026-05-22_181205/
│   │   ├── repair-runtime-docs-toc-2026-05-22_181857/
│   │   ├── repair-runtime-docs-toc-2026-05-22_181902/
│   │   ├── repair-runtime-docs-toc-2026-05-22_182410/
│   │   ├── repair-runtime-docs-toc-2026-05-22_182415/
│   │   ├── repair-runtime-docs-toc-2026-05-22_183011/
│   │   ├── repair-runtime-docs-toc-2026-05-22_183016/
```

---
*最后同步: 2026-05-24 18:01*
