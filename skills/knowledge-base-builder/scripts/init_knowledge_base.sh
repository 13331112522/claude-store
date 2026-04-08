#!/bin/bash
# init_knowledge_base.sh — Initialize a Karpathy LLM Wiki knowledge base from scratch
# Usage: bash init_knowledge_base.sh <target_directory>
#
# Creates the full directory structure, templates, CLAUDE.md constitution,
# initial log.md, and wiki/index.md for a new knowledge base.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${1:-.}"

if [ "$TARGET" == "." ]; then
    TARGET="$(pwd)"
fi

echo "=== Initializing Karpathy LLM Wiki Knowledge Base ==="
echo "Target: $TARGET"
echo ""

# Create directory structure
echo "Creating directory structure..."
mkdir -p "$TARGET/raw/articles"
mkdir -p "$TARGET/raw/papers"
mkdir -p "$TARGET/raw/transcripts"
mkdir -p "$TARGET/raw/code"
mkdir -p "$TARGET/raw/assets"
mkdir -p "$TARGET/raw/personal"
mkdir -p "$TARGET/wiki/concepts"
mkdir -p "$TARGET/wiki/entities"
mkdir -p "$TARGET/wiki/sources"
mkdir -p "$TARGET/wiki/queries"
mkdir -p "$TARGET/_templates"
mkdir -p "$TARGET/_lint"
mkdir -p "$TARGET/_scripts"

# Copy CLAUDE.md constitution
echo "Creating CLAUDE.md (knowledge base constitution)..."
cp "$SKILL_DIR/assets/CLAUDE.md" "$TARGET/CLAUDE.md"

# Copy template files
echo "Creating page templates..."
cp "$SKILL_DIR/assets/concept.md" "$TARGET/_templates/concept.md"
cp "$SKILL_DIR/assets/entity.md" "$TARGET/_templates/entity.md"
cp "$SKILL_DIR/assets/source_summary.md" "$TARGET/_templates/source_summary.md"

# Create initial log.md
TODAY=$(date +%Y-%m-%d)
echo "Creating log.md..."
cat > "$TARGET/log.md" << EOF
# 知识库操作日志

本文件记录知识库的所有操作历史，只追加不修改。

---

## [$TODAY] init | 知识库初始化
- 创建完整目录结构：raw/, wiki/, _templates/, _lint/, _scripts/
- 初始化CLAUDE.md知识库宪法
- 创建页面模板：concept.md, entity.md, source_summary.md
- 初始化wiki/index.md总目录
- 初始化log.md操作日志

---
EOF

# Create initial wiki/index.md
echo "Creating wiki/index.md..."
cat > "$TARGET/wiki/index.md" << EOF
# 知识库总目录

> 本文件是知识库的核心导航，所有Ingest/Query操作后必须更新。
> 按分类组织，每个页面附带一句话摘要与双向链接。

---

## 概念页面 (concepts)

<!-- LLM在此处自动维护概念页面列表 -->

## 实体页面 (entities)

<!-- LLM在此处自动维护实体页面列表 -->

## 资料摘要 (sources)

<!-- LLM在此处自动维护资料摘要页面列表 -->

## 高价值查询归档 (queries)

<!-- LLM在此处自动维护查询归档页面列表 -->

---

*最后更新：$TODAY | 总页面数：0*
EOF

# Create .gitkeep files in empty dirs to ensure they're tracked
touch "$TARGET/raw/articles/.gitkeep"
touch "$TARGET/raw/papers/.gitkeep"
touch "$TARGET/raw/transcripts/.gitkeep"
touch "$TARGET/raw/code/.gitkeep"
touch "$TARGET/raw/assets/.gitkeep"
touch "$TARGET/raw/personal/.gitkeep"
touch "$TARGET/wiki/concepts/.gitkeep"
touch "$TARGET/wiki/entities/.gitkeep"
touch "$TARGET/wiki/sources/.gitkeep"
touch "$TARGET/wiki/queries/.gitkeep"
touch "$TARGET/_lint/.gitkeep"
touch "$TARGET/_scripts/.gitkeep"

echo ""
echo "=== Knowledge Base Initialized Successfully ==="
echo ""
echo "Directory structure created:"
echo "  $TARGET/"
echo "  ├── raw/            (read-only source material)"
echo "  │   ├── articles/"
echo "  │   ├── papers/"
echo "  │   ├── transcripts/"
echo "  │   ├── code/"
echo "  │   ├── assets/"
echo "  │   └── personal/"
echo "  ├── wiki/           (LLM-compiled knowledge)"
echo "  │   ├── concepts/"
echo "  │   ├── entities/"
echo "  │   ├── sources/"
echo "  │   ├── queries/"
echo "  │   └── index.md"
echo "  ├── _templates/     (page templates)"
echo "  ├── _lint/          (health check reports)"
echo "  ├── _scripts/       (automation scripts)"
echo "  ├── log.md          (append-only operation log)"
echo "  └── CLAUDE.md       (knowledge base constitution)"
echo ""
echo "Next steps:"
echo "  1. Open this directory as an Obsidian vault"
echo "  2. Add source materials to raw/ subdirectories"
echo "  3. Start Claude Code in this directory (it auto-reads CLAUDE.md)"
echo "  4. Issue 'ingest' command to compile knowledge"

# --- Obsidian CLI Enhanced Mode Detection ---
echo ""
echo "--- Checking Obsidian CLI ---"

if command -v obsidian >/dev/null 2>&1 && obsidian version >/dev/null 2>&1; then
    CLI_VERSION=$(obsidian version 2>/dev/null | head -1 || echo "unknown")
    echo "Obsidian CLI found: $CLI_VERSION"

    # Copy operational scripts to _scripts/
    if [ -d "$SKILL_DIR/scripts" ]; then
        for script in kb-common.sh kb-ingest-scan.sh kb-query-search.sh kb-lint.sh kb-stats.sh; do
            if [ -f "$SKILL_DIR/scripts/$script" ]; then
                cp "$SKILL_DIR/scripts/$script" "$TARGET/_scripts/"
                chmod +x "$TARGET/_scripts/$script"
            fi
        done
        echo "Operational scripts deployed to _scripts/"
    fi

    # Check if target is already registered as an Obsidian vault
    VAULT_INFO=$(obsidian vault 2>/dev/null || echo "")
    VAULT_PATH=$(echo "$VAULT_INFO" | grep -i "path" | head -1 | sed 's/.*: *//' | tr -d '"' | xargs || echo "")

    if [ "$VAULT_PATH" = "$TARGET" ]; then
        echo "Vault is registered and active — Enhanced Mode: ENABLED"
    else
        echo "Note: This directory may not be the active Obsidian vault."
        echo "  If using multiple vaults, pass --vault VaultName to scripts."
        echo "  Enhanced Mode: ENABLED (with vault detection)"
    fi
else
    echo "Obsidian CLI not found."
    echo "  Install Obsidian 1.12.4+ and enable CLI in Settings > General."
    echo "  Scripts will use direct file I/O as fallback."
    echo "  Enhanced Mode: DISABLED (fallback mode)"

    # Still copy scripts for future use
    if [ -d "$SKILL_DIR/scripts" ]; then
        for script in kb-common.sh kb-ingest-scan.sh kb-query-search.sh kb-lint.sh kb-stats.sh; do
            if [ -f "$SKILL_DIR/scripts/$script" ]; then
                cp "$SKILL_DIR/scripts/$script" "$TARGET/_scripts/"
                chmod +x "$TARGET/_scripts/$script"
            fi
        done
        echo "Operational scripts deployed to _scripts/ (will use fallback mode)"
    fi
fi
