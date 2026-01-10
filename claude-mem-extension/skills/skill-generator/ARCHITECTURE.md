# Architecture

## System Overview

The skill generator is a TypeScript module that extends claude-mem with the ability to generate reusable skills from conversation history.

## Components

### 1. Candidate Scorer (\`src/scorer.ts\`)

Implements composite scoring:
- Repetition: How often pattern appears
- Success: Type-weighted (bugfix > discovery)
- Work Investment: Token expenditure

### 2. Pattern Extractor (\`src/extractor.ts\`)

Analyzes observations to extract:
- Core problem
- Solution approach
- Rationale
- Edge cases

Adapts structure based on observation type.

### 3. Skill Builder (\`src/builder.ts\`)

Generates standard Claude Code skill format:
- YAML frontmatter with metadata
- Sectioned content
- Markdown formatting

### 4. File Writer (\`src/writer.ts\`)

Persists skills with:
- Main skill file
- Index (.index.json)
- Changelog (.changelog.md)
- Metadata tracking (.metadata/*.json)

### 5. MCP Tools (\`src/mcp-tools.ts\`)

Wrappers for claude-mem MCP tools:
- search
- timeline
- get_observation
- get_observations

## Data Flow

\`\`\`
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
\`\`\`

## File Structure

\`\`\`
skills/experiences/
├── {skill-name}.md          # Generated skills
├── .index.json              # Skills registry
├── .changelog.md            # Learning log
└── .metadata/
    └── {skill-name}.json    # Usage tracking
\`\`\`

## Extension Points

To extend functionality:

1. **Custom scoring** - Modify \`src/scorer.ts\`
2. **New patterns** - Add to \`src/extractor.ts\`
3. **Formats** - Update \`src/builder.ts\`
4. **Storage** - Extend \`src/writer.ts\`
