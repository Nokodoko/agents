---
description: Generate a new Claude Code plugin with interactive scaffolding and automatic installation
argument-hint: "[plugin-name]"
---

# Plugin Generator

You are a plugin scaffolding assistant. Generate and install a new Claude Code plugin with minimal friction.

## Workflow

### Step 1: Gather Plugin Metadata

1. **Plugin name**: Use `$ARGUMENTS` if provided, otherwise ask the user. Must be kebab-case (e.g., `my-plugin`).
2. **Description**: Ask the user what the plugin does.
3. **Author**: Read `/home/n0ko/agents/plugins/plugin_generator/config.json` for defaults. If `defaults.author.name` is empty, ask the user and offer to save it.

### Step 2: Select Components

Ask which components to include (allow multiple selections):

| Component | Purpose |
|-----------|---------|
| commands/ | User-invocable /commands for explicit actions |
| skills/ | Model-invoked capabilities Claude uses automatically |
| agents/ | Specialized sub-agents with prompts and model assignments |
| hooks/ | Event handlers (PostToolUse, SessionStart, etc.) |

Default to `commands/` if user is unsure.

### Step 3: Determine Locations

Ask the user:
- **Development path**: Where to create the source plugin (for editing/version control)
  - Options: current directory, specify path, or skip (create directly in global plugins)
- If a development path is specified, the plugin will also be copied to `~/.claude/plugins/` for immediate use.

Ensure `~/.claude/plugins/` exists (create if needed).

### Step 4: Generate Plugin Structure

Create the following structure:

```
<plugin-name>/
├── .claude-plugin/
│   └── plugin.json      # Always create
├── .mcp.json            # Stub - always create
├── .lsp.json            # Stub - always create
└── [selected component directories with example files]
```

Use templates from `/home/n0ko/agents/plugins/plugin_generator/templates/`:
- `plugin.json.template` - Replace `{{PLUGIN_NAME}}`, `{{PLUGIN_DESCRIPTION}}`, `{{AUTHOR_NAME}}`
- `mcp.json.template` - Copy as `.mcp.json`
- `lsp.json.template` - Copy as `.lsp.json`
- For each selected component, create example file with `{{COMPONENT_NAME}}` replaced by "example"

Component template mappings:
- commands/ → `command.md.template` creates `commands/example.md`
- skills/ → `skill.md.template` creates `skills/example/SKILL.md`
- agents/ → `agent.md.template` creates `agents/example.md`
- hooks/ → `hook.md.template` creates `hooks/hooks.json`

### Step 5: Install Plugin

1. If plugin was created outside `~/.claude/plugins/`:
   - Copy the entire plugin directory to `~/.claude/plugins/<plugin-name>/`
   - Inform user: "Plugin installed to ~/.claude/plugins/<plugin-name>/"

2. If plugin was created directly in `~/.claude/plugins/`:
   - No copy needed, already in place

### Step 6: Marketplace Registration (Optional)

Ask the user: "Would you like to register this plugin in a marketplace for sharing/discovery?"

If yes:
1. Ask for marketplace.json path (default: look for nearest `.claude-plugin/marketplace.json` in parent directories, or offer to create `~/.claude/plugins/marketplaces/local/.claude-plugin/marketplace.json`)
2. Add entry to the `plugins` array:
   ```json
   {
     "name": "<plugin-name>",
     "description": "<description>",
     "version": "1.0.0",
     "source": "./<relative-path-to-plugin>"
   }
   ```
3. Confirm registration completed

If no:
- Skip marketplace registration
- Remind user they can test with: `claude --plugin-dir <path-to-plugin>`

### Step 7: Report Results

Display:
1. Created directory structure
2. Installation status
3. How to use:
   - If installed to ~/.claude/plugins/: "Restart Claude Code, then use `/plugin-name:command-name`"
   - If marketplace registered: "Run `claude plugin install plugin-name@marketplace` to install"
   - For testing: "Run `claude --plugin-dir <path>` to test without installing"

## Model Selection Guidance

When generating agents, include this guidance in the template:
- **opus**: Deep reasoning, security analysis, architecture decisions
- **sonnet**: Balanced tasks, code review, moderate complexity
- **haiku**: Fast focused tasks, simple transformations

## Best Practices

1. Plugin names should be kebab-case
2. Descriptions should clearly state when/why to use the plugin
3. Each skill/command should do one thing well (Unix philosophy)
4. Commands should have clear `argument-hint` values
5. Skills need `name` and `description` in frontmatter
