# Mind Transposition

> Transfer your AI agent's personality, skills, memory, and soul across platforms.

Your AI agent develops a unique personality over time — shaped by the skills you've installed, the memory it has accumulated, the soul (system prompt / persona) you've crafted, and the history of your interactions. Mind Transposition captures that essence and transfers it between platforms, so a fresh agent becomes functionally identical to the one you've been using.

## Features

- **Cross-Platform Support**: Transfer between Claude Code, OpenClaw, Nanobot, and Hermes
- **Complete Personality Export**: Captures soul, memory, skills, history, and settings
- **Intelligent File Mapping**: Automatically adapts files for the target platform's structure
- **GitHub Integration**: Secure private repository storage and version history
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

1. **Export** — Run on your source agent. It collects all personal files and creates a migration package on GitHub.
2. **Import** — Run on your target agent. It clones the package, maps files for the target platform, and places them in the correct locations.

The skill auto-detects which platform it's running on and handles all cross-platform file mapping automatically.

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
3. Ask for GitHub repository details (or create a new private one)
4. Push the migration package to GitHub

### Import a Mind

```
/mind-transposition import
```

Provide the GitHub repository URL (e.g., `username/agent-mind-backup`), and the skill will:
1. Detect your platform
2. Clone the migration package
3. Map files to your platform's structure
4. Create a backup of existing files
5. Place files in the correct locations

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

## Examples

### Migrate from Claude Code to OpenClaw

```bash
# On Claude Code (export)
/mind-transposition export
# Creates: github.com/username/claude-code-mind

# On OpenClaw (import)
/mind-transposition import
# Provide: username/claude-code-mind
# Result: CLAUDE.md → SOUL.md, skills mapped correctly
```

### Backup Your Agent Personality

```bash
/mind-transposition export
# Creates a timestamped backup on GitHub
# Track personality evolution through git history
```

### Clone Someone's Agent Setup

```bash
# Share your GitHub repo with someone
# They run import on their platform
/mind-transposition import
# Provide: shared-repo-name
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
- **Add Features**: Zip export, encrypted storage, etc.

## License

MIT License — See [LICENSE](LICENSE) for details.

## Links

- [GitHub Repository](https://github.com/13331112522/claude-store)
- [Skill Definition](SKILL.md)
- [Platform Reference](references/platforms.md)

---

**Note**: Mind Transposition is designed for backing up and transferring your own agent configurations. Always review imported files before activating, especially when importing from third-party sources.
