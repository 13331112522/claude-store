# Mind Transposition: Zip Package Feature Design

**Date:** 2025-01-15
**Status:** Design Complete
**Author:** Claude (with user collaboration)

## Overview

Add a zip package delivery option to the mind-transposition skill, allowing users to export agent personality (soul, memory, skills, history, settings) to a local zip file instead of (or in addition to) GitHub repositories. Import will auto-detect whether the source is a GitHub URL or a local zip file.

## Architecture

The zip package feature adds a parallel export path alongside the existing GitHub push. The core export logic (collecting files, creating the package structure with manifest.json, cross-platform-map.json, and categorized directories) remains unchanged. What changes is the "delivery" layer — instead of `gh` CLI + git operations, we use Python's `zipfile` module for local file packaging.

For import, we add a source detection layer that routes to either git clone (GitHub) or zip extraction (local file). Both paths converge on the same manifest parsing and cross-platform file mapping logic.

**Data Flow:**

```
EXPORT:
Platform Detection → Collect Files → Prepare Package Structure
                                          ↓
                              ┌───────────┴───────────┐
                         GitHub Push        Zip Package
                         (existing)         (new)

IMPORT:
User Input → Source Detector ──┬──> Git Clone → Manifest Read
                               │
                               └──> Zip Extract → Manifest Read
                                       ↓
                              Cross-Platform Mapping → Place Files
```

## Export Workflow Changes

### Modified Export Flow

After the export package directory is prepared (`mind-transposition-export/` with manifest.json, soul/, memory/, skills/, etc.), the user is prompted:

```
Export package ready. How would you like to deliver it?
1. Push to GitHub repository (requires gh CLI)
2. Save as local zip file
```

### Zip Export Implementation

For option 2 (local zip file):

1. **Prompt for output path:** Ask user: "Enter zip file destination path (or press Enter for default: ~/mind-transposition-export-<timestamp>.zip)"
2. **Validate path:** Check directory exists and is writable, resolve to absolute path
3. **Create zip archive:** Use `zipfile` with `ZIP_DEFLATED` compression, walk the prepared directory tree
4. **Verify integrity:** Basic validation that zip was created and contains expected files (at minimum manifest.json)
5. **Report results:** Show final path, file size, and files included

### Code Structure

```python
def create_zip_package(export_dir: str, output_path: str) -> str:
    """Create zip archive from prepared export directory."""
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(export_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, export_dir)
                zipf.write(file_path, arcname)
    return output_path
```

The GitHub path remains unchanged from the current implementation — this is purely additive.

## Import Workflow Changes

### Modified Import Flow with Auto-Detection

When the user runs `/mind-transposition import`, the source detection determines the delivery method:

### Detection Logic

1. If input starts with `http://`, `https://`, or matches GitHub owner/repo pattern (`username/repo-name`) → GitHub path
2. If input is a valid local file path ending in `.zip` → Zip extraction path
3. If input exists but isn't a zip → Error: "Not a valid zip file"
4. If input doesn't match either pattern → Ask user: "Is this a GitHub repository or local zip file path?"

### Zip Import Implementation

1. **Extract to temp directory:** `unzip <file> -d <temp_dir>` or Python's `zipfile.extractall()`
2. **Validate structure:** Check for `manifest.json` at root level — if missing, error: "Invalid mind transposition package (missing manifest.json)"
3. **Read manifest and map:** Same cross-platform mapping logic as GitHub path
4. **Proceed with placement:** Continue with existing file placement workflow

### Code Structure

```python
def detect_source_type(source: str) -> str:
    """Auto-detect if source is GitHub repo or local zip."""
    if source.startswith(('http://', 'https://')) or '/' in source:
        return 'github'
    if os.path.exists(source) and source.endswith('.zip'):
        return 'zip'
    return 'unknown'
```

The rest of the import flow (manifest parsing, cross-platform mapping, file placement, backup creation) remains shared between both paths.

## Package Structure

The zip file contains **identical structure** to the GitHub export:

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

No wrapper folder or additional files — the zip root directly contains the exported structure.

## Error Handling

### Zip Creation Errors

- **Disk space:** Check available space before zipping, warn if insufficient
- **File permissions:** Catch permission errors, suggest alternative location
- **Large files:** Warn if individual files > 50MB (Zip64 may be needed) or total package > 500MB
- **Integrity:** Verify created zip can be opened ( zipfile.testzip() )

### Zip Extraction Errors

- **Corrupted zip:** `BadZipFile` exception → "Package is corrupted or incomplete"
- **Wrong structure:** No manifest.json found → "Not a valid mind transposition package"
- **Version mismatch:** Manifest version unsupported → "Package version X not supported (current: Y)"
- **Path traversal:** Reject zip entries containing `../` to prevent security issues

### Import Source Detection Edge Cases

- **Ambiguous input:** User provides just a name like "my-backup" → ask to clarify
- **Both exist:** A GitHub repo AND a local zip with same name → ask which to use
- **Neither valid:** Clear error message with examples of valid inputs

### User Experience Considerations

- Progress feedback for large operations (especially zipping many skill files)
- Clear "what to do next" guidance after successful export/import
- Preserve existing GitHub export as default behavior for backward compatibility

## Testing Considerations

### Unit Tests

- `create_zip_package()` — Test with empty, single-file, and multi-file directories
- `detect_source_type()` — Test GitHub URLs, owner/repo strings, local zip paths, invalid inputs
- Zip validation — Test corrupted zips, missing manifest, malformed JSON
- Cross-platform mapping — Verify zip import produces same result as GitHub import from identical manifest

### Integration Test Scenarios

1. Round-trip: Export to zip → Import from zip → Verify file contents match
2. Cross-platform: Claude Code export to zip → Import to OpenClaw (mock platform detection)
3. Large packages: Test with skills containing many files (>100 files, >50MB)
4. GitHub vs Zip parity: Export same agent twice (once GitHub, once zip) → Compare manifests

### Manual Testing Checklist

- Export to custom path with spaces in name
- Import from zip in different locations (home dir, Desktop, etc.)
- Cancel operation mid-zip (Ctrl+C) — verify cleanup
- Export with existing file at destination (overwrite prompt)

### Platform-Specific Testing

- Windows paths (backslashes) in zip entries
- macOS resource forks (._ files) — should be excluded
- Linux permissions preservation in zip

## Implementation Files

**Files to Modify:**
- [skills/mind-transposition/SKILL.md](../skills/mind-transposition/SKILL.md) — Update command syntax and workflow documentation

**Files to Create:**
- Core implementation logic (if this skill has an implementation script)

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| User-specified output path | Maximum flexibility for user workflow |
| Auto-detection for import | Unified interface, simpler mental model |
| Identical structure to GitHub | Reuse validation/mapping logic, easier testing |
| No wrapper folder in zip | Simpler extraction, direct mapping to GitHub export structure |

## Next Steps

Ready to set up for implementation?
