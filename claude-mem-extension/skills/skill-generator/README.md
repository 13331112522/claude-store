# claude-mem skill-generator

> Transform your conversation history into reusable Claude Code skills

Automatically generate standardized skills from your claude-mem stored conversations. Capture patterns from successful debugging sessions, document best practices, and build a personal knowledge base from your problem-solving history.

## Features

- **Smart Pattern Detection** - Automatically identifies valuable patterns from your conversation history
- **Composite Scoring** - Ranks candidates by repetition, success rate, and work investment
- **Interactive Review** - Preview and edit skills before saving
- **Standard Format** - Generates proper Claude Code skill files with metadata
- **Global Installation** - Skills saved to `~/.claude/skills/experiences/` for universal access
- **Usage Tracking** - Built-in metrics to track skill adoption over time

## How It Works

```
Observations → Scorer → Ranked Candidates
                            ↓
                       User Selection
                            ↓
                      Pattern Extraction
                            ↓
                       Skill Building
                            ↓
                    Interactive Review
                            ↓
                        File Writer
                            ↓
                    Index & Changelog
```

### The Pipeline

1. **Searches memory** - Uses mem-search to find relevant observations
2. **Scores candidates** - Ranks by repetition + type weight + work investment
3. **Extracts patterns** - Identifies core problems, solutions, and edge cases
4. **Generates skills** - Creates standard Claude Code skill format with YAML frontmatter
5. **Interactive review** - You approve, edit, or skip each skill
6. **Persists skills** - Saves to global skills directory with metadata

### Scoring Algorithm

```
score = (work_tokens / 1000) + type_weight
```

| Type | Weight | Rationale |
|------|--------|-----------|
| 🔴 bugfix | 2.0 | Highest value - prevents recurring issues |
| ⚖️ decision | 1.8 | Architectural knowledge |
| 🟣 feature | 1.5 | Implementation patterns |
| 🔵 discovery | 1.2 | Learning moments |
| ✅ change | 1.0 | Refactoring knowledge |

## Installation

### Prerequisites

- [claude-mem](https://github.com/thedotmack/claude-mem) installed and configured
- Node.js 20+ and npm (for development only)
- Claude Code environment

### Quick Install

```bash
cd claude-mem-extension/skills/skill-generator
npm install
npm run build
./install.sh
```

### Manual Install

```bash
# 1. Build the project
npm install
npm run build

# 2. Find your claude-mem installation
find ~/.claude/plugins -name "claude-mem" -type d

# 3. Copy the skill file
cp skill.md ~/.claude/plugins/cache/thedotmack/claude-mem/skills/skill-generator.md

# 4. Restart Claude Code
```

## Usage

In Claude Code, invoke the skill:

```
Skill(skill-generator)
```

Follow the interactive prompts:

1. **Select search type**
   - Recent bug fixes
   - High-work features
   - Past week's observations
   - Custom search query

2. **Review candidates** - Top patterns are presented with scores

3. **Select to convert** - Choose which candidates to turn into skills

4. **Interactive review** - Preview each skill and decide to:
   - `yes` - Save to `~/.claude/skills/experiences/`
   - `no` - Skip this skill
   - `edit` - Make changes before saving
   - `skip` - Move to next

## Example

```
You: Skill(skill-generator)

Claude: Let's find patterns from your history. What would you like to search for?

1. Recent bug fixes
2. High-work features (lots of investment)
3. All observations from past week
4. Custom search query

You: 1

Claude: Found 12 candidates. Top 5:

[1] 🔴 Fixed observation iteration error (Score: 3.2)
    Debugged TypeScript iteration bug in skill generator

[2] 🔴 Resolved function signature mismatch (Score: 2.8)
    Fixed parameter type mismatch in MCP tool wrapper

[3] 🟣 Implemented skill generation orchestrator (Score: 2.4)
    Built core pipeline for skill generation

...

Select candidates to convert to skills (comma-separated numbers, or 'all'):

You: 1,2

Claude: [Skill 1/2] Generated: observation-iteration-debugging

--- Preview ---
# Observation Iteration Debugging

## When to Use
- Encountering "for...of" iteration errors on observations
- Debugging TypeScript iteration over MCP query results
- Objects lack expected properties during iteration

## How It Works
...

---

Save this skill? (yes/no/edit/skip)

You: yes

Claude: ✅ Saved to ~/.claude/skills/experiences/observation-iteration-debugging.md
```

## Generated Skill Format

Skills are saved with comprehensive metadata:

```markdown
---
name: observation-iteration-debugging
description: Debug TypeScript iteration errors over observation arrays
version: 1.0.0
generated: 2026-01-09T20:40:00Z
confidence: 0.85
tags: [debugging, typescript, iteration, mcp]
type: bugfix
source:
  sessions: [S99]
  observations: [929]
  project: ralph-wiggum
usage_count: 0
last_used: never
---

# Observation Iteration Debugging

## When to Use
- Encountering "for...of" iteration errors on observations
- Debugging TypeScript iteration over MCP query results
- Objects lack expected properties during iteration

## How It Works
...

## Example
...
```

## Architecture

```
claude-mem-extension/skills/skill-generator/
├── src/                    # TypeScript source
│   ├── index.ts           # Main orchestrator
│   ├── types.ts           # Type definitions
│   ├── scorer.ts          # Candidate scoring
│   ├── extractor.ts       # Pattern extraction
│   ├── builder.ts         # Markdown generation
│   ├── writer.ts          # File I/O and indexing
│   └── mcp-tools.ts       # MCP tool wrappers
├── tests/                 # Comprehensive test suite
│   ├── scorer.test.ts
│   ├── extractor.test.ts
│   ├── builder.test.ts
│   ├── writer.test.ts
│   ├── mcp-tools.test.ts
│   └── integration.test.ts
├── dist/                  # Compiled JavaScript
├── skill.md              # Claude Code skill definition
└── package.json          # Project config
```

### Components

| Component | Purpose |
|-----------|---------|
| **Scorer** | Composite scoring algorithm for ranking candidates |
| **Extractor** | Analyzes observations to extract patterns and structure |
| **Builder** | Generates standardized Claude Code skill format |
| **Writer** | Handles file persistence, indexing, and changelog |
| **MCP Tools** | Wrappers for claude-mem integration |

## Development

```bash
# Install dependencies
npm install

# Run tests
npm test

# Build TypeScript
npm run build

# Watch mode for development
npm run watch
```

## Output Directory

Generated skills are saved to: `~/.claude/skills/experiences/`

This global location makes skills available across all Claude Code projects.

### Directory Structure

```
~/.claude/skills/experiences/
├── {skill-name}.md          # Generated skills
├── .index.json              # Skills registry
├── .changelog.md            # Learning log
└── .metadata/
    └── {skill-name}.json    # Usage tracking
```

## Extension Points

Extend the skill-generator by modifying:

- **`src/scorer.ts`** - Custom scoring algorithms
- **`src/extractor.ts`** - New pattern extraction rules
- **`src/builder.ts`** - Custom skill formats
- **`src/writer.ts`** - Alternative storage backends

## Requirements

- **Runtime**: None (zero runtime dependencies)
- **Development**: Node.js 20+, TypeScript 5.9+, Jest 29+
- **External**: claude-mem plugin, Claude Code environment

## License

MIT

## Related

- [claude-mem](https://github.com/thedotmack/claude-mem) - Persistent memory for Claude Code
- [Ralph Wiggum](https://github.com/...) - Project this was developed for
