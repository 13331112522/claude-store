#!/bin/bash
# kb-ingest-scan.sh — Scan raw/ for unprocessed files
# Usage: bash kb-ingest-scan.sh [--vault NAME] [--format paths|json|summary] [--dir raw/subdir]
#
# Compares raw/ file list against log.md ingest records to identify
# files that haven't been compiled into wiki pages yet.

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/kb-common.sh"

# Defaults
FORMAT="paths"
SCAN_DIR="raw"

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
        --dir)
            SCAN_DIR="$2"
            shift 2
            ;;
        --dir=*)
            SCAN_DIR="${1#--dir=}"
            shift
            ;;
        *)
            echo "Unknown argument: $1" >&2
            exit 1
            ;;
    esac
done

resolve_vault

# --- Step 1: Get all raw files ---

raw_files=$(list_files "$SCAN_DIR" "md|txt" | grep -v '\.gitkeep$' || true)

if [ -z "$raw_files" ]; then
    echo "# No files found in $SCAN_DIR" >&2
    exit 0
fi

# --- Step 2: Get already-processed files from log.md ---

processed_patterns=""
if obsidian_available; then
    log_content=$(obsidian_cmd $(_get_vault_prefix) read file="log.md" 2>/dev/null || echo "")
else
    log_content=$(cat log.md 2>/dev/null || echo "")
fi

# Extract filenames mentioned in ingest log entries
# Look for patterns like file references in log entries
processed_files=$(echo "$log_content" | \
    grep -oE '[a-zA-Z0-9_./\-]+\.(md|txt)' | \
    grep "^raw/" | \
    sort -u || true)

# --- Step 3: Diff — find unprocessed ---

if [ -n "$processed_files" ]; then
    unprocessed=$(comm -23 <(echo "$raw_files" | sort) <(echo "$processed_files" | sort))
else
    unprocessed="$raw_files"
fi

# --- Step 4: Output ---

case "$FORMAT" in
    paths)
        if [ -n "$unprocessed" ]; then
            echo "$unprocessed"
        fi
        ;;
    json)
        echo "["
        first=true
        while IFS= read -r f; do
            [ -z "$f" ] && continue
            fname=$(basename "$f")
            fdir=$(dirname "$f" | sed "s|^${SCAN_DIR}/\?||")
            fext="${fname##*.}"
            if [ "$first" = true ]; then
                first=false
            else
                echo ","
            fi
            printf '  {"path":"%s","name":"%s","ext":"%s","dir":"%s"}' "$f" "$fname" "$fext" "$fdir"
        done <<< "$unprocessed"
        echo ""
        echo "]"
        ;;
    summary)
        total_raw=$(echo "$raw_files" | count_lines)
        total_unprocessed=$(echo "$unprocessed" | count_lines)
        total_processed=$((total_raw - total_unprocessed))

        echo "=== Ingest Scan Summary ==="
        echo "Directory: $SCAN_DIR"
        echo "Total files: $total_raw"
        echo "Already processed: $total_processed"
        echo "Unprocessed: $total_unprocessed"
        echo ""
        echo "--- Breakdown by subdirectory ---"

        # Count by subdirectory
        echo "$unprocessed" | while IFS= read -r f; do
            [ -z "$f" ] && continue
            dirname "$f" | sed "s|^${SCAN_DIR}/\?||" | sed 's/^$/root/'
        done | sort | uniq -c | sort -rn

        echo ""
        echo "--- File extension breakdown ---"
        echo "$unprocessed" | while IFS= read -r f; do
            [ -z "$f" ] && continue
            echo "${f##*.}"
        done | sort | uniq -c | sort -rn

        echo ""
        if [ "$total_unprocessed" -gt 0 ]; then
            echo "# Run: bash kb-ingest-scan.sh --format paths --dir $SCAN_DIR | head -N"
            echo "# to get the first N files to process."
        fi
        ;;
    *)
        echo "Unknown format: $FORMAT (use paths, json, or summary)" >&2
        exit 1
        ;;
esac
