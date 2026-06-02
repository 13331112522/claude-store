---
name: mind-transposition
description: >
  Transfer your AI agent's personality, skills, memory, and soul from one platform to another.
  Supports Claude Code, Nanobot, OpenClaw, and Hermes agents. Use this skill whenever the user
  wants to: migrate their agent personality to a new platform, back up their agent's personal
  files to GitHub, clone someone else's agent persona, set up a new agent with an existing
  personality, or mentions "mind transposition", "心智迁移", "agent migration", "personality
  transfer", "soul transfer", "skill migration", "agent backup", or wants to replicate one agent's
  behavior in another. Also use when the user asks to export/import agent configuration, sync
  agent settings across platforms, or move their AI assistant's characteristics between tools.
---

# Mind Transposition

Your agent has a personality — shaped by the skills you've installed, the memory it has accumulated, the soul (system prompt / persona) you've crafted, and the history of your interactions. This skill transfers that personality from one agent platform to another, so a fresh agent becomes functionally identical to the one you've been using.

## How It Works

Mind Transposition is a two-step process:

1. **Export** — Run on the source agent. It collects all personal files (skills, memory, soul, history) and pushes them to a GitHub repository.
2. **Import** — Run on the target agent. It clones the repository and places files in the correct locations for its platform.

The skill auto-detects which platform it's running on and handles cross-platform file mapping (e.g., Claude Code's `CLAUDE.md` maps to OpenClaw's `SOUL.md`).

## Supported Platforms

| Platform | Config Directory | Soul File | Memory | Skills | History |
|----------|-----------------|-----------|--------|--------|---------|
| Claude Code | `~/.claude/` | `CLAUDE.md` | (in sessions) | `skills/` | `history.jsonl` |
| OpenClaw | `~/.openclaw/` | `SOUL.md` | `MEMORY.md` + `memory/` | `skills/` | sessions |
| Nanobot | `~/.nanobot/workspace/` | `SOUL.md` | `MEMORY.md` | skills in workspace | session logs |
| Hermes | `~/.hermes/` | `config.yaml` + skills | `memory/` | `skills/` | `sessions/` |

For detailed platform-specific file locations and cross-platform mapping rules, read `references/platforms.md`.

## Command Syntax

The skill accepts a command argument that determines the mode:

- `/mind-transposition export` — Export this agent's mind to GitHub
- `/mind-transposition import` — Import a mind from GitHub into this agent
- `/mind-transposition status` — Show what personal files exist on this agent and their sizes

If no argument is given, default to showing status and asking which operation the user wants.

---

## Workflow: Export

### Step 1: Detect Platform

Check which agent platform you're running on by probing for characteristic directories:

```
if ~/.claude/ exists → Claude Code
if ~/.openclaw/ exists → OpenClaw
if ~/.nanobot/ exists → Nanobot
if ~/.hermes/ exists → Hermes
```

If multiple platforms are detected, ask the user which one to export from. If none are detected, ask the user to specify.

### Step 2: Collect Personal Files

Based on the detected platform, collect files from these categories:

**Soul** (personality / system prompt):
- Claude Code: `CLAUDE.md` (both `~/.claude/CLAUDE.md` and any project-level `CLAUDE.md`)
- OpenClaw: `SOUL.md`, `AGENTS.md`, `IDENTITY.md`, `BOOTSTRAP.md`, `USER.md`
- Nanobot: `SOUL.md`, `AGENTS.md`, `USER.md`
- Hermes: `config.yaml` (persona-related sections)

**Memory** (persistent knowledge):
- Claude Code: Check for memory-related files in `~/.claude/` or project directories
- OpenClaw: `MEMORY.md`, all files in `memory/` directory
- Nanobot: `MEMORY.md`
- Hermes: all files in `memory/` directory

**Skills** (installed capabilities):
- Claude Code: all directories under `~/.claude/skills/` (each containing `SKILL.md`)
- OpenClaw: all directories under `~/.openclaw/skills/`
- Nanobot: skill files in the workspace
- Hermes: all directories under `~/.hermes/skills/` (exclude bundled skills that ship with fresh install)

**History** (interaction logs):
- Claude Code: `history.jsonl`
- OpenClaw: session data
- Nanobot: session logs
- Hermes: `sessions/` directory

**Settings** (user preferences):
- Claude Code: `settings.json`, `hooks.json`
- OpenClaw: configuration files
- Nanobot: workspace config
- Hermes: `config.yaml` (non-secret sections), `.env` (warn user about secrets)

### Step 3: Prepare the Migration Package

Create a temporary directory structure for the export:

```
mind-transposition-export/
├── manifest.json          # Platform info, file list, timestamps
├── soul/                  # Personality files
├── memory/                # Memory files
├── skills/                # Skill directories
├── history/               # History/logs
├── settings/              # Configuration files
└── cross-platform-map.json # Mapping hints for import
```

The `manifest.json` should contain:
```json
{
  "source_platform": "claude-code",
  "export_date": "2025-01-15T10:30:00Z",
  "version": "1.0",
  "files": {
    "soul": ["CLAUDE.md"],
    "memory": [],
    "skills": ["skill-creator", "mind-transposition"],
    "history": ["history.jsonl"],
    "settings": ["settings.json"]
  },
  "total_size_bytes": 1234567
}
```

The `cross-platform-map.json` should contain mapping hints:
```json
{
  "source_platform": "claude-code",
  "soul_file": "CLAUDE.md",
  "soul_target_mapping": {
    "openclaw": "SOUL.md",
    "nanobot": "SOUL.md",
    "hermes": "config.yaml"
  },
  "memory_format": "inline",
  "skills_format": "skill-directory"
}
```

**Important**: Before packaging, warn the user about any files that may contain sensitive information (API keys in `.env`, tokens in `auth.json`, etc.) and ask whether to exclude them.

### Step 4: Push to GitHub

1. Check if `gh` CLI is available. If not, ask the user to install it or provide an alternative approach.

2. Check if the user has a configured GitHub repository:
   - Look for environment variable `MIND_TRANSPOSITION_REPO` (format: `owner/repo-name`)
   - Ask the user if they have one

3. If no repo exists:
   - Offer to create a new private repository using `gh repo create`
   - Default name: `mind-transposition-<platform>-<date>`
   - Always create as **private** repo (these files contain personal data)

4. Clone or update the repository:
   - If the repo is fresh, initialize with a `README.md` explaining the contents
   - If the repo already has data (from a previous export), ask whether to overwrite or create a branch

5. Copy the export package into the repo and commit:
   ```
   git add .
   git commit -m "mind transposition: export from <platform> on <date>"
   git push
   ```

6. Report to the user:
   - Repository URL
   - Files exported (with sizes)
   - Any warnings about sensitive data
   - Instructions for running import on the target agent

---

## Workflow: Import

### Step 1: Detect Platform

Same detection logic as export. This determines where files will be placed.

### Step 2: Get Source Repository

1. Ask for the GitHub repository URL or `owner/repo` identifier
2. If `MIND_TRANSPOSITION_REPO` is set, offer to use that
3. Clone the repository to a temporary directory

### Step 3: Read the Manifest

Read `manifest.json` and `cross-platform-map.json` from the cloned repo to understand:
- What platform the export came from
- What files are included
- How to map them to the current platform

### Step 4: Cross-Platform File Mapping

This is the most important step. Files from one platform need to be adapted for another.

**Soul mapping** (the core personality transfer):

| Source → Target | Mapping Rule |
|-----------------|-------------|
| Claude Code `CLAUDE.md` → OpenClaw/Nanobot `SOUL.md` | Copy content directly. CLAUDE.md is already markdown personality instructions that map well to SOUL.md format. |
| OpenClaw `SOUL.md` → Claude Code `CLAUDE.md` | Copy content to `~/.claude/CLAUDE.md`. May need to strip OpenClaw-specific directives. |
| OpenClaw `AGENTS.md` → Claude Code | Merge relevant behavioral rules into `CLAUDE.md` or create as a separate reference. |
| Hermes `config.yaml` → Any | Extract persona-related sections and convert to markdown format for the target platform. |
| Any → Nanobot | Nanobot's simple markdown format accepts content from any platform with minimal adaptation. |

**Memory mapping**:
- If source has `MEMORY.md` and target also uses `MEMORY.md` (OpenClaw, Nanobot) — copy directly
- If source has memory as session history (Claude Code) and target uses `MEMORY.md` — extract key facts from history and compile into `MEMORY.md` format
- If source has `memory/` directory with dated files — copy the directory

**Skills mapping**:
- Most modern agent platforms use a `skills/` directory with subdirectories containing `SKILL.md` files
- Skills that are platform-specific (using tools only available on one platform) should be flagged with a warning
- Universal skills (pure markdown instructions) can be copied directly

**History mapping**:
- History formats are platform-specific and generally not portable
- Offer to import history as a reference file rather than active history
- For Claude Code, append a note in `CLAUDE.md` about the imported agent's background

### Step 5: Place Files

After mapping, place files in the correct locations for the detected platform. See `references/platforms.md` for exact paths.

**Always create backups** before overwriting any existing files. Use a timestamped backup:
```
~/.claude/backups/mind-transposition-<timestamp>/
```

### Step 6: Post-Import Verification

1. List all files that were placed, with their paths
2. Warn about any files that needed manual adaptation
3. Suggest the user restart their agent session for changes to take effect
4. List any platform-specific skills that may need manual adjustment

---

## Workflow: Status

Show the user what personal files their current agent has:

1. Detect the platform
2. For each category (soul, memory, skills, history, settings):
   - Show which files exist
   - Show file sizes
   - Show last modified dates
3. Summarize: total number of files, total size
4. Note any potential issues (missing files, very large files, files with potential secrets)

---

## Important Considerations

**Secrets and API keys**: Never upload files containing API keys, tokens, or other secrets to GitHub without explicit user consent. Always warn when `.env`, `auth.json`, `settings.local.json`, or similar files are detected. Default to excluding them.

**Backup before import**: Always back up the target agent's existing files before overwriting. The user might want to merge rather than replace.

**Cross-platform skill compatibility**: Skills written for one platform may reference tools or features not available on another. After import, review installed skills and flag any that may be incompatible.

**Git history**: The GitHub repository serves as both a transfer mechanism and a backup. Each export creates a commit, so the user can track how their agent's personality has evolved over time.

**Large files**: If memory or history files are very large (>10MB), warn the user and suggest trimming before export. GitHub has a 100MB file size limit.

**Private vs public repos**: Always default to private repositories. Agent personality files contain information about the user's work patterns, preferences, and potentially sensitive context.
