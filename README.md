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
| **humanizer-zh** | 去除文本中的 AI 生成痕迹。检测并修复夸大的象征意义、宣传性语言、肤浅分析、AI 词汇等模式，使文字听起来更自然、更像人类书写 |
| **paper-to-blog** | Transforms academic papers (PDFs) into comprehensive 2000-word blog posts using a multi-agent system with parallel execution, OCR-based figure extraction, cover design, and iterative refinement |
| **senior-computer-vision** | World-class computer vision skill for image/video processing, object detection, segmentation, and visual AI systems. Expertise in PyTorch, OpenCV, YOLO, SAM, diffusion models, and vision transformers |
| **video-downloader** | Downloads videos from YouTube and other platforms for offline viewing, editing, or archival. Handles various formats and quality options |

### claude-mem Extensions

The `claude-mem-extension/` directory contains tools that extend [claude-mem](https://github.com/thedotmack/claude-mem) - the persistent memory system for Claude Code.

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

*Last updated: February 12, 2026*
