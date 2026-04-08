#!/bin/bash
# pre-tool.sh - Log tool usage before execution
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WORKING_DIR="$SKILL_DIR/memory/working"
mkdir -p "$WORKING_DIR"

TOOL_NAME="${1:-unknown}"
TOOL_INPUT="${2:-}"

SESSION_FILE="$WORKING_DIR/current_session.json"

# Initialize or update session file
if [ ! -f "$SESSION_FILE" ]; then
  cat > "$SESSION_FILE" << EOF
{
  "start_time": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "tool_calls": [],
  "errors": []
}
EOF
fi

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] pre-tool: $TOOL_NAME" >> "$WORKING_DIR/tool_log.txt"
