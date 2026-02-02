---
description: "List and run specialized code review agents"
argument-hint: "[AGENT_NAME] [TARGET]"
---

# Code Review Agents

Available agents and their specializations:

## Usage

```
/agents                           # Show this help
/agents code-review ./src         # Run code reviewer on ./src
/agents security ./src/auth.py    # Run security reviewer
/agents tech-lead ./              # Run tech lead review
/agents simplify ./utils.py       # Run code simplifier
/agents ux ./components/          # Run UX reviewer
/agents all ./src                 # Run ALL agents
```

## Available Agents

| Agent | Model | Focus |
|-------|-------|-------|
| `code-review` | sonnet | DRY, Unix philosophy, extensibility, decoupling |
| `security` | opus | Vulnerabilities, OWASP, attack surface |
| `tech-lead` | opus | Architecture, technical debt, risk |
| `simplify` | haiku | Reduce complexity, remove dead code |
| `ux` | haiku | Accessibility, interaction design |
| `all` | mixed | Run all agents in sequence |

---

Based on user input "$ARGUMENTS", determine which agent to run:

- If no arguments or "help": Display the usage information above
- If first argument matches an agent name: Run that agent's review on the target path
- If "all": Run all agents sequentially on the target

For each agent review, use the Task tool with:
- `model`: As specified in the table above
- `subagent_type`: "general-purpose"
- The full agent prompt from the agents repository

Target: $ARGUMENTS
