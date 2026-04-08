# Obsidian CLI Command Reference

Complete reference for all Obsidian CLI commands (Obsidian 1.12.4+).

## General

| Command | Description |
|---------|-------------|
| `obsidian version` | Show Obsidian version |
| `obsidian help [command]` | Display help for a command |
| `obsidian reload` | Reload the app window (dangerous) |
| `obsidian restart` | Restart the application (dangerous) |

## Vault

| Command | Description |
|---------|-------------|
| `obsidian vault` | Show current vault info |
| `obsidian vaults` | List known vaults (desktop only) |

Multi-vault usage: prefix any command with `vault="VaultName"`.

## Files and Folders

| Command | Description |
|---------|-------------|
| `obsidian file file="path"` | Show file info (defaults to active file) |
| `obsidian files` | List all files in vault |
| `obsidian folder file="path"` | Show folder info |
| `obsidian folders` | List all folders |
| `obsidian open file="path"` | Open a file in Obsidian |
| `obsidian create name="path" content="text"` | Create or overwrite a file |
| `obsidian create name="path" template="TemplateName"` | Create from template |
| `obsidian read file="path"` | Read file contents (defaults to active file) |
| `obsidian append file="path" content="text"` | Append content to end of file |
| `obsidian prepend file="path" content="text"` | Insert content after frontmatter |
| `obsidian move file="path" to="newpath"` | Move or rename (auto-updates wikilinks) |
| `obsidian rename file="path" to="newname"` | Rename a file |
| `obsidian delete file="path"` | Delete file (moves to trash) |
| `obsidian delete file="path" permanent` | Permanently delete (bypasses trash) |

## Search

| Command | Description |
|---------|-------------|
| `obsidian search query="text"` | Full-text search, returns matching file paths |
| `obsidian search:context query="text" limit=N` | Search with matching line context (grep-style) |
| `obsidian search:open` | Open search view in GUI |

## Links

| Command | Description |
|---------|-------------|
| `obsidian links file="path"` | List outgoing links from a file |
| `obsidian backlinks file="path"` | List backlinks to a file |
| `obsidian unresolved` | List unresolved links in vault |
| `obsidian orphans` | List files with no incoming links |
| `obsidian deadends` | List files with no outgoing links |

## Tags

| Command | Description |
|---------|-------------|
| `obsidian tags` | List all tags in vault |
| `obsidian tag tag="#tagname"` | List files with a specific tag |
| `obsidian tags:rename old="tag1" new="tag2"` | Bulk rename a tag across vault |

## Tasks

| Command | Description |
|---------|-------------|
| `obsidian tasks` | List all tasks in vault |
| `obsidian task` | Show or update a task |

## Properties (Frontmatter)

| Command | Description |
|---------|-------------|
| `obsidian properties file="path"` | List properties on a file |
| `obsidian property:read file="path" name="prop"` | Read a property value |
| `obsidian property:set file="path" name="prop" value="val"` | Set a property |
| `obsidian property:remove file="path" name="prop"` | Remove a property |
| `obsidian aliases` | List aliases in vault |

## Daily Notes

| Command | Description |
|---------|-------------|
| `obsidian daily` | Open today's daily note (creates if missing) |
| `obsidian daily:path` | Get daily note file path |
| `obsidian daily:read` | Read daily note contents |
| `obsidian daily:append content="text"` | Append to daily note |
| `obsidian daily:prepend content="text"` | Prepend to daily note |

## Outline

| Command | Description |
|---------|-------------|
| `obsidian outline file="path"` | Show headings for a file |

## Templates

| Command | Description |
|---------|-------------|
| `obsidian templates` | List templates |
| `obsidian template:read file="path"` | Read template content |
| `obsidian template:insert` | Insert template into active file |

## Bookmarks

| Command | Description |
|---------|-------------|
| `obsidian bookmarks` | List bookmarks |
| `obsidian bookmark file="path"` | Add a bookmark |

## Bases

| Command | Description |
|---------|-------------|
| `obsidian bases` | List all base files |
| `obsidian base:views` | List views in current base |
| `obsidian base:query` | Query a base and return results |
| `obsidian base:create` | Create a new item in a base |

## Word Count

| Command | Description |
|---------|-------------|
| `obsidian wordcount file="path"` | Count words and characters |

## Random Notes

| Command | Description |
|---------|-------------|
| `obsidian random` | Open a random note |
| `obsidian random:read` | Read a random note |

## Plugins

| Command | Description |
|---------|-------------|
| `obsidian plugins` | List installed plugins |
| `obsidian plugins:enabled` | List enabled plugins |
| `obsidian plugin id="name"` | Get plugin info |
| `obsidian plugin:enable id="name"` | Enable a plugin |
| `obsidian plugin:disable id="name"` | Disable a plugin |
| `obsidian plugin:install id="name"` | Install a community plugin |
| `obsidian plugin:uninstall id="name"` | Uninstall a plugin |
| `obsidian plugin:reload id="name"` | Reload a plugin (dev) |
| `obsidian plugins:restrict` | Toggle restricted mode (dangerous) |

## Themes

| Command | Description |
|---------|-------------|
| `obsidian themes` | List installed themes |
| `obsidian theme` | Show active theme info |
| `obsidian theme:set name="ThemeName"` | Set active theme |
| `obsidian theme:install name="ThemeName"` | Install a theme |
| `obsidian theme:uninstall name="ThemeName"` | Uninstall a theme |

## CSS Snippets

| Command | Description |
|---------|-------------|
| `obsidian snippets` | List CSS snippets |
| `obsidian snippets:enabled` | List enabled snippets |
| `obsidian snippet:enable name="name"` | Enable a snippet |
| `obsidian snippet:disable name="name"` | Disable a snippet |

## Tabs and Workspaces

| Command | Description |
|---------|-------------|
| `obsidian tabs` | List open tabs |
| `obsidian tab:open file="path"` | Open a new tab |
| `obsidian recents` | List recently opened files |
| `obsidian workspace` | Show workspace tree |
| `obsidian workspaces` | List saved workspaces |
| `obsidian workspace:save name="name"` | Save current layout |
| `obsidian workspace:load name="name"` | Load a saved workspace |
| `obsidian workspace:delete name="name"` | Delete a saved workspace |

## Commands & Hotkeys

| Command | Description |
|---------|-------------|
| `obsidian commands` | List available command IDs |
| `obsidian command id="cmdid"` | Execute an Obsidian command (dangerous) |
| `obsidian hotkeys` | List hotkeys for all commands |
| `obsidian hotkey id="cmdid"` | Get hotkey for a command |

## File History

| Command | Description |
|---------|-------------|
| `obsidian diff file="path"` | Compare file versions |
| `obsidian history file="path"` | List versions from file recovery |
| `obsidian history:list` | List all files with local history |
| `obsidian history:read file="path"` | Read a local history version |
| `obsidian history:restore file="path"` | Restore a local history version |
| `obsidian history:open` | Open file recovery UI |

## Sync

| Command | Description |
|---------|-------------|
| `obsidian sync` | Pause or resume sync |
| `obsidian sync:status` | Show sync status |
| `obsidian sync:history file="path"` | List sync versions for a file |
| `obsidian sync:read file="path"` | Read a sync version |
| `obsidian sync:restore file="path"` | Restore a sync version |
| `obsidian sync:open file="path"` | Open sync history in GUI |
| `obsidian sync:deleted` | List deleted files in sync |

## Publish

| Command | Description |
|---------|-------------|
| `obsidian publish:site` | Show publish site info |
| `obsidian publish:list` | List published files |
| `obsidian publish:status` | List publish changes |
| `obsidian publish:add file="path"` | Publish a file |
| `obsidian publish:remove file="path"` | Unpublish a file |
| `obsidian publish:open file="path"` | Open file on published site |

## Developer (all dangerous, require `allowDangerousCommands`)

| Command | Description |
|---------|-------------|
| `obsidian devtools` | Toggle Electron dev tools |
| `obsidian eval code="JS expression"` | Execute JavaScript, return result |
| `obsidian dev:console` | Show captured console messages |
| `obsidian dev:errors` | Show captured JS errors |
| `obsidian dev:screenshot` | Take screenshot (returns base64 PNG) |
| `obsidian dev:dom` | Query DOM elements |
| `obsidian dev:css` | Inspect CSS with source locations |
| `obsidian dev:mobile` | Toggle mobile emulation |
| `obsidian dev:debug` | Attach/detach CDP debugger |
| `obsidian dev:cdp` | Run a CDP command |

## Output Formats

Many commands support `format=` parameter:

| Format | Use Case |
|--------|----------|
| `json` | Pipe through `jq` |
| `csv` / `tsv` | Spreadsheet export |
| `md` | Markdown format |
| `paths` | File paths only (for piping) |
| `text` | Human-readable (default) |
| `tree` | Folder hierarchy |
| `yaml` | YAML format (default for properties) |

## Common Patterns

```bash
# Search and pipe to jq
obsidian search query="TODO" format=json | jq '.[].file'

# Bulk move tagged files
obsidian tag tag="#archive" format=paths | xargs -I{} obsidian move file="{}" to="Archive/"

# Bulk set properties
obsidian files format=paths | while read -r f; do
  obsidian property:set file="$f" name="status" value="review"
done

# Copy note content to clipboard
obsidian read file="note" --copy

# Vault health check
obsidian orphans
obsidian unresolved
obsidian deadends
```

## TUI Mode

Run `obsidian` with no arguments to launch interactive TUI:

| Key | Action |
|-----|--------|
| Arrow keys | Select file |
| `/` | Filter by filename |
| `Enter` | Open in Obsidian |
| `n` | Create new note |
| `d` | Delete file |
| `r` | Rename |
| `Ctrl+R` | Search command history |
| `q` | Quit |
