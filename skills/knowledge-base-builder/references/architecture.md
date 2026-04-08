# Karpathy LLM Wiki Architecture Reference

Complete architecture specification for the knowledge base, based on Andrej Karpathy's LLM Wiki design.

## Three-Layer Architecture

| Layer | Directory | Write Permission | Core Rule | Purpose |
|-------|-----------|-----------------|-----------|---------|
| Raw Facts | `raw/` | User only, LLM read-only | Never modify, append only | Source material: web clippings, papers, PDFs, transcripts, code, personal notes |
| Knowledge Compiled | `wiki/` | LLM only, user read-only | LLM maintains entirely | Structured knowledge: concept pages, entity pages, summaries, cross-references |
| Rules & Constraints | `CLAUDE.md` | User + LLM co-iterate | All LLM operations must comply | The "constitution" defining structure, naming, workflows, boundaries |

## Two Core Navigation Files

### wiki/index.md (Content-Oriented Master Index)
- Location: `wiki/` root
- Must be updated by LLM after every Ingest
- Organized by: entities / concepts / sources / topics
- Each entry: 1-sentence summary + bidirectional link
- LLM must read this first when answering queries to locate relevant pages

### log.md (Time-Oriented Operation Log)
- Location: Root directory
- Append-only: never modify or delete existing entries
- Format: `## [YYYY-MM-DD] operation_type | description`
- Records all Ingest/Query/Lint operations
- Enables LLM to identify already-processed files

## Three Core Operations

### Operation 1: Ingest (Knowledge Entry/Compilation)
Trigger keywords: ingest, process, record, compile

Flow:
1. Scan `raw/` directory, compare against `log.md` ingest records, identify unprocessed files
2. Confirm file list with user, confirm focus areas
3. For each file:
   - Read original content, extract core information
   - Generate source summary page per `source_summary.md` template → `wiki/sources/`
   - Extract concepts and entities, check for existing wiki pages:
     - Existing pages: incrementally update with new information
     - New pages: create per template in `wiki/concepts/` or `wiki/entities/`
   - Add bidirectional links for all new/updated content
4. Update `wiki/index.md` master index
5. Append ingest record to `log.md`
6. Output summary to user

### Operation 2: Query (Query & Knowledge Archival)
Trigger keywords: query, search, ask, analyze, compare

Flow:
1. Read `wiki/index.md` to locate relevant pages
2. Read full content of all relevant pages
3. Generate answer with:
   - Source citations: `[Source: [[page_name]]]`
   - Bidirectional links for all concepts/entities
   - Clear structure (Markdown/tables/lists as appropriate)
4. If answer has high value (analysis, comparison, insight, new connections):
   - Generate new page → `wiki/queries/`
   - Update `wiki/index.md`
5. Append query record to `log.md`
6. Output answer to user with archived page names

### Operation 3: Lint (Health Inspection/Maintenance)
Trigger keywords: lint, inspect, health check, maintain

Recommended frequency: weekly

Flow:
1. Full scan of `wiki/` pages, checking:
   - Content consistency: contradictions across pages
   - Link integrity: broken bidirectional links, missing pages for mentioned concepts
   - Page health: orphan pages (no incoming links), empty pages, missing metadata
   - Information completeness: gaps that could be filled
2. Auto-fix certain issues (missing links, index errors)
3. Generate inspection report:
   - Scope and time of inspection
   - Auto-fixed issues
   - Issues requiring manual confirmation
   - Optimization suggestions
4. Save report to `_lint/lint-YYYY-MM-DD.md`
5. Append lint record to `log.md`

## Directory Structure

```
vault_root/
├── raw/                    # Raw facts layer (read-only)
│   ├── articles/           # Web clippings
│   ├── papers/             # Research papers
│   ├── transcripts/        # Meeting/podcast transcripts
│   ├── code/               # Code/project docs
│   ├── assets/             # Images/attachments
│   └── personal/           # Personal notes/journals
├── wiki/                   # Knowledge layer (LLM-only writes)
│   ├── concepts/           # Concept pages
│   ├── entities/           # Entity pages (people/projects/products)
│   ├── sources/            # Source summary pages
│   ├── queries/            # High-value query archives
│   └── index.md            # Master index
├── _templates/             # Page templates
│   ├── concept.md
│   ├── entity.md
│   └── source_summary.md
├── _lint/                  # Health check reports
├── _scripts/               # Automation scripts (optional)
├── log.md                  # Operation log (append-only)
└── CLAUDE.md               # Knowledge base constitution
```

## Iron Rules

1. Never modify anything in `raw/` — no tags, no edits, no renames
2. `log.md` is append-only — never modify or delete historical records
3. All `wiki/` content must follow template format requirements
4. Answer queries using knowledge base content first; web search only when KB lacks coverage
5. Never generate unsourced content — all claims must trace to source material
6. Always update `index.md` and `log.md` after every operation

## Daily Workflow

1. **Capture**: Web Clipper saves to `raw/`, personal notes to `raw/personal/`
2. **Compile**: 5 min daily — run Ingest, review AI output, confirm conflicts
3. **Explore**: Ask questions; high-value answers auto-archive back to Wiki
4. **Inspect**: Weekly Lint — review report, optimize structure

## Advanced Optimizations

- **Local search**: When KB exceeds 100 sources, add BM25+vector hybrid search
- **Automation**: Cron jobs to auto-sync notes and trigger ingest
- **Git versioning**: Track all changes with git for full rollback capability
- **Multi-format output**: Marp plugin for slides, Dataview for dynamic queries
