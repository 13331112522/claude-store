# Platform Reference Guide

Detailed file locations and structures for each supported agent platform.

## Table of Contents

1. [Claude Code](#claude-code)
2. [OpenClaw](#openclaw)
3. [Nanobot](#nanobot)
4. [Hermes](#hermes)
5. [Cross-Platform Mapping Rules](#cross-platform-mapping-rules)

---

## Claude Code

Claude Code is Anthropic's official CLI agent. Configuration lives in `~/.claude/`.

### Directory Structure

```
~/.claude/
├── CLAUDE.md              # Global system prompt / persona definition
├── settings.json          # User settings (permissions, model, plugins)
├── settings.local.json    # Local-only settings overrides
├── skills/                # Installed skills
│   └── <skill-name>/
│       └── SKILL.md       # Skill definition
├── hooks.json             # Hook configurations
├── history.jsonl          # Conversation history (JSONL format)
├── projects/              # Project-specific settings
├── sessions/              # Session data
├── plugins/               # Plugin data
├── todos/                 # Todo list data
├── backups/               # Backup directory
├── plans/                 # Plan data
├── shell-snapshots/       # Shell state snapshots
└── debug/                 # Debug logs
```

Project-level `CLAUDE.md` files may also exist in project root directories.

### Soul File: `CLAUDE.md`

- Location: `~/.claude/CLAUDE.md` (global) and `<project>/CLAUDE.md` (per-project)
- Format: Markdown with free-form instructions
- Content: System-level instructions, behavioral guidelines, persona definition
- Loaded at the start of every session

### Memory

Claude Code does not have a dedicated persistent memory file. Memory is embedded in:
- `CLAUDE.md` (user may add memory sections manually)
- Session history in `history.jsonl`
- Skills may implement their own memory systems

### Skills

- Location: `~/.claude/skills/<skill-name>/SKILL.md`
- Format: Markdown with YAML frontmatter (name, description)
- Each skill is a directory containing at minimum a `SKILL.md` file
- Skills can also include `scripts/`, `references/`, and `assets/` subdirectories

### History

- File: `~/.claude/history.jsonl`
- Format: JSON Lines, one JSON object per line
- Contains conversation turns and tool usage

### Settings

- `settings.json`: Main settings (permissions, model choice, enabled plugins)
- `settings.local.json`: Local overrides (not synced)
- `hooks.json`: Hook definitions for tool call events

---

## OpenClaw

OpenClaw is a personal AI agent platform. Configuration lives in `~/.openclaw/`.

### Directory Structure

```
~/.openclaw/
├── SOUL.md        # Agent personality, voice, and tone
├── AGENTS.md      # Behavioral rules, task orchestration, sub-agent definitions
├── USER.md        # User profile, preferences, and context
├── MEMORY.md      # Long-term persistent memory (facts, decisions)
├── TOOLS.md       # Tool definitions and usage instructions
├── HEARTBEAT.md   # Scheduled/recurring task definitions (cron-like)
├── IDENTITY.md    # Agent identity and core attributes
├── BOOTSTRAP.md   # Initial setup and bootstrapping instructions
├── skills/        # Installed skills
│   └── <skill-name>/
│       └── SKILL.md
└── memory/        # Dated memory files
    └── YYYY-MM-DD.md
```

### Soul File: `SOUL.md`

- The primary personality definition — "where your agent's voice lives"
- Injected on every normal session, carrying significant weight in shaping behavior
- Format: Markdown with persona/tone/vibe definitions

### Memory

- `MEMORY.md`: Long-term durable memory, loaded at start of every session
- `memory/YYYY-MM-DD.md`: Date-stamped memory entries, used for session-level memory flush

### Skills

- Location: `~/.openclaw/skills/<skill-name>/SKILL.md`
- Format: Markdown with YAML frontmatter
- Loaded with precedence rules and optional gating

---

## Nanobot

Nanobot (by HKUDS) is an ultra-lightweight agent runtime. Configuration lives in `~/.nanobot/workspace/`.

### Directory Structure

```
~/.nanobot/
└── workspace/
    ├── SOUL.md        # Personality, tone, values, boundaries
    ├── AGENTS.md      # Operating rules, tool discipline, priorities
    ├── USER.md        # User profile & preferences
    ├── MEMORY.md      # Long-term memory (grows over sessions)
    └── skills/        # Skills directory (if present)
```

### Soul File: `SOUL.md`

- Defines personality, tone, values, and behavioral boundaries
- Read at the start of every session along with AGENTS.md and USER.md

### Memory

- `MEMORY.md`: Single file that grows as the agent works
- Seeded with starting information; agent appends to it based on rules in `AGENTS.md`
- File-first approach — flat markdown files instead of databases

### Skills

- Skills may be stored in the workspace or as separate modules
- Format follows the same pattern as OpenClaw (markdown-based)

---

## Hermes

Hermes (by NousResearch) is a self-improving AI agent. Configuration lives in `~/.hermes/`.

### Directory Structure

```
~/.hermes/
├── config.yaml        # Structured settings (providers, models, options)
├── .env               # Secrets & API keys
├── skills/            # All skills (bundled + Hub-installed + user-created)
│   └── <skill-name>/
│       └── SKILL.md
├── profiles/          # Multiple agent profiles
│   └── <workspace>/
│       ├── skills/
│       ├── config.yaml
│       └── ...
├── memory/            # Agent memory storage
├── sessions/          # Session history/state
├── gateway/           # Gateway state (Telegram, Discord, etc.)
├── auth.json          # Messaging gateway tokens
└── kanban/            # Task management state
```

### Soul / Configuration

- No dedicated `SOUL.md` file — persona is configured through `config.yaml`
- The config.yaml contains model selection, provider settings, and behavioral options
- Persona customization may be embedded in skills or config

### Memory

- Stored in `~/.hermes/memory/` directory
- Format depends on installed memory skills
- Can include task-centric categorization and tiered storage

### Skills

- Location: `~/.hermes/skills/<skill-name>/SKILL.md`
- Three sources: bundled (ship with Hermes), Hub-installed, user-created
- All mixed in the same directory — when exporting, try to identify user-created vs bundled
- Profiles can have their own isolated skills in `~/.hermes/profiles/<workspace>/skills/`

### History

- Stored in `~/.hermes/sessions/` directory

---

## Cross-Platform Mapping Rules

### Soul / Persona Mapping

| Source | Target | Action |
|--------|--------|--------|
| Claude Code `CLAUDE.md` | OpenClaw `SOUL.md` | Direct copy. Content is already markdown personality instructions. |
| Claude Code `CLAUDE.md` | Nanobot `SOUL.md` | Direct copy. Same rationale. |
| Claude Code `CLAUDE.md` | Hermes `config.yaml` | Extract key behavioral instructions and add as persona config section. May need format conversion. |
| OpenClaw `SOUL.md` | Claude Code `CLAUDE.md` | Direct copy to `~/.claude/CLAUDE.md`. Strip any OpenClaw-specific directives (like `memoryFlush`). |
| OpenClaw `SOUL.md` | Nanobot `SOUL.md` | Direct copy. Formats are nearly identical. |
| OpenClaw `AGENTS.md` | Any | Merge relevant behavioral rules into the target's soul file or create as separate reference. OpenClaw AGENTS.md contains task orchestration rules that may not map 1:1. |
| Nanobot `SOUL.md` | Any | Direct copy to target's soul file. Nanobot's format is the simplest and most portable. |
| Hermes `config.yaml` | OpenClaw/Nanobot `SOUL.md` | Extract persona-relevant sections from YAML and convert to markdown. |

### Memory Mapping

| Source | Target | Action |
|--------|--------|--------|
| OpenClaw `MEMORY.md` | Nanobot `MEMORY.md` | Direct copy |
| Nanobot `MEMORY.md` | OpenClaw `MEMORY.md` | Direct copy |
| Claude Code history | OpenClaw/Nanobot `MEMORY.md` | Parse `history.jsonl`, extract key facts, preferences, and decisions. Compile into `MEMORY.md` format with a note about the source. |
| Any `memory/` directory | Any `memory/` directory | Copy dated markdown files directly |
| Hermes `memory/` | OpenClaw/Nanobot `MEMORY.md` | Compile memory entries into a single `MEMORY.md` |

### Skills Mapping

All four platforms use a similar skills structure (`skills/<name>/SKILL.md` with YAML frontmatter). Skills can generally be copied directly between platforms with these caveats:

- Skills referencing platform-specific tools (e.g., Claude Code's `Bash` tool vs OpenClaw's tool ecosystem) may need adaptation
- Skills using MCP servers need the MCP configuration to be present on the target platform
- Hermes bundled skills should be excluded from export (they ship with fresh install)

### Settings Mapping

Settings are the least portable category — each platform has different configuration structures.

- **Do** copy: behavioral preferences, model preferences, persona-related settings
- **Do not** copy: API keys, tokens, absolute paths, platform-specific feature flags
- **Warn about**: any settings that might not have an equivalent on the target platform
