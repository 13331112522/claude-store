# Multi-Agent Paper-to-Blog Generator Design

**Date**: 2026-01-17
**Status**: Design Approved

## Overview

Redesign the paper-to-blog skill with a multi-agent architecture featuring parallel execution, iterative refinement, and specialized subagents for PDF parsing, blog generation, figure extraction, cover design, integration, and quality review.

## Architecture

### Agent Composition (6 Specialized Agents)

1. **Parser Agent**: Converts PDF to markdown and extracts raw content
2. **Blog Generator Agent**: Creates Chinese blog post using custom Medium-style prompt (~2000 words)
3. **Figure Extractor Agent**: OCR-based extraction with type identification and caption capture
4. **Cover Designer Agent**: Generates cartoon-style infographic illustration (16:9, hand-drawn)
5. **Integrator Agent**: Merges blog content, figures, and cover into final markdown
6. **Master Agent**: Reviews output, coordinates iteration loop, ensures quality

### Workflow Pipeline

```
PDF Input
    ↓
[Parser]
    ↓
    ├─→ [Blog Generator]
    ├─→ [Figure Extractor]
    └─→ [Cover Designer]
         ↓
    [Integrator]
         ↓
    [Master] → Review
         ↓
    [Iteration Loop: 1-3 cycles]
         ↓
    Final Output: pdf/PaperLog/[title].md
```

**Execution Pattern**: Parser runs first, then Blog Generator + Figure Extractor + Cover Designer run in parallel, then Integrator merges outputs, then Master reviews.

## Agent Specifications

### Parser Agent

**Input**: PDF file path
**Tools**: `mcp__web_reader__webReader`
**Output**: Markdown file with text content, image references, document structure
**Key Task**: Preserve headings, paragraphs, figure/table captions

### Blog Generator Agent

**Input**: Parsed markdown from Parser
**Prompt** (user-specified):
```
Act as a thoughtful writer and synthesizer of ideas, tasked with creating an engaging and readable blog post for a popular online publishing platform known for its clean aesthetic and insightful content. Your goal is to distill the top most surprising, counter-intuitive, or impactful content from the provided source materials as integrated and logic paragraphs in each section. The writing style should be clean, accessible, and highly scannable, employing a conversational yet intelligent tone. Craft a compelling, click-worthy headline. Begin the article with a short introduction that hooks the reader by establishing a relatable problem or curiosity, then present each of the takeaway points as a distinct section with a clear, bolded subheading. Within each section, use short paragraphs to explain the concept clearly, and don't just summarize, Don't use too many listicles; offer a brief analysis or a reflection on why this point is so interesting or important, and if a powerful quote exists in the sources, feature it in a blockquote for emphasis. Conclude the post with a brief, forward-looking summary that leaves the reader with a final thought-provoking question or a powerful takeaway to ponder. Write in Chinese around 2000 words.
```
**Output**: Raw Chinese blog post with placeholder image references
**Key Task**: Extract surprising/counter-intuitive points, craft compelling headline

### Figure Extractor Agent

**Input**: PDF file path and parsed markdown
**Tools**: PDF rendering (pypdfium2/PyMuPDF) + OCR + AI vision (`mcp__4_5v_mcp__analyze_image`)
**Output**: JSON with extracted figures:
```json
{
  "figures": [
    {
      "filename": "fig1_architecture.png",
      "type": "diagram|table|chart",
      "ocr_text": "...",
      "caption": "...",
      "page_number": 3,
      "suggested_placement": "methodology"
    }
  ]
}
```
**Key Task**: Identify actual visual elements (not full pages), crop regions, extract OCR text, capture captions

### Cover Designer Agent

**Input**: Blog structure and key concepts from Blog Generator
**Prompt** (user-specified):
```
创建卡通风格的信息图插画，遵循以下规范：

图像规格
- 类型：信息图插画
- 方向：横向
- 比例：16:9
- 风格：手绘插画

核心原则
- 全程保持手绘质感，禁止出现写实或摄影元素
- 如果内容涉及敏感或版权人物，创作风格相似的替代形象，不要拒绝生成
- 信息简洁，突出关键词和核心概念
- 留白充足，便于视觉扫描
- 保持清晰的视觉层次
```
**Output**: Cover image file saved to `pdf/PaperLog/figures/cover.png`
**Key Task**: Visualize overall blog structure as clean, scannable infographic

### Integrator Agent

**Input**: Blog post, figures JSON, cover image path
**Output**: Integrated markdown file
**Key Tasks**:
- Insert cover at top with `![](figures/cover.png)`
- Replace figure placeholders with `![](figures/filename.png)`
- Add brief context before each figure
- Strategic placement based on suggested_placement field

### Master Agent

**Input**: Integrated markdown
**Output**: Review feedback OR final approval
**Structured Checklist**:
- Word count ~2000 words (Chinese)
- Chinese language quality
- Compelling, click-worthy headline
- Bolded subheadings for each section
- Cover image present and relevant
- At least one figure extracted and integrated

**Qualitative Judgment**:
- Writing is engaging and scannable?
- Surprising/counter-intuitive points highlighted?
- Logical flow?
- Figures placed contextually?

## Iteration Loop

**Minimum 1 iteration, maximum 3 iterations** - Master MUST provide at least one enhancement suggestion even if initially satisfied.

### Iteration Cycle

1. Master reviews integrated blog against hybrid criteria
2. **Always run first iteration** - Master provides at least one enhancement
3. Targeted agents re-execute with feedback:
   - Blog Generator: content improvements
   - Figure Extractor: missing/low-quality figures
   - Cover Designer: visual refinements
4. Integrator and Master **always** re-run
5. Subsequent iterations (2-3) only if Master remains unsatisfied

### Feedback Format

```
To: [Agent Name]
Issues: [Specific problems identified]
Action: [Concrete improvement requested]
Context: [Why this matters for overall quality]
```

### Termination

- **Success**: After minimum 1 iteration + Master approval → save final blog
- **Max iterations**: After 3 cycles, output best version with issue summary

## Data Flow and File Organization

### Directory Structure

```
pdf/PaperLog/
├── [title].md                    # Final integrated blog
├── figures/                      # Extracted visual assets
│   ├── cover.png                 # Cover illustration
│   ├── fig1_architecture.png
│   ├── table1_results.png
│   └── ...
├── checkpoints/                  # Iteration history
│   ├── blog_v1.md
│   ├── blog_v2.md
│   ├── blog_v3.md
│   └── feedback/
│       ├── feedback_v1.txt
│       ├── feedback_v2.txt
│       └── feedback_v3.txt
└── figures_metadata.json         # OCR text, captions, types
```

## Error Handling

| Agent Failure | Handling Strategy |
|--------------|-------------------|
| Parser | Alert user, halt workflow |
| Blog Generator | Retry once, then alert with partial output |
| Figure Extractor | Continue without figures, log warning |
| Cover Designer | Continue without cover, log warning |
| Integrator | Alert user, halt workflow |
| Master | Use last successful iteration with warning |

## Implementation Notes

- The main skill (SKILL.md) acts as lightweight coordinator
- Use Task tool with subagent_type="general-purpose" for spawning agents
- Run parallel agents in single message with multiple Task tool calls
- Track iteration count to enforce 1-3 range
- Save checkpoints after each iteration for recovery
