#!/bin/bash
# kb-query-search.sh — Search wiki pages for Query operations
# Usage: bash kb-query-search.sh "search terms" [--vault NAME] [--limit N] [--context]
#
# Uses Obsidian CLI search when available, falls back to grep.
# Returns wiki page matches with optional context and backlink counts.

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/kb-common.sh"

# Defaults
LIMIT=20
SHOW_CONTEXT=false
QUERY=""

# Parse arguments
parse_vault_arg "$@"
set -- ${PARSED_ARGS[@]+"${PARSED_ARGS[@]}"}

while [ $# -gt 0 ]; do
    case "$1" in
        --limit)
            LIMIT="$2"
            shift 2
            ;;
        --limit=*)
            LIMIT="${1#--limit=}"
            shift
            ;;
        --context)
            SHOW_CONTEXT=true
            shift
            ;;
        *)
            QUERY="$1"
            shift
            ;;
    esac
done

if [ -z "$QUERY" ]; then
    echo "Usage: bash kb-query-search.sh \"search terms\" [--limit N] [--context]" >&2
    exit 1
fi

resolve_vault
VA=$(_get_vault_prefix)

# --- Search ---

if obsidian_available; then
    if [ "$SHOW_CONTEXT" = true ]; then
        # Context search with grep-style output
        results=$(obsidian_cmd $VA search:context query="$QUERY" limit="$LIMIT" 2>/dev/null || true)
        # Filter to wiki/ paths only
        if [ -n "$results" ]; then
            echo "$results" | awk '/^wiki\// {print}' || true
        fi
    else
        # Path-only search
        results=$(obsidian_cmd $VA search query="$QUERY" format=paths 2>/dev/null || true)
        if [ -n "$results" ]; then
            wiki_results=$(echo "$results" | grep "^wiki/" || true)
            if [ -n "$wiki_results" ]; then
                echo "$wiki_results" | head -"$LIMIT"
            fi
        fi
    fi

    # Show backlinks for each result (only in path mode without context)
    if [ "$SHOW_CONTEXT" = false ] && [ -n "${wiki_results:-}" ]; then
        echo ""
        echo "--- Backlink counts ---"
        echo "$wiki_results" | head -"$LIMIT" | while IFS= read -r f; do
            [ -z "$f" ] && continue
            bl=$(obsidian_cmd $VA backlinks file="$f" 2>/dev/null | grep -c "." || echo "0")
            pt=$(obsidian_cmd $VA property:read file="$f" name="type" 2>/dev/null | grep -v "^Error" | tr -d ' "' | head -1 || true)
            [ -z "$pt" ] && pt="unknown"
            printf "%s\tbacklinks\t%s\t%s\n" "$bl" "$pt" "$f"
        done
    fi
else
    # Fallback: grep search
    echo "# Fallback mode: using grep (install Obsidian CLI for enhanced search)" >&2
    if [ "$SHOW_CONTEXT" = true ]; then
        grep -rn "$QUERY" wiki/ --include="*.md" | head -"$LIMIT" || true
    else
        grep -rl "$QUERY" wiki/ --include="*.md" | head -"$LIMIT" || true
    fi
fi
