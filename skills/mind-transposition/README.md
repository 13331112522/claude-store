# Mind Transposition

> Transfer your AI agent's personality, skills, memory, and soul across platforms.

Your AI agent develops a unique personality over time — shaped by the skills you've installed, the memory it has accumulated, the soul (system prompt / persona) you've crafted, and the history of your interactions. Mind Transposition captures that essence and transfers it between platforms, so a fresh agent becomes functionally identical to the one you've been using.

## Features

- **Cross-Platform Support**: Transfer between Claude Code, OpenClaw, Nanobot, and Hermes
- **Complete Personality Export**: Captures soul, memory, skills, history, and settings
- **Intelligent File Mapping**: Automatically adapts files for the target platform's structure
- **GitHub Integration**: Secure private repository storage and version history
- **Zip Package Export**: Save agent mind as a local .zip file for air-gapped environments
- **Auto-Detection Import**: Automatically detects GitHub URLs or local zip files
- **Backup Protection**: Automatic timestamped backups before import
- **Security First**: Warns about secrets and sensitive data before export

## Supported Platforms

| Platform | Config | Soul File | Memory | Skills |
|----------|--------|-----------|--------|--------|
| Claude Code | `~/.claude/` | `CLAUDE.md` | Sessions | `skills/` |
| OpenClaw | `~/.openclaw/` | `SOUL.md` | `MEMORY.md` + `memory/` | `skills/` |
| Nanobot | `~/.nanobot/workspace/` | `SOUL.md` | `MEMORY.md` | workspace skills |
| Hermes | `~/.hermes/` | `config.yaml` | `memory/` | `skills/` |

## How It Works

Mind Transposition is a two-step process:

1. **Export** — Run on your source agent. It collects all personal files and delivers them via:
   - **GitHub repository** — Push to a private GitHub repo (default, requires gh CLI)
   - **Local zip file** — Package as a downloadable .zip file

2. **Import** — Run on your target agent. It accepts either:
   - GitHub repository URL or `owner/repo` identifier
   - Local zip file path (.zip extension)

The skill auto-detects the source type and platform, handling all cross-platform file mapping automatically.

## Installation

### Claude Code

```bash
# Clone this repository
git clone https://github.com/13331112522/claude-store.git

# Copy the skill to your Claude Code skills directory
cp -r claude-store/skills/mind-transposition ~/.claude/skills/
```

### Other Platforms

Copy the `mind-transposition` folder to your platform's skills directory:
- OpenClaw: `~/.openclaw/skills/`
- Nanobot: `~/.nanobot/workspace/skills/`
- Hermes: `~/.hermes/skills/`

## Usage

### Export Your Agent's Mind

```
/mind-transposition export
```

The skill will:
1. Detect your platform
2. Collect all personal files (soul, memory, skills, history, settings)
3. Ask for delivery method:
   - **GitHub**: Ask for repository details (or create a new private one)
   - **Zip file**: Prompt for output path (default: `~/mind-transposition-export-<timestamp>.zip`)
4. Create and deliver the migration package

**Delivery Options:**
- **GitHub** — Better for version history, remote access, and sharing between machines
- **Zip file** — Better for air-gapped environments, quick local backups, or when gh CLI is unavailable

### Import a Mind

```
/mind-transposition import
```

Provide either:
- GitHub repository URL (e.g., `username/agent-mind-backup` or `https://github.com/username/repo`)
- Local zip file path (e.g., `~/mind-transposition-export-2025-01-15.zip`)

The skill will:
1. Auto-detect source type (GitHub or zip file)
2. Detect your platform
3. Clone repository or extract zip file
4. Validate package structure (manifest.json required)
5. Map files to your platform's structure
6. Create a backup of existing files
7. Place files in the correct locations

### Check Status

```
/mind-transposition status
```

See what personal files exist on your current agent, their sizes, and last modified dates.

## What Gets Exported

### Soul (Personality)
- System prompts, persona definitions, behavioral guidelines
- Claude Code: `CLAUDE.md`
- OpenClaw/Nanobot: `SOUL.md`, `AGENTS.md`, `IDENTITY.md`
- Hermes: `config.yaml` persona sections

### Memory (Knowledge)
- Long-term memory, accumulated facts, preferences
- OpenClaw/Nanobot: `MEMORY.md`, `memory/` directory
- Hermes: `memory/` directory
- Claude Code: Session history extraction

### Skills (Capabilities)
- All installed skills with their definitions
- Platform-specific skills flagged for review
- Skills in `skills/` directories

### History (Context)
- Conversation logs, session data
- Platform-specific formats (adapted for target)

### Settings (Preferences)
- User preferences, behavioral settings
- API keys excluded by default

## Migration Package Structure

```
mind-transposition-export/
├── manifest.json              # Platform info, file list, timestamps
├── soul/                      # Personality files
├── memory/                    # Memory files
├── skills/                    # Skill directories
├── history/                   # History/logs
├── settings/                  # Configuration files
└── cross-platform-map.json    # Mapping hints for import
```

## Security Considerations

- **Private Repositories**: Always creates private GitHub repositories by default
- **Secret Detection**: Warns about API keys, tokens, and sensitive files
- **Backup Creation**: Timestamped backups before any file overwrites
- **User Consent**: Explicit confirmation before excluding sensitive data
- **Zip File Security**:
  - Validates zip structure before extraction (must contain manifest.json)
  - Rejects path traversal attempts (entries containing `../`)
  - Warns about suspiciously large files inside zip (>50MB)
- **Delivery Method Choice**:
  - GitHub: Better for version history and remote access
  - Zip: Better for air-gapped environments or when gh CLI unavailable

## Examples

### Migrate from Claude Code to OpenClaw

```bash
# On Claude Code (export)
/mind-transposition export
# Choose delivery method (GitHub or zip)

# On OpenClaw (import)
/mind-transposition import
# Provide: username/claude-code-mind (or ~/export.zip)
# Result: CLAUDE.md → SOUL.md, skills mapped correctly
```

### Backup Your Agent Personality

```bash
# GitHub backup (version history)
/mind-transposition export
# Choose GitHub → creates private repo with git history

# Local backup (quick, no GitHub account)
/mind-transposition export
# Choose Zip → saves to ~/mind-transposition-export-<timestamp>.zip
```

### Share Your Agent Setup

```bash
# Export and share via GitHub
/mind-transposition export
# Make GitHub repo public or share with specific users

# Export and share via zip
/mind-transposition export
# Choose zip → send the .zip file directly
# Recipient runs: /mind-transposition import
# Provides path to the downloaded .zip file
```

## Platform-Specific Notes

### Claude Code
- Project-level `CLAUDE.md` files are included
- Memory is extracted from `history.jsonl`
- Skills directory: `~/.claude/skills/`

### OpenClaw
- Multiple soul files (`SOUL.md`, `AGENTS.md`, `IDENTITY.md`)
- Memory in both `MEMORY.md` and `memory/` directory
- Memory flush rules respected

### Nanobot
- Simple markdown-based configuration
- Single `MEMORY.md` file
- Workspace-based skills

### Hermes
- YAML-based configuration
- Persona extracted from `config.yaml`
- Bundled vs user-created skills detected

## Architecture

Mind Transposition follows a pipeline architecture:

1. **Platform Detection**: Probes for characteristic directories
2. **File Collection**: Gathers files by category (soul, memory, skills, etc.)
3. **Package Creation**: Builds manifest and categorizes files
4. **Delivery**: GitHub repository push (or local zip)
5. **Import Processing**: Clone → Manifest Read → Cross-Platform Mapping → File Placement

For detailed platform-specific file locations and mapping rules, see [references/platforms.md](references/platforms.md).

## Contributing

Contributions are welcome! The skill is designed to be extensible:

- **Add Platform Support**: Extend platform detection and file mapping
- **Improve Mappings**: Enhance cross-platform file conversion
- **Add Features**: Encrypted storage, cloud provider integration, etc.

## License

MIT License — See [LICENSE](LICENSE) for details.

## Links

- [GitHub Repository](https://github.com/13331112522/claude-store)
- [Skill Definition](SKILL.md)
- [Platform Reference](references/platforms.md)

---

**Note**: Mind Transposition is designed for backing up and transferring your own agent configurations. Always review imported files before activating, especially when importing from third-party sources.
