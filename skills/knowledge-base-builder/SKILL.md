---
name: knowledge-base-builder
description: This skill scaffolds a complete Karpathy LLM Wiki personal knowledge base from scratch, including the full directory structure (raw/, wiki/, _templates/, _lint/, _scripts/), the CLAUDE.md constitution file, page templates (concept, entity, source_summary), initial log.md and wiki/index.md. Triggers when the user wants to create, initialize, or set up a new knowledge base, Obsidian vault for knowledge management, or LLM Wiki following the Karpathy architecture.
---

# Knowledge Base Builder

## Overview

Scaffold a complete Karpathy LLM Wiki knowledge base from zero to operational. Based on Andrej Karpathy's architecture where LLM acts as a "knowledge incremental compiler" — knowledge is compiled once into a persistent, interlinked Markdown Wiki that grows with compound interest on every new input.

Core metaphor: **Obsidian is the IDE, LLM is the programmer, Wiki is the iterable codebase.**

## Quick Start: Initialize a New Knowledge Base

Run the bundled init script to create the complete directory structure and all initial files:

```bash
bash scripts/init_knowledge_base.sh /path/to/target/directory
```

This creates:
- All directories: `raw/`, `wiki/`, `_templates/`, `_lint/`, `_scripts/`
- `CLAUDE.md` — the knowledge base constitution (copied from `assets/CLAUDE.md`)
- Three page templates in `_templates/` (copied from `assets/`)
- Initial `log.md` (append-only operation log)
- Initial `wiki/index.md` (master navigation index)
- `.gitkeep` files in empty directories

After initialization:
1. Open the target directory as an Obsidian vault
2. Start Claude Code in that directory (auto-reads `CLAUDE.md`)
3. Add source materials to `raw/` subdirectories
4. Issue "ingest" command to begin compiling knowledge

## Three-Layer Architecture

| Layer | Directory | Write Access | Rule |
|-------|-----------|-------------|------|
| Raw Facts | `raw/` | User only (LLM read-only) | Never modify, append only |
| Knowledge | `wiki/` | LLM only (user reads/reviews) | Follow templates, bidirectional links |
| Rules | `CLAUDE.md` | User + LLM co-iterate | All LLM operations must comply |

## Directory Structure

```
vault_root/
├── raw/                    # Source material (read-only for LLM)
│   ├── articles/           # Web clippings
│   ├── papers/             # Research papers
│   ├── transcripts/        # Meeting/podcast transcripts
│   ├── code/               # Code/project docs
│   ├── assets/             # Images/attachments
│   └── personal/           # Personal notes/journals
├── wiki/                   # Compiled knowledge (LLM writes)
│   ├── concepts/           # Concept pages
│   ├── entities/           # Entity pages (people/projects/products)
│   ├── sources/            # Source summary pages
│   ├── queries/            # High-value query archives
│   └── index.md            # Master index (updated after every operation)
├── _templates/             # Page templates
│   ├── concept.md
│   ├── entity.md
│   └── source_summary.md
├── _lint/                  # Health check reports
├── _scripts/               # Automation scripts
├── log.md                  # Operation log (append-only)
└── CLAUDE.md               # Knowledge base constitution
```

## Three Core Operations

### 1. Ingest (Knowledge Compilation)
**Triggers**: ingest, process, compile

1. Scan `raw/`, compare against `log.md`, find unprocessed files
2. Confirm file list and focus areas with user
3. Per file: generate source summary → update/create concept & entity pages → add bidirectional links
4. Update `wiki/index.md`
5. Append to `log.md`: `## [YYYY-MM-DD] ingest | processed file, X pages created, X updated`
6. Output summary to user

### 2. Query (Knowledge Retrieval & Archival)
**Triggers**: query, search, ask, analyze, compare

1. Read `wiki/index.md` to locate relevant pages
2. Read full content of all relevant pages
3. Generate answer with source citations `[Source: [[page]]]` and bidirectional links
4. High-value answers auto-archive to `wiki/queries/`, update `index.md`
5. Append to `log.md`
6. Output answer with archived page names

### 3. Lint (Health Check)
**Triggers**: lint, inspect, health check, maintain

1. Full scan of `wiki/` — check consistency, link integrity, orphans, completeness
2. Auto-fix certain issues
3. Generate report → `_lint/lint-YYYY-MM-DD.md`
4. Append to `log.md`
5. Output summary with link to full report

## Obsidian CLI Enhanced Mode

When Obsidian CLI (v1.12.4+) is available, use it instead of direct file I/O for all vault operations. The CLI keeps Obsidian's index in sync, auto-rewrites wikilinks on moves, and provides instant link diagnostics that are impossible with direct file manipulation.

### Prerequisites
- Obsidian 1.12.4+ installed and running (CLI auto-launches it)
- CLI enabled: Settings > General > Command line interface > toggle on > Register CLI
- PATH: `export PATH="$PATH:/Applications/Obsidian.app/Contents/MacOS"`

### When to Use CLI vs Direct File I/O

| Operation | CLI Command | Advantage |
|-----------|-------------|-----------|
| Scan raw files | `obsidian files format=paths \| grep "^raw/"` | Always in sync with Obsidian index |
| Read wiki page | `obsidian read file="path"` | Index-aware read |
| Create wiki page | `obsidian create name="path" content="..."` | Auto-index, validates wikilinks |
| Append to log.md | `obsidian append file="log.md" content="..."` | Index stays consistent |
| Set frontmatter | `obsidian property:set file="path" name="k" value="v"` | Clean YAML, no breakage risk |
| Search knowledge | `obsidian search query="..." format=json` | Full-text indexed search |
| Check backlinks | `obsidian backlinks file="path"` | Impossible with direct I/O |
| Find broken links | `obsidian unresolved` | Instant, impossible with direct I/O |
| Find orphans | `obsidian orphans` | Instant, impossible with direct I/O |
| Move/rename page | `obsidian move file="old" to="new"` | Auto-rewrites ALL wikilinks |
| Bulk tag rename | `obsidian tags:rename old="x" new="y"` | One command, updates everywhere |

### Enhanced Ingest Flow

```
1. SCAN:  obsidian files format=paths | grep "^raw/" | grep -E "\.(md|txt)$"
   → Compare against log.md ingest records to find unprocessed files

2. READ:  obsidian read file="raw/path/to/file.md"
   → Read source material through Obsidian's API

3. CHECK: obsidian search query="concept name" format=paths
   → Check if concept/entity page already exists before creating

4. CREATE: obsidian create name="wiki/sources/src-FILE.md" content="..."
           obsidian property:set file="..." name="type" value="source_summary"
   → Create pages with automatic index sync

5. UPDATE: obsidian append file="wiki/concepts/X.md" content="new section"
   → Add new findings to existing concept pages

6. INDEX:  Regenerate wiki/index.md content, then obsidian create (overwrite)

7. LOG:    obsidian append file="log.md" content="## [DATE] ingest | ..."
```

### Enhanced Query Flow

```
1. SEARCH:  obsidian search query="user query" format=paths | grep "^wiki/"
            obsidian search:context query="..." limit=20
   → Full-text indexed search across wiki pages

2. READ:    obsidian read file="wiki/concepts/X.md"
   → Read relevant pages

3. RELATE:  obsidian backlinks file="wiki/concepts/X.md"
            obsidian links file="wiki/concepts/X.md"
   → Discover relationships via backlinks (impossible without CLI)

4. ARCHIVE: obsidian create name="wiki/queries/query-TOPIC.md" content="..."
            obsidian property:set file="..." name="type" value="query"
   → Archive high-value answers

5. INDEX + LOG: Same as Ingest steps 6-7
```

### Enhanced Lint Flow

```
1. LINK HEALTH:
   obsidian orphans     → wiki pages with no incoming links
   obsidian unresolved  → broken link targets (distinguish "expected" vs "truly broken")
   obsidian deadends    → wiki pages with no outgoing links

2. FRONTMATTER: For each wiki/ page:
   obsidian property:read file="..." name="type"
   obsidian property:read file="..." name="tags"
   → Verify all required fields present

3. BACKLINK SYMMETRY: For each wiki/ page:
   obsidian backlinks file="..." and obsidian links file="..."
   → If A links to B, B should reference A in its "related" section

4. INDEX FRESHNESS:
   obsidian files format=paths | grep "^wiki/" vs wiki/index.md content
   → Detect pages on disk but missing from index

5. AUTO-FIX (with --fix):
   obsidian property:set for missing frontmatter
   obsidian append for missing cross-references
```

### Fallback Behavior

When Obsidian CLI is unavailable, all operations revert to direct file I/O (Read/Write/Edit tools). Features lost in fallback mode:
- Backlink analysis (no way to discover incoming links)
- Automatic wikilink rewriting on move/rename
- Instant orphan/unresolved link detection
- Structured search with ranking
- Safe frontmatter manipulation

Scripts detect CLI availability at runtime and degrade gracefully.

### Multi-Vault Support

If the knowledge base is not the active Obsidian vault, prefix all commands:
```bash
obsidian vault="knowledge_base" files format=paths
```

Scripts accept `--vault VaultName` argument. When omitted, auto-detects by comparing `obsidian vault` path against current directory.

### Operational Scripts

Five scripts are provided in `scripts/` and deployed to `_scripts/` during initialization:

| Script | Purpose | Usage |
|--------|---------|-------|
| `kb-common.sh` | Shared library (CLI detection, vault resolution, log append) | Source from other scripts |
| `kb-ingest-scan.sh` | Scan raw/ for unprocessed files | `bash kb-ingest-scan.sh [--format paths\|json\|summary]` |
| `kb-query-search.sh` | Search wiki pages with backlink discovery | `bash kb-query-search.sh "query" [--context]` |
| `kb-lint.sh` | Full health audit (superset of vault-health-check.sh) | `bash kb-lint.sh [--fix] [--scope wiki\|all]` |
| `kb-stats.sh` | Vault statistics dashboard | `bash kb-stats.sh [--format summary\|json\|md]` |

All scripts support `--vault VaultName` for multi-vault environments.

## Page Templates

All pages must have YAML frontmatter (title, type, date, tags, source_count) and bidirectional `[[links]]`.

Three templates are provided in `assets/`:
- **concept.md** — Core definition, principles, use cases, related links
- **entity.md** — Overview, key info, timeline, related links
- **source_summary.md** — Summary, key points, extracted concepts/entities, conflicts

## Iron Rules

1. Never modify `raw/` — no tags, no edits, no renames
2. `log.md` is append-only — never modify or delete
3. All `wiki/` content follows template format
4. Prefer knowledge base content over web search
5. Never generate unsourced claims
6. Always update `index.md` and `log.md` after every operation

## Bundled Resources

### scripts/
- `init_knowledge_base.sh` — Full knowledge base skeleton initialization with CLI detection
- `kb-common.sh` — Shared library for CLI detection, vault resolution, log append
- `kb-ingest-scan.sh` — Scan raw/ for unprocessed files (CLI-enhanced with fallback)
- `kb-query-search.sh` — Search wiki with backlink discovery (CLI-enhanced with fallback)
- `kb-lint.sh` — Full health audit with auto-fix (superset of vault-health-check.sh)
- `kb-stats.sh` — Vault statistics dashboard (CLI-enhanced with fallback)

### references/architecture.md
Full architecture specification including three-layer model, navigation files, detailed operation flows, directory structure, and advanced optimization strategies. Load this for in-depth understanding of the Karpathy LLM Wiki design.

### assets/
- `CLAUDE.md` — Knowledge base constitution to be placed in vault root
- `concept.md` — Concept page template
- `entity.md` — Entity page template
- `source_summary.md` — Source summary page template
