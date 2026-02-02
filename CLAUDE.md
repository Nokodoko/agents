# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository serves two purposes:
1. **Code review agents** - Specialized sub-agents for code review (Code Reviewer, Security Reviewer, Tech Lead, UX Reviewer, Code Simplifier)
2. **Claude Code plugin marketplace** - A collection of plugins and a plugin generator for scaffolding new plugins

## Architecture

```
agents/
├── agents/                 # Agent prompt definitions (model + system prompt)
├── commands/               # Slash commands that invoke agents
├── plugins/                # Claude Code plugins
│   ├── code-review-agents/ # Plugin exposing review commands
│   └── plugin_generator/   # Plugin scaffolding tool
├── settings/               # User settings (LSP, MCP, hooks)
├── .claude-plugin/         # Marketplace registry
├── config.json             # Agent metadata (name, model, prompt_file)
└── run_agent.py            # CLI helper for agent invocation
```

### Plugin Structure

Each plugin follows this structure:
```
plugin-name/
├── .claude-plugin/plugin.json   # Required: Plugin manifest
├── commands/                    # Optional: /plugin-name:command-name
├── skills/                      # Optional: Auto-invoked by model
├── agents/                      # Optional: Sub-agent definitions
└── hooks/                       # Optional: Event handlers
```

## Slash Commands

Review commands are defined in `commands/` and exposed via the code-review-agents plugin:

| Command | Agent | Model |
|---------|-------|-------|
| `/code-review <target>` | code_reviewer | sonnet |
| `/security-review <target>` | security_reviewer | opus |
| `/tech-lead <target>` | tech_lead | opus |
| `/ux-review <target>` | ux_reviewer | haiku |
| `/code-simplify <target>` | code_simplifier | haiku |
| `/review-all <target>` | All five agents in parallel | mixed |

## Helper Script

```bash
python run_agent.py --list                    # List available agents
python run_agent.py code_reviewer ./src/      # Get Task config for one agent
python run_agent.py --all ./src/              # Get Task configs for all agents
```

## Adding a New Agent

1. Create prompt file in `agents/<agent_name>.md` with frontmatter:
   ```markdown
   # Agent Name
   **Model:** sonnet|opus|haiku
   ## System Prompt
   <prompt content>
   ```
2. Add entry to `config.json` under `agents`
3. Create corresponding command in `commands/<command-name>.md`

## Plugin Generator

Create new plugins interactively:
```
/plugin-generator:generate [plugin-name]
```

Plugins are installed to `~/.claude/plugins/` and optionally registered in `.claude-plugin/marketplace.json`.

## Model Selection

- **opus**: Deep reasoning - security analysis, architecture decisions
- **sonnet**: Balanced - code review, moderate complexity
- **haiku**: Fast - simple transformations, focused tasks
