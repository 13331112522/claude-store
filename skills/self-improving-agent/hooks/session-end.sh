#!/bin/bash
# session-end.sh - Mark session end
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WORKING_DIR="$SKILL_DIR/memory/working"
mkdir -p "$WORKING_DIR"

cat > "$WORKING_DIR/session_end.json" << EOF
{
  "end_time": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "status": "completed"
}
EOF

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] session ended" >> "$WORKING_DIR/tool_log.txt"
