---
name: obsidian-cli
description: This skill should be used when the user wants to read, create, edit, move, search, or manage notes in an Obsidian vault via the command line. It provides comprehensive Obsidian CLI (v1.12.4+) command knowledge for full vault management — including CRUD operations on notes, frontmatter properties, tags, links, daily notes, tasks, plugins, themes, search, sync, publish, and automated vault health monitoring. Triggers when the user mentions Obsidian, vault operations, daily notes, or wants to script/automate note-taking workflows from the terminal.
---

# Obsidian CLI

## Overview

Manipulate an Obsidian vault programmatically via the official CLI (shipped with Obsidian 1.12.4+). The CLI is a "remote control" for a running Obsidian app — every operation passes through Obsidian's internal API, so wikilinks stay intact, the index stays in sync, and frontmatter updates are reflected immediately.

## Prerequisites

- Obsidian 1.12.4 or later installed
- CLI enabled: **Settings → General → Command line interface** → toggle on → **Register CLI**
- PATH configured (macOS): `export PATH="$PATH:/Applications/Obsidian.app/Contents/MacOS"`
- Verify: `obsidian version`

## Key Design Principles

1. **The CLI auto-launches Obsidian if not running.** No manual startup needed, but allow time for app boot on first command.
2. **The `move` command auto-rewrites wikilinks.** This is the primary advantage over direct file manipulation. Never use `mv` to move vault files.
3. **All operations go through Obsidian's internal API.** Index, links, and metadata stay consistent — unlike editing `.md` files directly on disk.
4. **Multi-vault support.** Prefix any command with `vault="VaultName"` to target a specific vault.
5. **For bulk operations on 3000+ files**, consider shell loops or Python scripts calling the CLI, as sequential CLI calls have per-command overhead.

## Command Syntax

```
obsidian [vault="VaultName"] <command> [param=value] [flag]
```

- Parameters: `key=value` format
- Flags: bare words (no `--` prefix), except `--copy`
- Output formats: `format=json|csv|tsv|md|paths|text|tree|yaml`

## Quick Reference by Task

### Note CRUD

```bash
# List all notes
obsidian files

# Read a note
obsidian read file="path/to/note"

# Create a note
obsidian create name="path/to/note" content="# Title"

# Create from template
obsidian create name="path/to/note" template="TemplateName"

# Append / prepend content
obsidian append file="path/to/note" content="new text"
obsidian prepend file="path/to/note" content="text after frontmatter"

# Move (rewrites wikilinks automatically)
obsidian move file="old/path" to="new/path"

# Delete (to trash, or permanent)
obsidian delete file="path/to/note"
obsidian delete file="path/to/note" permanent
```

### Frontmatter Properties

```bash
# View properties
obsidian properties file="note"

# Read a specific property
obsidian property:read file="note" name="category"

# Set a property
obsidian property:set file="note" name="category" value="tech"

# Remove a property
obsidian property:remove file="note" name="status"
```

### Search

```bash
# Full-text search (file paths)
obsidian search query="search term"

# Search with context (grep-style)
obsidian search:context query="term" limit=10

# JSON output for piping
obsidian search query="TODO" format=json | jq '.[].file'
```

### Tags

```bash
# List all tags
obsidian tags

# Files with a specific tag
obsidian tag tag="#project"

# Bulk rename a tag
obsidian tags:rename old="oldtag" new="newtag"
```

### Links & Vault Health

```bash
# Outgoing links from a note
obsidian links file="note"

# Backlinks to a note
obsidian backlinks file="note"

# Broken link targets (unresolved)
obsidian unresolved

# Notes with no incoming links (orphans)
obsidian orphans

# Notes with no outgoing links (dead ends)
obsidian deadends
```

### Daily Notes

```bash
# Open today's daily note (creates if missing)
obsidian daily

# Read / append / get path
obsidian daily:read
obsidian daily:append content="- [ ] Task"
obsidian daily:path
```

### Tasks

```bash
# List all tasks
obsidian tasks

# Show or update a specific task
obsidian task
```

### Bulk Operations Pattern

For operations across many files, use `format=paths` and pipe:

```bash
# Move all files with a tag to a folder
obsidian tag tag="#archive" format=paths | xargs -I{} obsidian move file="{}" to="Archive/"

# Set property on all files
obsidian files format=paths | while read -r f; do
  obsidian property:set file="$f" name="status" value="review"
done
```

### Plugin & Theme Management

```bash
obsidian plugins
obsidian plugin:enable id="dataview"
obsidian plugin:disable id="calendar"
obsidian themes
obsidian theme:set name="Minimal"
```

### Developer Access

```bash
# Execute JS in Obsidian's context
obsidian eval code="app.vault.getFiles().length"

# Screenshot, console, errors
obsidian dev:screenshot
obsidian dev:console
obsidian dev:errors
```

## Automated Vault Health Check

Use the bundled script for periodic vault health monitoring:

```bash
bash scripts/vault-health-check.sh [vault_name]
```

This script reports orphan notes, unresolved links, dead ends, and tag summary.

To automate via cron (e.g., weekly Monday morning appended to daily note):

```
0 9 * * 1 obsidian daily:append content="$(/path/to/vault-health-check.sh)"
```

## Knowledge Base Patterns

When operating on a Karpathy LLM Wiki knowledge base (knowledge-base-builder skill), use these specialized patterns:

### Scan for Unprocessed Raw Files
```bash
# List all raw markdown files, diff against log.md ingest records
obsidian files format=paths | grep "^raw/" | grep -E "\.(md|txt)$"
obsidian read file="log.md" | grep -E "ingest|处理"
```

### Create Wiki Page with Frontmatter
```bash
# Create a concept page, then set properties
obsidian create name="wiki/concepts/New-Concept.md" content="# New Concept\n\nDefinition..."
obsidian property:set file="wiki/concepts/New-Concept.md" name="type" value="concept"
obsidian property:set file="wiki/concepts/New-Concept.md" name="tags" value="[tag1, tag2]"
obsidian property:set file="wiki/concepts/New-Concept.md" name="source_count" value="1"
obsidian property:set file="wiki/concepts/New-Concept.md" name="date" value="2026-04-07"
```

### Check Knowledge Base Health
```bash
# Full health audit (orphans, unresolved, deadends, tags)
obsidian orphans | grep "^wiki/"
obsidian unresolved
obsidian deadends | grep "^wiki/" | grep -v "wiki/index.md"
obsidian tags
```

### Discover Page Relationships
```bash
# Find all pages linking to a concept
obsidian backlinks file="wiki/concepts/Self-Evolution-and-Self-Improvement.md"
# Find all pages a concept links to
obsidian links file="wiki/concepts/Self-Evolution-and-Self-Improvement.md"
```

### Bulk Ingest Progress Tracking
```bash
# Count compiled vs raw files
echo "Raw: $(obsidian files format=paths | grep '^raw/' | grep '\.md$' | wc -l)"
echo "Wiki sources: $(obsidian files format=paths | grep '^wiki/sources/' | grep '\.md$' | wc -l)"
echo "Wiki concepts: $(obsidian files format=paths | grep '^wiki/concepts/' | grep '\.md$' | wc -l)"
echo "Wiki entities: $(obsidian files format=paths | grep '^wiki/entities/' | grep '\.md$' | wc -l)"
```

### Move/Rename a Wiki Page (auto-updates all links)
```bash
# Safe rename — all [[Old Name]] references across the vault are updated
obsidian move file="wiki/concepts/Old-Name.md" to="wiki/concepts/New-Name.md"
```

## Full Command Reference

For the complete list of 100+ commands across all categories (files, properties, search, tags, links, tasks, daily notes, templates, bookmarks, bases, plugins, themes, snippets, workspaces, file history, sync, publish, developer tools), consult `references/command-reference.md`.

## Limitations

- Obsidian desktop must be running (CLI auto-launches if not)
- Desktop only (no CLI on iOS/Android)
- Sequential execution is slow for 3000+ files — use scripts for bulk work
- Multiple vaults require `vault="Name"` parameter each time
