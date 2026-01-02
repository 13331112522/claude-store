# Year Brief Generator

Generate a comprehensive year-end brief by scanning the Obsidian vault for all work from the specified year.

## How it works

This command:
1. Scans the file system for markdown files created/modified in the target year
2. Analyzes file metadata (dates, sizes, directories)
3. Samples key files to understand content themes
4. Generates a comprehensive year brief covering all work domains
5. Unlike agent-context-based approaches, this provides complete vault coverage

## What to generate

Create a comprehensive year brief document with:

### Structure
1. **Executive Summary**
   - Year overview (2-3 sentences capturing the essence)
   - Key achievements by category (AI research, investment, technical work, etc.)
   - Major metrics (files created, themes, milestones)

2. **Monthly/Quarterly Timeline**
   - Break down work by month or quarter
   - Highlight major works in each period
   - Identify thematic evolution throughout the year

3. **Deep Dive: Core Themes**
   - Group work by major themes (AI research, investment, etc.)
   - For each theme:
     - Key documents/papers
     - Insights developed
     - Evolution of thinking

4. **Quantitative Metrics**
   - Content volume (files by directory)
   - Time distribution (work by month/quarter)
   - Research themes by volume
   - Language distribution (if applicable)

5. **Tool & Workflow Evolution**
   - How workflows changed from early → mid → late year
   - Tools adopted or refined
   - Process improvements

6. **Key Insights & Learnings**
   - Technical insights
   - Domain-specific insights (investment, AI, etc.)
   - Meta-insights about knowledge work

7. **Challenges & Limitations**
   - Technical challenges encountered
   - Workflow bottlenecks
   - Knowledge management issues

8. **Future Directions**
   - Quarterly roadmap for next year
   - Areas to improve
   - Goals to scale

9. **Ultrathinking Section** (Strategic Analysis)
   - What this year really represents
   - Meta-patterns in the work
   - Why it matters for long-term vision

10. **Closing Thoughts**
    - The year as a foundation
    - Meta-skills developed
    - Vision for next year

### File System Scanning Approach

**Do NOT rely solely on agent context or session memories.** Instead:

1. **Survey the vault structure:**
   ```bash
   find "{vault_path}" -maxdepth 2 -type d
   ```

2. **Count files by directory:**
   ```bash
   find "{vault_path}/{dir}" -name "*.md" -type f | wc -l
   ```

3. **Sample key files:**
   - Get file listings with dates
   - Identify largest/most recent files
   - Read first 50 lines of key files to understand themes

4. **Analyze patterns:**
   - What directories have most files?
   - What time periods show highest activity?
   - What themes emerge from file names and content?

5. **Synthesize into narrative:**
   - Connect file system data to story of the year
   - Identify evolution and growth patterns
   - Extract lessons and insights

### Output Format

- Save to: `{vault_path}/{YEAR}_Year_Brief.md`
- Use markdown formatting
- Include tables for metrics
- Use bullet points for readability
- Add horizontal rules to separate major sections

### Coverage

- **Full Year Scan:** January - December of target year
- **All Directories:** Include all major work directories
- **Bilingual Content:** Handle both English and Chinese files
- **All Work Types:** Research, investment, coding, writing, etc.

## Example Output Structure

```markdown
# {YEAR} Year Brief - Comprehensive Overview

**Generated:** {Current Date}
**Coverage Period:** Full Year {YEAR} (January - December)
**Vault Size:** {Total files} files across {N} directories
**Status:** Complete Year Analysis

---

## Executive Summary

{YEAR} was a year of {themes}...

### Key Achievements by Category

**🔬 AI Research & Analysis**
- Papers processed: {N}
- Core themes: {list}

**💼 Investment Philosophy**
- Framework developed: {name}
- Key principles: {list}

...

## Monthly Work Analysis

### Q1 {YEAR} (Jan-Mar): {Theme}

**January {YEAR}**
- Work item 1
- Work item 2

...

## Deep Dive: Core Themes

### 1. {Theme Name}

**Key Documents:**
- Document 1
- Document 2

**Insights:**
- Insight 1
- Insight 2

...

## Quantitative Metrics

### Content Volume
- Total Files: {N}
- By directory: {breakdown}

...

## Ultrathinking: What {YEAR} Really Represents

### The Meta-Pattern: {Pattern Name}

{Deep strategic analysis}

...

## Closing Thoughts

{YEAR} was {summary}...

**The goal:** {vision for next year}
```

## Important Notes

- **Scan the actual file system**, don't just use agent context
- **Sample broadly**: Look at multiple directories and time periods
- **Quantify everything**: Count files, measure sizes, track dates
- **Tell a story**: Connect the data to narrative arcs
- **Be honest about limitations**: What the scan might miss
- **Include Chinese content**: If vault has Chinese documents, include them
- **Ultrathink deeply**: Go beyond surface metrics to strategic insights

## When to use

- At year-end (December/January) to create comprehensive year brief
- When asked for "what did I accomplish this year?"
- When planning next year's work (need to understand this year's foundation)
- When reflecting on growth and evolution over time

## Output

Generate a comprehensive markdown document covering all work in the specified year, saved to the vault root as `{YEAR}_Year_Brief.md`.