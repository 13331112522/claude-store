#!/bin/bash
# kb-common.sh — Shared library for knowledge base scripts
# Source this file: source "$(dirname "$0")/kb-common.sh"
#
# Provides: CLI detection, vault resolution, stderr suppression, log appending

# --- CLI Detection ---

_OBSIDIAN_AVAILABLE=""
_obsidian_checked=false

obsidian_available() {
    if [ "$_obsidian_checked" = true ]; then
        [ "$_OBSIDIAN_AVAILABLE" = "yes" ]
        return
    fi
    _obsidian_checked=true
    if command -v obsidian >/dev/null 2>&1 && obsidian version >/dev/null 2>&1; then
        _OBSIDIAN_AVAILABLE="yes"
        return 0
    else
        _OBSIDIAN_AVAILABLE="no"
        return 1
    fi
}

# --- CLI Command Wrapper (suppresses stderr noise) ---

obsidian_cmd() {
    local stderr_file
    stderr_file="/tmp/obsidian-stderr-$$.txt"
    local result
    if result=$(obsidian "$@" 2>"$stderr_file"); then
        # Filter out loading noise from stdout
        echo "$result" | grep -v "^20[0-9][0-9]-" | grep -v "installer is out of date" | grep -v "Loading updated app"
        rm -f "$stderr_file"
        return 0
    fi
    # Command failed — show real errors, suppress known noise
    if [ -f "$stderr_file" ]; then
        grep -v "installer out of date" "$stderr_file" >&2 2>/dev/null || true
        rm -f "$stderr_file"
    fi
    return 1
}

# --- Vault Resolution ---

_VAULT_ARG=""
_VAULT_RESOLVED=false

# Set vault name explicitly
set_vault() {
    _VAULT_ARG="vault=\"$1\""
    _VAULT_RESOLVED=true
}

# Auto-detect vault: if PWD matches the active vault path, no prefix needed
resolve_vault() {
    if [ "$_VAULT_RESOLVED" = true ]; then
        return
    fi
    _VAULT_RESOLVED=true
    if ! obsidian_available; then
        _VAULT_ARG=""
        return
    fi
    local vault_info
    if vault_info=$(obsidian_cmd vault 2>/dev/null); then
        local vault_path
        # Output is tab-separated: "path\t/actual/path" — extract the path value
        vault_path=$(echo "$vault_info" | grep "^path" | head -1 | awk -F'\t' '{print $2}' | tr -d '"' | xargs)
        if [ -n "$vault_path" ] && [ "$(cd "$vault_path" 2>/dev/null && pwd)" = "$(pwd)" ]; then
            _VAULT_ARG=""
        else
            # PWD doesn't match active vault — user must specify --vault
            _VAULT_ARG=""
        fi
    fi
}

get_vault_arg() {
    echo "$_VAULT_ARG"
}

# Parse --vault NAME from arguments, remove it from ARGV
parse_vault_arg() {
    PARSED_ARGS=()
    while [ $# -gt 0 ]; do
        case "$1" in
            --vault)
                shift
                set_vault "$1"
                ;;
            --vault=*)
                set_vault "${1#--vault=}"
                ;;
            *)
                PARSED_ARGS+=("$1")
                ;;
        esac
        shift
    done
}

# --- Log Entry (append-only) ---

log_entry() {
    local content="$1"
    if obsidian_available; then
        obsidian_cmd $(_get_vault_prefix) append file="log.md" content="$content" >/dev/null 2>&1
    else
        echo "$content" >> "$(pwd)/log.md"
    fi
}

_get_vault_prefix() {
    echo $_VAULT_ARG
}

# --- File Listing ---

# List all files in a directory prefix (e.g., "raw/", "wiki/")
list_files() {
    local prefix="$1"
    local ext_filter="${2:-}"
    if obsidian_available; then
        local all_files
        all_files=$(obsidian_cmd $(_get_vault_prefix) files format=paths 2>/dev/null || true)
        if [ -n "$ext_filter" ]; then
            echo "$all_files" | grep "^$prefix" | grep -E "\\.(${ext_filter})$" || true
        else
            echo "$all_files" | grep "^$prefix" || true
        fi
    else
        if [ -n "$ext_filter" ]; then
            find "$prefix" -type f 2>/dev/null | grep -E "\\.(${ext_filter})$" || true
        else
            find "$prefix" -type f 2>/dev/null || true
        fi
    fi
}

# --- Utility ---

# Count lines, return 0 if empty
count_lines() {
    local input
    input=$(cat)
    if [ -z "$input" ]; then
        echo "0"
    else
        echo "$input" | wc -l | tr -d ' '
    fi
}

# Today's date
today() {
    date +%Y-%m-%d
}
