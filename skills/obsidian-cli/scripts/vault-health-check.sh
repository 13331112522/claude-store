#!/bin/bash
# vault-health-check.sh — Obsidian Vault health report
# Usage: bash vault-health-check.sh [vault_name]
#
# Requires: Obsidian CLI enabled and Obsidian running.
# The CLI will auto-launch Obsidian if not running.

set -euo pipefail

VAULT_ARG=""
if [ -n "${1:-}" ]; then
    VAULT_ARG="vault=\"$1\""
fi

echo "=== Obsidian Vault Health Report ==="
echo "Date: $(date)"
echo ""

echo "## File Statistics"
obsidian $VAULT_ARG files | tail -1
echo ""

echo "## Orphan Notes (no incoming links)"
obsidian $VAULT_ARG orphans
echo ""

echo "## Unresolved Links (broken link targets)"
obsidian $VAULT_ARG unresolved
echo ""

echo "## Dead-end Notes (no outgoing links)"
obsidian $VAULT_ARG deadends
echo ""

echo "## Tag Summary"
obsidian $VAULT_ARG tags
echo ""

echo "=== Report Complete ==="
