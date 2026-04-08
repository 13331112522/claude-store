#!/bin/bash
# kb-stats.sh — Knowledge base statistics dashboard
# Usage: bash kb-stats.sh [--vault NAME] [--format summary|json|md]
#
# Shows file counts by type, tag distribution, link health, and raw vs wiki breakdown.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/kb-common.sh"

# Defaults
FORMAT="summary"

# Parse arguments
parse_vault_arg "$@"
set -- ${PARSED_ARGS[@]+"${PARSED_ARGS[@]}"}

while [ $# -gt 0 ]; do
    case "$1" in
        --format)
            FORMAT="$2"
            shift 2
            ;;
        --format=*)
            FORMAT="${1#--format=}"
            shift
            ;;
        *)
            echo "Unknown argument: $1" >&2
            exit 1
            ;;
    esac
done

resolve_vault
VA=$(_get_vault_prefix)

# --- Helper: count files matching prefix and extensions ---
count_by_prefix() {
    local prefix="$1"
    local ext_pattern="$2"
    if [ -n "$ALL_FILES" ]; then
        echo "$ALL_FILES" | grep "^$prefix" | grep -E "\\.(${ext_pattern})$" | grep -v '\.gitkeep$' | wc -l | tr -d ' '
    else
        echo "0"
    fi
}

# --- Gather statistics with single file list fetch ---

if obsidian_available; then
    vault_info=$(obsidian_cmd $VA vault 2>/dev/null | grep "^name" | awk -F'\t' '{print $2}' || echo "N/A")
    # Single CLI call — cache all file paths
    ALL_FILES=$(obsidian_cmd $VA files format=paths 2>/dev/null || echo "")
else
    vault_info="N/A (CLI unavailable)"
    ALL_FILES=$(find . -type f -not -path './.obsidian/*' -not -path './.git/*' -not -name '.gitkeep' 2>/dev/null | sed 's|^\./||' || echo "")
fi

# Raw files
raw_md=$(count_by_prefix "raw/" "md")
raw_txt=$(count_by_prefix "raw/" "txt")
raw_total=$((raw_md + raw_txt))

# Raw subdirectory breakdown
raw_articles=$(count_by_prefix "raw/articles/" "md|txt")
raw_papers=$(count_by_prefix "raw/papers/" "md|txt")
raw_transcripts=$(count_by_prefix "raw/transcripts/" "md|txt")
raw_code=$(count_by_prefix "raw/code/" "md|txt")
raw_personal=$(count_by_prefix "raw/personal/" "md|txt")

# Wiki pages
wiki_concepts=$(count_by_prefix "wiki/concepts/" "md")
wiki_entities=$(count_by_prefix "wiki/entities/" "md")
wiki_sources=$(count_by_prefix "wiki/sources/" "md")
wiki_queries=$(count_by_prefix "wiki/queries/" "md")
wiki_total=$((wiki_concepts + wiki_entities + wiki_sources + wiki_queries))

# Total
total_files=$(echo "$ALL_FILES" | grep -v '^$' | wc -l | tr -d ' ')

# Link health (CLI only)
unresolved_count=0
orphan_count=0
deadend_count=0
tag_count=0

if obsidian_available; then
    unresolved_count=$(obsidian_cmd $VA unresolved 2>/dev/null | grep -c '.' || echo "0")
    orphan_result=$(obsidian_cmd $VA orphans 2>/dev/null || true)
    orphan_count=$(echo "$orphan_result" | grep -c "^wiki/" 2>/dev/null || echo "0")
    deadend_result=$(obsidian_cmd $VA deadends 2>/dev/null || true)
    deadend_count=$(echo "$deadend_result" | grep "^wiki/" | grep -vc "wiki/index.md" 2>/dev/null || echo "0")
    tag_output=$(obsidian_cmd $VA tags 2>/dev/null || true)
    tag_count=$(echo "$tag_output" | grep -c '.' 2>/dev/null || echo "0")
fi

# Compile ratio
if [ "$raw_total" -gt 0 ] && command -v bc >/dev/null 2>&1; then
    compile_ratio=$(echo "scale=1; $wiki_sources * 100 / $raw_total" | bc 2>/dev/null || echo "0")
else
    compile_ratio="N/A"
fi

# --- Output ---

case "$FORMAT" in
    summary)
        echo "=== Knowledge Base Statistics ==="
        echo ""
        echo "Vault: $vault_info"
        echo "Mode: $(obsidian_available && echo "Obsidian CLI" || echo "Direct File I/O")"
        echo ""
        echo "--- Raw Materials ---"
        echo "  Total raw files:    $raw_total"
        echo "    articles:         $raw_articles"
        echo "    papers:           $raw_papers"
        echo "    transcripts:      $raw_transcripts"
        echo "    code:             $raw_code"
        echo "    personal:         $raw_personal"
        echo ""
        echo "--- Compiled Knowledge ---"
        echo "  Total wiki pages:   $wiki_total"
        echo "    concepts:         $wiki_concepts"
        echo "    entities:         $wiki_entities"
        echo "    source summaries: $wiki_sources"
        echo "    query archives:   $wiki_queries"
        echo ""
        echo "--- Health ---"
        if obsidian_available; then
            echo "  Unresolved links:   $unresolved_count"
            echo "  Orphan wiki pages:  $orphan_count"
            echo "  Dead-end pages:     $deadend_count"
            echo "  Tags in use:        $tag_count"
        else
            echo "  (install Obsidian CLI for link health data)"
        fi
        echo ""
        echo "--- Progress ---"
        echo "  Compile ratio:      ${compile_ratio}% ($wiki_sources / $raw_total raw files have summaries)"
        echo "  Ingest progress:    $wiki_total wiki pages from $raw_total raw files"
        ;;
    json)
        cat << EOF
{
  "vault": $(echo "$vault_info" | head -1 | jq -Rs . 2>/dev/null || echo '"N/A"'),
  "mode": "$(obsidian_available && echo "cli" || echo "fallback")",
  "raw": {
    "total": $raw_total,
    "articles": $raw_articles,
    "papers": $raw_papers,
    "transcripts": $raw_transcripts,
    "code": $raw_code,
    "personal": $raw_personal
  },
  "wiki": {
    "total": $wiki_total,
    "concepts": $wiki_concepts,
    "entities": $wiki_entities,
    "sources": $wiki_sources,
    "queries": $wiki_queries
  },
  "health": {
    "unresolved_links": $unresolved_count,
    "orphan_pages": $orphan_count,
    "deadend_pages": $deadend_count,
    "tags": $tag_count
  },
  "progress": {
    "compile_ratio": "$compile_ratio",
    "raw_files": $raw_total,
    "wiki_pages": $wiki_total
  }
}
EOF
        ;;
    md)
        echo "# Knowledge Base Statistics"
        echo ""
        echo "| Category | Count |"
        echo "|----------|-------|"
        echo "| Raw files (total) | $raw_total |"
        echo "| - articles | $raw_articles |"
        echo "| - papers | $raw_papers |"
        echo "| - transcripts | $raw_transcripts |"
        echo "| - code | $raw_code |"
        echo "| - personal | $raw_personal |"
        echo "| Wiki pages (total) | $wiki_total |"
        echo "| - concepts | $wiki_concepts |"
        echo "| - entities | $wiki_entities |"
        echo "| - source summaries | $wiki_sources |"
        echo "| - query archives | $wiki_queries |"
        if obsidian_available; then
            echo "| Unresolved links | $unresolved_count |"
            echo "| Orphan wiki pages | $orphan_count |"
            echo "| Dead-end pages | $deadend_count |"
            echo "| Tags in use | $tag_count |"
        fi
        echo "| Compile ratio | ${compile_ratio}% |"
        ;;
    *)
        echo "Unknown format: $FORMAT (use summary, json, or md)" >&2
        exit 1
        ;;
esac
