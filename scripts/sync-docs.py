#!/usr/bin/env python3
"""
致富经文档同步脚本
扫描 apps/ 和学习笔记目录，自动更新 docs/ 下的 Markdown 文档。

用法：
  python scripts/sync-docs.py [--project-root /path/to/致富经] [--commit]

选项：
  --project-root  致富经项目根目录（默认自动检测）
  --commit        同步后自动 git commit + push
"""

import json
import os
import subprocess
import sys
import re
from pathlib import Path
from datetime import datetime


# ─── 配置 ─────────────────────────────────────────────

APPS = {
    "xiaowutools-v2": {
        "doc_file": "apps/xiaowutools-v2.md",
        "title": "xiaowutools-v2（小工具箱）",
        "description": "在线工具网站，提供短视频下载、图片格式转换、微信截图生成等实用小工具。",
        "extra_md": ["SPEC.md"],
    },
    "teamclaw": {
        "doc_file": "apps/teamclaw.md",
        "title": "teamclaw（TeamClaw）",
        "description": "现代化团队协作平台，项目管理、文档协作、飞书集成与多 Agent 自动迭代。",
        "extra_md": ["TECH_SPEC.md"],
    },
    "projects-dashboard": {
        "doc_file": "apps/projects-dashboard.md",
        "title": "projects-dashboard（项目仪表盘）",
        "description": "项目管理 Dashboard，集成数据可视化、拖拽排序、SEO 自动化。",
    },
    "poetry-app": {
        "doc_file": "apps/poetry-app.md",
        "title": "poetry-app（诗词应用）",
        "description": "基于 Expo 的跨平台诗词学习应用，支持 iOS/Android/Web。",
    },
}

NOTE_DIRS = {
    "个人/学习": "notes/learning",
    "学习笔记": "notes/practice",
}

# ─── 工具函数 ──────────────────────────────────────────

def run(cmd, cwd=None, check=True):
    """执行 shell 命令并返回输出"""
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if check and r.returncode != 0:
        print(f"  ⚠ 命令失败: {cmd}\n  {r.stderr.strip()}")
        return ""
    return r.stdout.strip()


def read_json(path):
    """安全读取 JSON 文件"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def read_text(path):
    """安全读取文本文件"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""


def extract_dep_groups(pkg):
    """从 package.json 提取依赖分组"""
    groups = {}
    for key in ["dependencies", "devDependencies", "peerDependencies"]:
        deps = pkg.get(key, {})
        if deps:
            groups[key] = deps
    return groups


def classify_tech_stack(pkg, deps_groups):
    """从 package.json 依赖推断技术栈"""
    all_deps = set()
    for group in deps_groups.values():
        all_deps.update(group.keys())

    stack = []

    # 框架
    if "next" in all_deps:
        ver = deps_groups.get("dependencies", {}).get("next", deps_groups.get("devDependencies", {}).get("next", ""))
        stack.append(("框架", f"Next.js {ver}"))
    elif "expo" in all_deps or "expo-router" in all_deps:
        ver = deps_groups.get("dependencies", {}).get("expo", "")
        stack.append(("框架", f"Expo {ver}"))
    elif "express" in all_deps:
        stack.append(("运行时", "Express"))

    # React
    if "react" in all_deps:
        ver = deps_groups.get("dependencies", {}).get("react", "")
        stack.append(("语言", f"React {ver}"))

    # TypeScript
    if "typescript" in all_deps:
        stack.append(("语言", "TypeScript"))

    # 样式
    if "tailwindcss" in all_deps or "@tailwindcss/postcss" in all_deps:
        stack.append(("样式", "Tailwind CSS"))

    # UI 库
    ui_libs = []
    for lib in ["@radix-ui/react-dialog", "@radix-ui/react-tabs", "react-native-paper"]:
        if lib in all_deps:
            ui_libs.append(lib.split("/")[-1])
    if ui_libs:
        stack.append(("UI", ", ".join(ui_libs)))

    # 状态管理
    if "zustand" in all_deps:
        stack.append(("状态管理", "Zustand"))
    if "@tanstack/react-query" in all_deps:
        stack.append(("数据获取", "TanStack React Query"))
    if "swr" in all_deps:
        stack.append(("数据获取", "SWR"))

    # 可视化
    if "recharts" in all_deps:
        stack.append(("可视化", "Recharts"))

    # 数据库/后端
    if "@supabase/supabase-js" in all_deps:
        stack.append(("后端", "Supabase"))
    if "better-sqlite3" in all_deps:
        stack.append(("本地存储", "better-sqlite3"))

    # 测试
    if "vitest" in all_deps:
        stack.append(("测试", "Vitest"))

    return stack


def get_dir_tree(app_path, max_depth=2, exclude=None):
    """获取目录树"""
    if exclude is None:
        exclude = {"node_modules", ".next", ".git", "dist", ".expo", ".DS_Store", ".windsurf", "__pycache__"}

    lines = []
    base_name = os.path.basename(app_path)

    def _walk(path, prefix="", depth=0):
        if depth > max_depth:
            return
        try:
            entries = sorted(os.listdir(path))
        except PermissionError:
            return
        dirs = []
        files = []
        for e in entries:
            if e in exclude or e.endswith(".log") or e.startswith("progress_"):
                continue
            full = os.path.join(path, e)
            if os.path.isdir(full):
                dirs.append(e)
            else:
                files.append(e)

        # 只显示关键文件
        key_exts = {".md", ".json", ".ts", ".tsx", ".js", ".mts", ".py", ".toml", ".yaml", ".yml"}
        key_files = [f for f in files if any(f.endswith(ext) for ext in key_exts) or f.startswith("Dockerfile") or f == ".env.example"]
        key_files = key_files[:20]  # 限制数量

        for d in dirs:
            lines.append(f"{prefix}├── {d}/")
            _walk(os.path.join(path, d), prefix + "│   ", depth + 1)
        for f in key_files:
            lines.append(f"{prefix}├── {f}")

    lines.append(f"{base_name}/")
    _walk(app_path)
    return "\n".join(lines[:60])  # 最多 60 行


def get_recent_changes(app_path, max_entries=5):
    """获取 git 最近变更"""
    output = run("git log --oneline -10 --no-decorate", cwd=app_path)
    if not output:
        return []
    entries = []
    for line in output.split("\n")[:max_entries]:
        parts = line.split(" ", 1)
        if len(parts) == 2:
            entries.append({"hash": parts[0][:7], "message": parts[1]})
    return entries


# ─── 同步逻辑 ──────────────────────────────────────────

def sync_app(app_name, app_path, config, docs_dir):
    """同步单个应用的文档"""
    doc_path = os.path.join(docs_dir, config["doc_file"])
    pkg_path = os.path.join(app_path, "package.json")
    readme_path = os.path.join(app_path, "README.md")

    print(f"\n📦 同步 {app_name}...")

    # 读取信息
    pkg = read_json(pkg_path)
    readme = read_text(readme_path)
    deps = extract_dep_groups(pkg)
    stack = classify_tech_stack(pkg, deps)
    tree = get_dir_tree(app_path)
    changes = get_recent_changes(app_path)

    # 提取 README 第一段描述（跳过标题）
    readme_desc = ""
    in_first_para = False
    for line in readme.split("\n"):
        stripped = line.strip()
        if stripped.startswith("#") and not in_first_para:
            continue
        if stripped and not in_first_para:
            in_first_para = True
            readme_desc += stripped + " "
        elif in_first_para and not stripped:
            break
    readme_desc = readme_desc.strip()

    # 构建 Markdown
    lines = []
    lines.append(f"# {config['title']}\n")
    desc = readme_desc if readme_desc else config["description"]
    lines.append(f"> {desc}\n")

    # 技术栈
    if stack:
        lines.append("## 技术栈\n")
        lines.append("| 类别 | 技术 |")
        lines.append("|------|------|")
        for cat, tech in stack:
            lines.append(f"| {cat} | {tech} |")
        lines.append("")

    # 关键依赖
    if deps.get("dependencies"):
        lines.append("## 关键依赖\n")
        lines.append("| 包名 | 版本 |")
        lines.append("|------|------|")
        for name, ver in sorted(deps["dependencies"].items()):
            lines.append(f"| `{name}` | {ver} |")
        lines.append("")

    # 项目结构
    if tree:
        lines.append("## 项目结构\n")
        lines.append("```")
        lines.append(tree)
        lines.append("```\n")

    # 更新日志
    if changes:
        lines.append("## 最近更新\n")
        lines.append("| Commit | 说明 |")
        lines.append("|--------|------|")
        for c in changes:
            lines.append(f"| `{c['hash']}` | {c['message']} |")
        lines.append("")

    # 脚本信息
    lines.append("---")
    lines.append(f"*最后同步: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")

    new_content = "\n".join(lines)

    # 对比是否变化
    old_content = read_text(doc_path)
    if new_content.strip() != old_content.strip():
        os.makedirs(os.path.dirname(doc_path), exist_ok=True)
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  ✅ 已更新 {config['doc_file']}")
        return True
    else:
        print(f"  ⏭ 无变化")
        return False


def sync_notes(notes_src, notes_dst, docs_dir):
    """同步学习笔记的索引页"""
    src_dir = os.path.join(os.path.dirname(docs_dir), notes_src)
    dst_index = os.path.join(docs_dir, notes_dst.replace("notes/", "") + "/index.md") if notes_dst.startswith("notes/") else None

    if not os.path.isdir(src_dir):
        print(f"  ⚠ 目录不存在: {src_dir}")
        return False

    print(f"\n📚 扫描 {notes_src}...")

    # 扫描 markdown 文件
    md_files = sorted([
        f for f in os.listdir(src_dir)
        if f.endswith(".md") and not f.startswith(".")
    ])

    changed = False
    for md_file in md_files:
        src_path = os.path.join(src_dir, md_file)
        content = read_text(src_path)
        if not content:
            continue

        # 提取标题和第一段
        title = md_file.replace(".md", "")
        first_para = ""
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped.startswith("#"):
                title = stripped.lstrip("#").strip()
                continue
            if stripped and not stripped.startswith("![") and not stripped.startswith("<!--"):
                first_para = stripped
                break

        print(f"  📄 {title}: {first_para[:60]}...")

    return changed


def main():
    # 解析参数
    args = sys.argv[1:]
    project_root = None
    do_commit = False

    for i, arg in enumerate(args):
        if arg == "--project-root" and i + 1 < len(args):
            project_root = args[i + 1]
        elif arg == "--commit":
            do_commit = True

    # 自动检测项目根目录
    if not project_root:
        script_dir = Path(__file__).resolve().parent
        project_root = str(script_dir.parent.parent)

    project_root = os.path.abspath(project_root)
    docs_dir = os.path.join(project_root, "docs")
    apps_dir = os.path.join(project_root, "apps")

    print(f"🏠 项目根目录: {project_root}")
    print(f"📁 文档目录: {docs_dir}")

    # 同步各应用
    any_changed = False
    for app_name, config in APPS.items():
        app_path = os.path.join(apps_dir, app_name)
        if not os.path.isdir(app_path):
            print(f"  ⚠ 跳过不存在的应用: {app_name}")
            continue
        if sync_app(app_name, app_path, config, docs_dir):
            any_changed = True

    # 同步笔记索引
    for src, dst in NOTE_DIRS.items():
        if sync_notes(src, dst, docs_dir):
            any_changed = True

    # Git 提交 & 推送
    if any_changed:
        print(f"\n📝 检测到文档变更")
        if do_commit:
            run("git add -A", cwd=docs_dir)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            run(f'git commit -m "docs: 自动同步 {timestamp}" --allow-empty', cwd=docs_dir)
            run("git push origin main", cwd=docs_dir)
            print(f"  ✅ 已提交并推送到 GitHub")
        else:
            print(f"  ℹ 使用 --commit 参数自动提交推送")
    else:
        print(f"\n✅ 所有文档已是最新")

    return 0


if __name__ == "__main__":
    sys.exit(main())
