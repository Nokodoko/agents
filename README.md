# Claude Code Agents & Plugins

A collection of specialized agents, plugins, and tooling for [Claude Code](https://claude.ai/code).

## Features

### Code Review Agents

Five specialized sub-agents for comprehensive code review:

| Command | Agent | Model | Purpose |
|---------|-------|-------|---------|
| `/code-review <target>` | Code Reviewer | sonnet | Code quality, DRY, architecture |
| `/security-review <target>` | Security Reviewer | opus | OWASP vulnerabilities, threat analysis |
| `/tech-lead <target>` | Tech Lead | opus | Architecture, tech debt, risk assessment |
| `/ux-review <target>` | UX Reviewer | haiku | Accessibility, error handling, responsive design |
| `/code-simplify <target>` | Code Simplifier | haiku | Reduce complexity, remove dead code |
| `/review-all <target>` | All agents | mixed | Run all five in parallel |

### Plugin Generator

Scaffold new Claude Code plugins interactively:

```
/plugin-generator:generate [plugin-name]
```

Creates plugins with:
- Commands (slash commands)
- Skills (auto-invoked capabilities)
- Agents (sub-agent definitions)
- Hooks (event handlers)

## Directory Structure

```
agents/
├── agents/                 # Agent prompt definitions
├── commands/               # Slash commands that invoke agents
├── plugins/                # Claude Code plugins
│   ├── code-review-agents/ # Plugin exposing review commands
│   └── plugin_generator/   # Plugin scaffolding tool
├── settings/               # User settings (LSP, MCP, hooks)
├── .claude-plugin/         # Marketplace registry
├── config.json             # Agent metadata
└── run_agent.py            # CLI helper for agent invocation
```

## Installation

### Via Claude Code Plugin Manager

```bash
# Install code review agents
claude plugin install code-review-agents@agents

# Install plugin generator
claude plugin install plugin-generator@agents
```

### Manual Installation

Copy to your plugins directory:

```bash
cp -r plugins/plugin_generator ~/.claude/plugins/
cp -r plugins/code-review-agents ~/.claude/plugins/
```

## Usage

### Running Review Agents

```bash
# In a Claude Code session
/code-review ./src/
/security-review ./api/
/review-all ./project/
```

### Creating New Plugins

```bash
/plugin-generator:generate my-awesome-plugin
```

### CLI Helper

```bash
python run_agent.py --list                    # List available agents
python run_agent.py code_reviewer ./src/      # Get Task config for one agent
python run_agent.py --all ./src/              # Get Task configs for all agents
```

## Adding New Agents

1. Create prompt file in `agents/<agent_name>.md`:
   ```markdown
   # Agent Name
   **Model:** sonnet|opus|haiku
   ## System Prompt
   <prompt content>
   ```

2. Add entry to `config.json` under `agents`

3. Create command in `commands/<command-name>.md`

## Model Selection Guide

- **opus**: Deep reasoning - security analysis, architecture decisions
- **sonnet**: Balanced - code review, moderate complexity
- **haiku**: Fast - simple transformations, focused tasks

## Documentation

- [Hook Development Guide](plugins/plugin_generator/docs/HOOKS_GUIDE.md) - Building hook-based plugins

## License

MIT
