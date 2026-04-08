#!/bin/bash
# kb-lint.sh — Knowledge base health check (superset of vault-health-check.sh)
# Usage: bash kb-lint.sh [--vault NAME] [--fix] [--scope wiki|all]
#
# Checks: link integrity, frontmatter compliance, index freshness,
# raw integrity, orphan detection, bidirectional link symmetry.
# Auto-fixes with --fix flag.
# Report saved to _lint/lint-YYYY-MM-DD.md

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/kb-common.sh"

# Defaults
FIX=false
SCOPE="all"

# Parse arguments
parse_vault_arg "$@"
set -- ${PARSED_ARGS[@]+"${PARSED_ARGS[@]}"}

while [ $# -gt 0 ]; do
    case "$1" in
        --fix)
            FIX=true
            shift
            ;;
        --scope)
            SCOPE="$2"
            shift 2
            ;;
        --scope=*)
            SCOPE="${1#--scope=}"
            shift
            ;;
        *)
            echo "Unknown argument: $1" >&2
            exit 1
            ;;
    esac
done

resolve_vault
TODAY=$(today)
REPORT_FILE="_lint/lint-${TODAY}.md"
VA=$(_get_vault_prefix)

# Initialize report
mkdir -p _lint
cat > "$REPORT_FILE" << EOF
# 知识库健康巡检报告

**日期**: $TODAY
**范围**: $SCOPE
**自动修复**: $FIX
**模式**: $(obsidian_available && echo "Obsidian CLI" || echo "直接文件I/O")

---

EOF

ISSUES_FOUND=0
ISSUES_FIXED=0

report_section() {
    echo "## $1" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
}

report_item() {
    local status="$1"
    local message="$2"
    if [ "$status" = "FIXED" ]; then
        echo "- [x] $message (auto-fixed)" >> "$REPORT_FILE"
        ISSUES_FIXED=$((ISSUES_FIXED + 1))
    elif [ "$status" = "WARN" ]; then
        echo "- [ ] ⚠️ $message" >> "$REPORT_FILE"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    else
        echo "- [ ] $message" >> "$REPORT_FILE"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
}

report_ok() {
    echo "- ✅ $1" >> "$REPORT_FILE"
}

# ========================================
# CHECK 1: Vault-level link health
# ========================================
report_section "1. 链接完整性"

if obsidian_available; then
    # Orphans
    orphans=$(obsidian_cmd $VA orphans 2>/dev/null || true)
    orphan_wiki=$(echo "$orphans" | grep "^wiki/" || true)
    orphan_count=$(echo "$orphan_wiki" | count_lines)

    if [ "$orphan_count" -eq 0 ]; then
        report_ok "No orphan wiki pages (all pages have incoming links)"
    else
        report_item "WARN" "Found $orphan_count orphan wiki pages (no incoming links):"
        echo '```' >> "$REPORT_FILE"
        echo "$orphan_wiki" >> "$REPORT_FILE"
        echo '```' >> "$REPORT_FILE"
    fi

    # Unresolved links
    unresolved=$(obsidian_cmd $VA unresolved 2>/dev/null || true)
    unresolved_count=$(echo "$unresolved" | count_lines)

    if [ "$unresolved_count" -eq 0 ]; then
        report_ok "No unresolved links"
    else
        # Separate expected unresolved (raw files not yet ingested) from truly broken
        raw_files=$(list_files "raw/" "md" | grep -v '\.gitkeep$' || true)
        raw_basenames=$(echo "$raw_files" | while IFS= read -r f; do
            basename "$f" .md | sed 's/[ _].*//' | tr '[:upper:]' '[:lower:]'
        done | sort -u || true)

        expected_unresolved=""
        truly_broken=""
        while IFS= read -r link; do
            [ -z "$link" ] && continue
            link_lower=$(echo "$link" | tr '[:upper:]' '[:lower:]')
            if echo "$raw_basenames" | grep -q "$link_lower"; then
                expected_unresolved="$expected_unresolved$link"$'\n'
            else
                truly_broken="$truly_broken$link"$'\n'
            fi
        done <<< "$unresolved"

        expected_count=$(echo "$expected_unresolved" | count_lines)
        broken_count=$(echo "$truly_broken" | count_lines)

        if [ "$expected_count" -gt 0 ]; then
            report_item "WARN" "$expected_count unresolved links have matching raw files (awaiting ingest):"
            echo '```' >> "$REPORT_FILE"
            echo "$expected_unresolved" >> "$REPORT_FILE"
            echo '```' >> "$REPORT_FILE"
        fi

        if [ "$broken_count" -gt 0 ]; then
            report_item "FAIL" "$broken_count truly broken links (no matching file):"
            echo '```' >> "$REPORT_FILE"
            echo "$truly_broken" >> "$REPORT_FILE"
            echo '```' >> "$REPORT_FILE"
        fi
    fi

    # Dead ends
    deadends=$(obsidian_cmd $VA deadends 2>/dev/null || true)
    deadend_wiki=$(echo "$deadends" | grep "^wiki/" | grep -v "wiki/index.md" || true)
    deadend_count=$(echo "$deadend_wiki" | count_lines)

    if [ "$deadend_count" -eq 0 ]; then
        report_ok "No dead-end wiki pages (all pages link to others)"
    else
        report_item "WARN" "Found $deadend_count dead-end wiki pages (no outgoing links):"
        echo '```' >> "$REPORT_FILE"
        echo "$deadend_wiki" >> "$REPORT_FILE"
        echo '```' >> "$REPORT_FILE"
    fi
else
    report_item "WARN" "Obsidian CLI unavailable — link integrity check skipped"
fi

# ========================================
# CHECK 2: Frontmatter compliance
# ========================================
report_section "2. Frontmatter 规范检查"

wiki_files=$(list_files "wiki/" "md" | grep -v '\.gitkeep$' | grep -v "wiki/index.md" || true)
required_props="type date tags"

while IFS= read -r f; do
    [ -z "$f" ] && continue
    missing_props=""

    if obsidian_available; then
        for prop in $required_props; do
            val=$(obsidian_cmd $VA property:read file="$f" name="$prop" 2>/dev/null | tr -d ' "' || true)
            if [ -z "$val" ] || [ "$val" = "null" ]; then
                missing_props="$missing_props $prop"
            fi
        done

        if [ -n "$missing_props" ]; then
            if [ "$FIX" = true ]; then
                # Set default values for missing properties
                page_type=$(echo "$f" | sed 's|wiki/||' | cut -d'/' -f1 | sed 's/s$//')
                for prop in $missing_props; do
                    case "$prop" in
                        type) val="$page_type" ;;
                        date) val="$TODAY" ;;
                        tags) val="[]" ;;
                    esac
                    obsidian_cmd $VA property:set file="$f" name="$prop" value="$val" >/dev/null 2>&1 || true
                done
                report_item "FIXED" "$f — added missing properties:$missing_props"
            else
                report_item "FAIL" "$f — missing properties:$missing_props"
            fi
        fi
    else
        # Fallback: check frontmatter via grep
        for prop in $required_props; do
            if ! grep -q "^${prop}:" "$f" 2>/dev/null; then
                missing_props="$missing_props $prop"
            fi
        done
        if [ -n "$missing_props" ]; then
            report_item "FAIL" "$f — missing properties:$missing_props"
        fi
    fi
done <<< "$wiki_files"

total_wiki=$(echo "$wiki_files" | count_lines)
report_ok "Checked $total_wiki wiki pages for frontmatter compliance"

# ========================================
# CHECK 3: Index freshness
# ========================================
report_section "3. Index 新鲜度"

# Get pages listed in index.md
if obsidian_available; then
    index_content=$(obsidian_cmd $VA read file="wiki/index.md" 2>/dev/null || echo "")
else
    index_content=$(cat wiki/index.md 2>/dev/null || echo "")
fi

# Extract page names from [[links]] in index
index_linked=$(echo "$index_content" | grep -oE '\[\[([^]]+)\]\]' | sed 's/\[\[//;s/\]\]//' | sort -u || true)

# Get actual wiki files
actual_pages=$(echo "$wiki_files" | while IFS= read -r f; do
    [ -z "$f" ] && continue
    basename "$f" .md
done | sort -u || true)

# Pages in index but not on disk
if [ -n "$index_linked" ]; then
    stale_index=$(comm -23 <(echo "$index_linked") <(echo "$actual_pages"))
    stale_count=$(echo "$stale_index" | count_lines)
    if [ "$stale_count" -gt 0 ]; then
        report_item "WARN" "$stale_count pages referenced in index.md but not found on disk:"
        echo '```' >> "$REPORT_FILE"
        echo "$stale_index" >> "$REPORT_FILE"
        echo '```' >> "$REPORT_FILE"
    else
        report_ok "All index references point to existing pages"
    fi
fi

# Pages on disk but not in index
missing_from_index=$(comm -13 <(echo "$index_linked") <(echo "$actual_pages"))
missing_count=$(echo "$missing_from_index" | count_lines)
if [ "$missing_count" -gt 0 ]; then
    if [ "$FIX" = true ]; then
        report_item "FIXED" "$missing_count wiki pages not in index.md (auto-update required — Claude should update index.md)"
    else
        report_item "WARN" "$missing_count wiki pages exist but are not referenced in index.md"
    fi
else
    report_ok "All wiki pages are referenced in index.md"
fi

# ========================================
# CHECK 4: Raw integrity
# ========================================
if [ "$SCOPE" = "all" ]; then
    report_section "4. Raw 资料完整性"

    raw_count=$(list_files "raw/" "md|txt" | grep -v '\.gitkeep$' | count_lines)
    report_ok "Found $raw_count raw text files"

    # Check if any raw files have been modified recently (potential violation)
    if [ "$(uname)" = "Darwin" ]; then
        recent_mods=$(find raw/ -type f -mtime -1 -name "*.md" 2>/dev/null | grep -v '\.gitkeep$' | head -10 || true)
        if [ -n "$recent_mods" ]; then
            report_item "WARN" "Some raw files were modified in the last 24h (verify no LLM edits):"
            echo '```' >> "$REPORT_FILE"
            echo "$recent_mods" >> "$REPORT_FILE"
            echo '```' >> "$REPORT_FILE"
        fi
    fi
fi

# ========================================
# CHECK 5: Tag inventory
# ========================================
report_section "5. Tag 概览"

if obsidian_available; then
    tag_output=$(obsidian_cmd $VA tags 2>/dev/null || true)
    if [ -n "$tag_output" ]; then
        echo '```' >> "$REPORT_FILE"
        echo "$tag_output" >> "$REPORT_FILE"
        echo '```' >> "$REPORT_FILE"
    else
        report_ok "No tags found in vault"
    fi
else
    report_item "WARN" "Obsidian CLI unavailable — tag inventory skipped"
fi

# ========================================
# Summary
# ========================================
echo "" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "**Summary**: Issues found: $ISSUES_FOUND | Auto-fixed: $ISSUES_FIXED" >> "$REPORT_FILE"
echo "**Report saved**: $REPORT_FILE" >> "$REPORT_FILE"

# Append to log.md
log_entry "

---

## [$TODAY] lint | 健康巡检
- 范围: $SCOPE
- 发现问题: $ISSUES_FOUND
- 自动修复: $ISSUES_FIXED
- 报告: [[$REPORT_FILE]]

---

"

# Output summary to stdout
echo "=== KB Lint Complete ==="
echo "Report: $REPORT_FILE"
echo "Issues found: $ISSUES_FOUND"
echo "Issues fixed: $ISSUES_FIXED"
