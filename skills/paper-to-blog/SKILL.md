---
name: paper-to-blog
description: This skill transforms academic papers (PDFs) into comprehensive 2000-word blog posts using a multi-agent system with parallel execution, OCR-based figure extraction, cover design, and iterative refinement (1-3 iterations). Use when converting research papers into engaging Chinese blog articles with flowing prose and properly extracted figures.
---

# Paper to Blog (Multi-Agent)

## Overview

Transform academic research papers into comprehensive, in-depth blog articles (~2000 words) using a coordinated multi-agent system. The workflow features parallel execution, AI-assisted figure extraction, cover design, and quality-driven iteration.

## When to Use This Skill

Use this skill when:
- User wants to convert a research paper PDF into a comprehensive blog article (~2000 words)
- User mentions "paper to blog", "论文转博客", "make a blog from paper"
- User wants to create an in-depth exploration of academic research in flowing prose
- User wants to generate Chinese blog content from English papers
- User wants detailed technical content with properly extracted figures and cover illustration

## Multi-Agent Architecture

This skill uses **6 specialized agents** with parallel execution:

```
PDF Input
    ↓
[Parser Agent]
    ↓
    ├─→ [Blog Generator Agent] ──┐
    ├─→ [Figure Extractor Agent] ─┤
    └─→ [Cover Designer Agent] ────┤
         ↓                         ↓
    [Integrator Agent] ←───────────┘
         ↓
    [Master Agent] → [Iteration Loop: 1-3 cycles]
         ↓
    Final Output
```

### Agent Responsibilities

1. **Parser Agent**: Converts PDF to markdown using `mcp__web_reader__webReader`
2. **Blog Generator Agent**: Creates Chinese blog post using custom Medium-style prompt
3. **Figure Extractor Agent**: Extracts actual image files using PDF rendering + AI vision (PyMuPDF + `mcp__4_5v_mcp__analyze_image`)
4. **Cover Designer Agent**: Generates cartoon-style illustration via ZhipuAI CogView API
5. **Integrator Agent**: Merges blog, figures, and cover into final markdown
6. **Master Agent**: Quality review with hybrid criteria, coordinates iteration loop

## Workflow

### Step 1: Validate Input

Ensure PDF file exists and is accessible.

**Action:** Verify PDF path, alert user if file not found.

### Step 2: Spawn Parser Agent

Convert PDF to markdown format.

**Action:** Use Task tool with general-purpose agent, provide prompt from `agents/parser.md`

### Step 3: Parallel Execution (Blog Generator, Figure Extractor, Cover Designer)

Execute three agents in parallel for efficiency.

**Action:** Use Task tool with three general-purpose agents in a single message, provide prompts from:
- `agents/blog-generator.md` (includes your custom Medium-style prompt)
- `agents/figure-extractor.md` (OCR + vision analysis)
- `agents/cover-designer.md` (cartoon infographic prompt)

### Step 4: Spawn Integrator Agent

Merge all outputs into integrated markdown.

**Action:** Use Task tool with general-purpose agent, provide prompt from `agents/integrator.md`

### Step 5: Iteration Loop (Minimum 1, Maximum 3)

Spawn Master Agent for review and coordinate refinement cycles.

**Action per iteration:**
1. Use Task tool with general-purpose agent, provide prompt from `agents/master.md`
2. If approved AND iteration >= 1: Proceed to final output
3. If iteration reaches 3: Force approval with issue summary (final iteration)
4. Otherwise: Spawn targeted agents with Master's feedback
5. Re-run Integrator and Master
6. Save checkpoint for iteration history to `checkpoints/` directory

**Mandatory First Iteration:** Even if Master is satisfied initially, at least one refinement cycle MUST occur.

### Step 6: Save Final Output

Save approved blog to `pdf/PaperLog/[title].md`

**Action:** Write final markdown with all figures and cover properly integrated.

## Output Structure

```
pdf/PaperLog/
├── [title].md                    # Final integrated blog
├── figures/                      # Extracted visual assets
│   ├── cover.png
│   ├── fig1_architecture.png
│   └── ...
├── checkpoints/                  # Iteration history
│   ├── blog_v1.md
│   ├── blog_v2.md
│   └── feedback/
│       ├── feedback_v1.txt
│       └── ...
└── figures_metadata.json
```

## Example Usage

**User says:** "Turn this SAM3 paper into a blog post"

**Workflow:**
1. Validate PDF input
2. Spawn Parser Agent → get parsed markdown
3. Spawn Blog Generator + Figure Extractor + Cover Designer in parallel
4. Spawn Integrator Agent → get integrated blog
5. Spawn Master Agent → get review feedback
6. **Iteration 1 (mandatory):** Targeted agents re-run with feedback
7. Re-run Integrator and Master
8. If approved after iteration >= 1: Save final output
9. Otherwise repeat steps 6-8 until iteration 3
10. Save final blog to `pdf/PaperLog/` and return summary

## Resources

### agents/

Contains specifications for each specialized agent:
- `parser.md` - PDF to markdown conversion
- `blog-generator.md` - Chinese blog generation with custom prompt
- `figure-extractor.md` - PDF rendering + AI vision figure/table extraction
- `cover-designer.md` - ZhipuAI CogView API cover generation
- `integrator.md` - Merge all outputs
- `master.md` - Quality review and iteration coordination

### scripts/

Contains Python helper scripts:
- `extract_figures.py` - PDF page rendering and figure cropping with AI vision
- `generate_cover.py` - Cover image generation via CogView API

### docs/plans/

- `2026-01-17-multi-agent-blog-generator-design.md` - System architecture design
- `2026-01-17-multi-agent-implementation.md` - Implementation planning reference
