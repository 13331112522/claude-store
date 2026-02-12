# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Claude Code skill** named `paper-to-blog` that transforms academic research papers (PDFs) into comprehensive, in-depth blog articles (~2000 words) written in Chinese using a **multi-agent architecture**.

## Skill Structure

```
paper-to-blog/
├── SKILL.md                              # Main skill definition with multi-agent workflow
├── agents/                               # Agent specifications
│   ├── parser.md
│   ├── blog-generator.md
│   ├── figure-extractor.md
│   ├── cover-designer.md
│   ├── integrator.md
│   └── master.md
├── lib/
│   └── coordinator.js                    # Orchestration logic (reference)
├── references/
│   └── blog-writer-instructions.md       # Legacy writing guidelines
└── docs/plans/
    └── 2026-01-17-multi-agent-*.md       # Design and implementation docs
```

## Multi-Agent Architecture

The skill uses **6 specialized agents** with parallel execution:

1. **Parser Agent**: PDF → markdown via `mcp__web_reader__webReader`
2. **Blog Generator Agent**: Creates Chinese blog (~2000 words) with custom Medium-style prompt
3. **Figure Extractor Agent**: OCR + AI vision (`mcp__4_5v_mcp__analyze_image`) for figure/table extraction
4. **Cover Designer Agent**: Cartoon infographic generation (16:9, hand-drawn style)
5. **Integrator Agent**: Merges blog + figures + cover
6. **Master Agent**: Quality review (hybrid criteria), coordinates iteration loop

### Execution Flow

```
Parser → (Blog Generator || Figure Extractor || Cover Designer) → Integrator → Master → [1-3 iterations]
```

### Iteration Rules

- **Minimum 1 iteration** (mandatory, even if initially satisfied)
- **Maximum 3 iterations**
- Master provides structured feedback to targeted agents
- Integrator and Master always re-run; others re-run selectively

## Key Constraints

- **Language**: Chinese blog content
- **Length**: ~2000 words
- **Style**: Medium-style, clean, scannable, minimal listicles
- **Figures**: Extract actual visual elements (not full pages) with OCR
- **Cover**: Cartoon infographic, 16:9 aspect ratio

## MCP Tools Used

- `mcp__web_reader__webReader` - PDF to markdown conversion
- `mcp__4_5v_mcp__analyze_image` - Visual analysis for figure extraction

## Output Locations

- Blog articles: `pdf/PaperLog/[title].md`
- Extracted figures: `pdf/PaperLog/figures/`
- Cover: `pdf/PaperLog/figures/cover.png`
- Checkpoints: `pdf/PaperLog/checkpoints/`

## Development

When modifying this skill:
1. Agent specifications are in `agents/` directory
2. Main workflow is in `SKILL.md`
3. Design docs are in `docs/plans/`
4. Test with sample PDFs in `test/fixtures/`
