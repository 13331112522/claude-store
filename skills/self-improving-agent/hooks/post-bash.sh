#!/bin/bash
# post-bash.sh - Capture error context after Bash execution
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WORKING_DIR="$SKILL_DIR/memory/working"
mkdir -p "$WORKING_DIR"

TOOL_OUTPUT="${1:-}"
EXIT_CODE="${2:-0}"

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] post-bash exit=$EXIT_CODE" >> "$WORKING_DIR/tool_log.txt"

# If error, save context for self-correction
if [ "$EXIT_CODE" != "0" ]; then
  cat > "$WORKING_DIR/last_error.json" << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "exit_code": $EXIT_CODE,
  "output": $(echo "$TOOL_OUTPUT" | head -100 | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))' 2>/dev/null || '"(unable to capture)"')
}
EOF
fi
