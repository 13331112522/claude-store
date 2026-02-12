# Paper-to-Blog Skill

Transform academic research papers into comprehensive Chinese blog posts using a multi-agent AI system.

## Features

- **Multi-Agent Architecture**: 6 specialized agents with parallel execution
- **Chinese Blog Generation**: ~2000 words, Medium-style, clean and scannable
- **OCR-Based Figure Extraction**: Extract actual figures/tables (not full pages) with AI vision
- **Cover Design**: Cartoon infographic illustration (16:9, hand-drawn style)
- **Iterative Refinement**: Quality-driven improvement loop (1-3 iterations)

## Quick Start

```
User: "Convert this research-paper.pdf to a blog post"
```

The skill will:
1. Parse the PDF to markdown
2. Generate Chinese blog content (~2000 words)
3. Extract figures and tables with OCR
4. Create cover illustration
5. Integrate everything into final markdown
6. Review and refine (1-3 iterations)
7. Save to `pdf/PaperLog/[title].md`

## Requirements

- Claude Code with MCP tools enabled
- PDF research paper as input

## Output

```
pdf/PaperLog/
├── [title].md              # Final integrated blog
├── figures/
│   ├── cover.png
│   └── [extracted figures]
└── checkpoints/            # Iteration history
```

## Architecture

See [docs/plans/2026-01-17-multi-agent-blog-generator-design.md](docs/plans/2026-01-17-multi-agent-blog-generator-design.md) for detailed system architecture.

## License

Part of the Claude Code skills ecosystem.
