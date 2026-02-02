# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Plugin Generator scaffolds and installs Claude Code plugins with minimal friction. Run `/plugin-generator:generate` to create a new plugin that's immediately usable.

## Usage

```
/plugin-generator:generate [plugin-name]
```

The command will:
1. Prompt for plugin name, description, and components
2. Generate plugin structure with templates
3. Copy to `~/.claude/plugins/` for immediate use
4. Optionally register in a marketplace for sharing

## Testing During Development

```bash
claude --plugin-dir /home/n0ko/agents/plugins/plugin_generator
```

## Installation

The plugin is registered in the `agents` marketplace. To install:

```bash
claude plugin install plugin-generator@agents
```

Or via the interactive plugin manager: `/plugin` → Install → select `plugin-generator@agents`

## Plugin Structure

```
plugin_generator/
├── .claude-plugin/plugin.json   # Plugin manifest
├── commands/
│   └── generate.md              # /plugin-generator:generate command
├── templates/                   # Scaffolding templates
└── config.json                  # Author defaults
```

## Configuration

Edit `config.json` to set defaults:
```json
{
  "defaults": {
    "author": { "name": "Your Name" },
    "global_plugin_path": "~/.claude/plugins/",
    "marketplace_search_paths": [".claude-plugin/marketplace.json"]
  }
}
```

## Generated Plugin Structure

```
<plugin-name>/
├── .claude-plugin/plugin.json   # Plugin manifest
├── .mcp.json                    # MCP server config stub
├── .lsp.json                    # LSP server config stub
├── commands/                    # If selected
├── skills/                      # If selected
├── agents/                      # If selected
└── hooks/                       # If selected
```

## Installation Flow

1. **Development copy**: Created at user-specified path (for version control)
2. **Installed copy**: Copied to `~/.claude/plugins/` (for immediate use)
3. **Marketplace**: Optionally registered for discovery/sharing

## Template Placeholders

- `{{PLUGIN_NAME}}` - kebab-case identifier
- `{{PLUGIN_DESCRIPTION}}` - Plugin description
- `{{AUTHOR_NAME}}` - Author name
- `{{COMPONENT_NAME}}` - Component name (defaults to "example")
- `{{EVENT_TYPE}}` - Hook event type (hooks only)
- `{{HOOK_PATH}}` - Absolute path to hook installation (hooks only)

## Hook Development

**IMPORTANT**: Hooks have unique registration requirements. See `docs/HOOKS_GUIDE.md` for:

- Hook registration (must be in `~/.claude/settings.json`, NOT plugin manifest)
- Input/output formats and exit codes
- Error handling best practices
- Desktop notification integration
- Testing and debugging tips

Key points:
- Hooks receive JSON via stdin, not environment variables
- Use `set -uo pipefail` (avoid `set -e`)
- stdout injects context to Claude, exit 2 blocks prompts
