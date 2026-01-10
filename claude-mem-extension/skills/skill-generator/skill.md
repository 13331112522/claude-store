---
name: skill-generator
description: Generate reusable skills from your conversation history
version: 1.0.0
---

# Skill Generator

Generate reusable skills from your conversation history stored in claude-mem.

## When to Use

Use this skill when the user wants to:
- Capture patterns from successful debugging sessions
- Document best practices they've discovered
- Create reusable knowledge from their problem-solving history
- Build a personal knowledge base from their work

## Workflow

Follow this exact workflow when invoked:

### Step 1: Ask User What to Search

Ask the user what they want to search for:

```
Let's find patterns from your history. What would you like to search for?

1. Recent bug fixes
2. High-work features (lots of investment)
3. All observations from past week
4. Custom search query
```

### Step 2: Search for Observations

Based on user's choice, use the `search` MCP tool:

- **Bug fixes**: `search(query="bug fix error fix", type="observations", obs_type="bugfix", limit=30, project="ralph-wiggum")`
- **High-work features**: `search(query="", type="observations", obs_type="feature", limit=30, project="ralph-wiggum")` then sort by work_tokens
- **Past week**: `search(type="observations", dateStart="2026-01-02", limit=30, project="ralph-wiggum")`
- **Custom**: Use their query

### Step 3: Score and Present Candidates

From the search results, calculate scores for each candidate:

**Score Formula:**
```
score = (work_tokens / 1000) + type_weight

Type weights:
- bugfix: 2.0
- decision: 1.8
- feature: 1.5
- discovery: 1.2
- change: 1.0
```

Present top 5-10 candidates:

```
Found X candidates. Top 5:

[1] 🔴/🟣/✅ Title (Score: X.X)
    Brief description from title

[2] ...
```

### Step 4: User Selection

Ask user to select:

```
Select candidates to convert to skills (comma-separated numbers, or 'all'):
```

### Step 5: Fetch Full Observations

For selected IDs, use `get_observations`:

```
get_observations(ids=[123, 456, 789], project="ralph-wiggum")
```

### Step 6: Generate Skills

For each observation, generate a skill file:

**Skill Structure:**

```markdown
---
name: descriptive-name
description: One-line description
version: 1.0.0
generated: YYYY-MM-DDTHH:MM:SSZ
confidence: 0.0-1.0
tags: [tag1, tag2, tag3]
type: bugfix|feature|decision|discovery|change
source:
  sessions: [S1]
  observations: [123]
  project: ralph-wiggum
usage_count: 0
last_used: never
---

# Title

Brief description of when to use this.

## When to Use

[Conditions]

## How It Works

[Steps]

## Example

[Code if applicable]
```

**Generate content based on observation type:**

- **Bugfix**: Problem → Solution → Prevention
- **Feature**: Goal → Approach → Usage
- **Decision**: Context → Options → Rationale
- **Discovery**: Finding → Implications → Applications
- **Change**: Before → After → Migration

### Step 7: Interactive Review

For each skill:

```
[Skill 1/X] Generated: descriptive-name

--- Preview ---
[first 20 lines of skill]
---

Save this skill? (yes/no/edit/skip)
```

- **yes**: Save to `~/.claude/skills/experiences/{name}.md`
- **no**: Skip
- **edit**: Ask what to change
- **skip**: Move to next

### Step 8: Save Approved Skills

For approved skills:

1. Create directory: `mkdir -p ~/.claude/skills/experiences`
2. Write file: `~/.claude/skills/experiences/{name}.md`
3. Confirm: `✅ Saved to ~/.claude/skills/experiences/{name}.md`

## Output Directory

Skills are saved to: `~/.claude/skills/experiences/` (global Claude skills directory)

## Important Notes

- **Always use `get_observations` for 2+ observations** (batch is faster)
- **Create directory if it doesn't exist**
- **Generate descriptive names** (kebab-case)
- **Include source metadata** for traceability
- **Calculate confidence** based on work_tokens (more = higher confidence)
