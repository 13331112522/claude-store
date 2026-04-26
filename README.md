# Claude Store

A collection of techniques, patterns, and tools for working effectively with Claude Code.

## Overview

This repository contains my personal collection of Claude-related techniques and configurations. It's an evolving project that captures best practices, custom commands, specialized agents, and skills developed through extensive hands-on experience with Claude.

## What's Inside

This collection focuses on practical techniques for:

- **Agent Design Patterns**: Reusable agent architectures for common tasks
- **Custom Commands**: Slash commands that extend Claude's capabilities
- **Specialized Skills**: Domain-specific expertise and workflows
- **Prompt Engineering**: Techniques for getting the best results from Claude
- **claude-mem Extensions**: Tools for extending Claude's persistent memory capabilities

## Usage

### Agents

Place agent configuration files in the `agents/` directory. These subagent configurations can be launched using the Task tool in Claude Code:

```
Use the Task tool with the subagent_type parameter matching your agent configuration
```

Agents are ideal for complex, multi-step tasks that require specialized capabilities or autonomous execution.

### Commands

Place custom slash command definitions in the `commands/` directory. Each command file (`.md` format) defines a slash command that you can invoke directly:

```
/command-name
```

Commands are perfect for frequently-used workflows, predefined prompts, or complex operations you want to repeat consistently.

### Skills

Place skill definitions in the `skills/` directory. Skills extend Claude's capabilities with specialized knowledge and workflows:

```
Use the Skill tool to invoke a skill by name
```

Skills are designed for domain-specific tasks like document processing, data analysis, or specialized content creation.

#### Available Skills

| Skill | Description |
|-------|-------------|
| **ai-daily-digest** | Fetches RSS feeds from 90+ top Hacker News sources, uses Gemini (primary) or OpenAI-compatible APIs to generate a daily AI/tech digest report with configurable sources and bilingual support |
| **akshare** | 使用 AKShare Python 库查询中国股票数据。支持 A 股、港股、美股实时行情、历史 K 线、财务报表、资金流向、龙虎榜、融资融券等数据查询 |
| **baoyu-article-illustrator** | Analyzes article structure, identifies key paragraphs, and generates AI illustrations in multiple styles (editorial, watercolor, sketch, minimal, etc.) with batch strategy and error handling |
| **humanizer-zh** | 去除文本中的 AI 生成痕迹。检测并修复夸大的象征意义、宣传性语言、肤浅分析、AI 词汇等模式，使文字听起来更自然、更像人类书写 |
| **investment-advisor** | 基于段永平价值投资哲学的个人投资顾问。融合投资学习资料、仓位管理、估值模型和 Dalio 宏观周期框架的实战投资知识体系。支持公司分析、买卖决策、仓位管理、估值判断等 |
| **knowledge-base-builder** | Implements Andrej Karpathy's viral "LLM Wiki" architecture — turns your Obsidian vault into a self-compiling knowledge engine. LLM acts as a "knowledge incremental compiler": dump raw materials (papers, articles, transcripts) into `raw/`, run Ingest to compile structured wiki pages with bidirectional links, Query to retrieve with source citations, and Lint to health-check. Deeply integrated with Obsidian CLI for indexed search, backlink analysis, automatic wikilink rewriting, and orphan detection — capabilities impossible with plain file I/O. One-command init, graceful CLI fallback, multi-vault support |
| **obsidian-cli** | Obsidian vault CLI integration — vault health checks, command reference, and vault management utilities |
| **paper-to-blog** | Transforms academic papers (PDFs) into comprehensive 2000-word blog posts using a multi-agent system with parallel execution, OCR-based figure extraction, cover design, and iterative refinement |
| **self-improving-agent** | Self-improving agent pattern with pre-tool, post-bash, and session-end hooks for continuous learning and behavior refinement |
| **senior-computer-vision** | World-class computer vision skill for image/video processing, object detection, segmentation, and visual AI systems. Expertise in PyTorch, OpenCV, YOLO, SAM, diffusion models, and vision transformers |
| **vibe-trading** | AI-powered multi-agent finance workspace with backtesting, strategy generation, and portfolio analysis across global markets (A-shares, HK/US equities, crypto). Supports 64 finance skills, 29 agent swarm presets, technical analysis, quant research, and derivatives pricing |
| **video-downloader** | Downloads videos from YouTube and other platforms for offline viewing, editing, or archival. Handles various formats and quality options |
| **volcengine-podcast-tts** | Volcengine podcast TTS integration — protocol client for converting text scripts to podcast audio using Volcengine's TTS API with speaker diarization support |
| **html-ppt-editor** | **WYSIWYG editor for guizang-style HTML PPT files** — edit text, add images/text, drag/reposition elements, replace/delete/resize images, delete slides, and save. Perfect for visual editing of magazine-style web presentations |
| **guizang-ppt-skill** | Generates "electronic magazine × e-ink" style horizontal swipe web PPTs (single HTML file). Features WebGL fluid backgrounds, serif titles + sans-serif body, chapter curtains, data posters, and image grids. Ideal for sharing/demographics/launch-style presentations |

### claude-mem Extensions

The `claude-mem-extension/` directory contains tools that extend [claude-mem](https://github.com/thedotmack/claude-mem) - the persistent memory system for Claude Code.

## Featured Skills

### HTML PPT Editor

The **html-ppt-editor** skill provides browser-based WYSIWYG editing capabilities for guizang-style HTML presentations. It's perfect when you need to visually edit a PPT without touching code.

#### When to Use

- You have a guizang-format HTML PPT file (single file with `<section class="slide">` and `#deck`)
- You want to "edit this PPT", "modify text", "replace images", "add images/text", "drag to reposition"
- You prefer visual editing over manual code changes

#### Workflow

**Step 1: Create an editable version**

The editor script is injected into your HTML file:

```python
import os
# Read original HTML
with open('your-file.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Read editor script
editor_js_path = os.path.expanduser('~/.claude/skills/html-ppt-editor/guizang-ppt-editor.js')
with open(editor_js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Inject before </body>
html = html.replace('</body>', f'<script>\n{js}\n</script>\n</body>')

# Save as editor.html
output_path = 'editor.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)
```

**Step 2: Open in browser**

```bash
open editor.html
```

**Step 3: Use the editor**

| Operation | Method |
|-----------|--------|
| **Enter/Exit Edit Mode** | Click "Edit" button or press `E` key |
| **Select Element** | Click on text block or image in edit mode |
| **Edit Text** | Double-click text block, type directly |
| **Add Image** | Click "🖼 Add Image" → select image file |
| **Add Text** | Click "📝 Add Text" → auto enters edit mode |
| **Drag to Move** | Select → drag blue handle icon (top-left) |
| **Replace Image** | Select image → Click "📷 Replace" → select new image |
| **Delete Image** | Select image → Click "🗑 Delete" button |
| **Resize Image** | Select image → drag corner handles |
| **Delete Element** | Select → press `Delete` key |
| **Navigate Slides** | Exit edit, use `←→` keys or bottom dots; use toolbar ◀▶ in edit mode |
| **Delete Slide** | Click "🗑 Delete Page" in toolbar |
| **Deselect** | Click blank area or press `Esc` |
| **Save** | Click "💾 Save" or press `Ctrl+S` → downloads clean HTML |

**Keyboard shortcuts:** `E` (edit) | `←→` (navigate) | `Double-click` (edit text) | `Delete` (remove) | `Ctrl+S` (save) | `Esc` (exit)

**Step 4: After editing**

The save function automatically downloads `index-edited.html` — a clean HTML file without editor code. To continue editing, simply re-inject the editor script.

#### Notes

1. **Only supports guizang format** — HTML must have `#deck` container and `<section class="slide">` elements
2. **Save downloads a new file** — Browser security prevents overwriting the original file
3. **Editor doesn't affect original file** — Injection is done on a copy
4. **Image replacement uses base64** — Replaced images are embedded as base64, file size will increase
5. **Drag uses transform** — Moved elements use CSS `transform: translate()`, preserved on save

#### skill-generator

A TypeScript-based tool that automatically transforms your conversation history into reusable Claude Code skills.

**What it does:**
- Searches your claude-mem stored conversations for valuable patterns
- Scores and ranks candidates by type weight and work investment
- Extracts core problems, solutions, and best practices
- Generates standardized skill files with YAML frontmatter
- Provides interactive review workflow before saving

**Quick start:**
```bash
cd claude-mem-extension/skills/skill-generator
npm install
npm run build
./install.sh
```

**Usage in Claude Code:**
```
/claude-mem:skill-generator
```

Invoke this slash command anytime you want to generate skills based on your Claude Code usage history.

**Generated skills are saved to:** `~/.claude/skills/experiences/`

## Philosophy

The techniques shared here are grounded in real-world usage. Each pattern, command, or skill has been developed and refined through actual work, not theoretical exploration.

The goal is to share practical, immediately useful approaches that you can adapt to your own needs.

## Status

This is the initial version of the repository. The content will evolve and expand as I continue to discover and refine new techniques.

## Contributing

While this is primarily a personal collection, feel free to explore, adapt, and use these techniques in your own work. If you find something particularly useful, I'd love to hear about it.

---

*Last updated: April 26, 2026*
