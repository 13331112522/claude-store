# Installation Instructions

## Step 1: Build the project

```bash
cd claude-mem-extension/skills/skill-generator
npm install
npm run build
```

## Step 2: Find claude-mem

```bash
find ~/.claude/plugins -name "claude-mem" -type d
```

Common locations:
- `~/.claude/plugins/cache/thedotmack/claude-mem`
- `~/.claude/plugins/marketplaces/claude-mem`

## Step 3: Copy skill file

```bash
# Replace with actual path from step 2
CLAUDE_MEM_DIR="~/.claude/plugins/cache/thedotmack/claude-mem"
cp skill.md "$CLAUDE_MEM_DIR/skills/skill-generator.md"
```

## Step 4: Restart Claude Code

Quit and restart Claude Code to load the new skill.

## Step 5: Test

In Claude Code:
```
Skill(skill-generator)
```

## Troubleshooting

**Skill not found:**
- Verify claude-mem is installed
- Check the skills directory path
- Restart Claude Code

**MCP tools not available:**
- Ensure claude-mem MCP server is running
- Check Claude Code settings for MCP configuration
