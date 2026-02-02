#!/usr/bin/env python3
"""
Agent Runner - Invokes review agents on specified files or directories.

Usage:
    python run_agent.py <agent_name> <target_path> [--all]

Examples:
    python run_agent.py code_reviewer ./src/app.py
    python run_agent.py security_reviewer ./src/
    python run_agent.py --all ./src/  # Run all agents

Available agents:
    - code_reviewer    : Architecture, DRY, Unix philosophy, extensibility
    - code_simplifier  : Complexity reduction, dead code removal
    - security_reviewer: Vulnerability detection, OWASP analysis
    - tech_lead        : Strategic oversight, technical debt, risk analysis
    - ux_reviewer      : Accessibility, interaction design, responsive patterns
"""

import json
import sys
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / "config.json"


def load_config():
    """Load agent configuration from config.json."""
    with open(CONFIG_PATH) as f:
        return json.load(f)


def load_agent_prompt(prompt_file: str) -> str:
    """Load the agent's system prompt from its markdown file."""
    prompt_path = SCRIPT_DIR / prompt_file
    with open(prompt_path) as f:
        content = f.read()

    # Extract just the prompt content (skip the header with model info)
    lines = content.split('\n')
    prompt_lines = []
    in_prompt = False

    for line in lines:
        if line.startswith('## System Prompt'):
            in_prompt = True
            continue
        if in_prompt:
            prompt_lines.append(line)

    return '\n'.join(prompt_lines).strip()


def list_agents(config: dict) -> None:
    """Print available agents and their descriptions."""
    print("\nAvailable Agents:")
    print("-" * 60)
    for agent_id, agent in config["agents"].items():
        print(f"\n  {agent_id}")
        print(f"    Model: {agent['model']}")
        print(f"    {agent['description']}")
    print()


def get_agent_info(config: dict, agent_name: str) -> dict:
    """Get agent configuration by name."""
    if agent_name not in config["agents"]:
        print(f"Error: Unknown agent '{agent_name}'")
        list_agents(config)
        sys.exit(1)
    return config["agents"][agent_name]


def format_task_command(agent: dict, target: str) -> dict:
    """Format the agent invocation for Claude Code Task tool."""
    prompt = load_agent_prompt(agent["prompt_file"])

    return {
        "description": f"{agent['name']} review",
        "prompt": f"{prompt}\n\n---\n\nPlease review the following target: {target}",
        "model": agent["model"],
        "subagent_type": "general-purpose"
    }


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    config = load_config()

    # Handle --list flag
    if sys.argv[1] == "--list":
        list_agents(config)
        sys.exit(0)

    # Handle --all flag
    if sys.argv[1] == "--all":
        if len(sys.argv) < 3:
            print("Error: Please specify a target path")
            print("Usage: python run_agent.py --all <target_path>")
            sys.exit(1)

        target = sys.argv[2]
        print(f"\nRunning all agents on: {target}\n")

        for agent_id, agent in config["agents"].items():
            task = format_task_command(agent, target)
            print(f"Agent: {agent['name']}")
            print(f"  Model: {task['model']}")
            print(f"  Target: {target}")
            print(f"  Task config: {json.dumps(task, indent=2)}")
            print("-" * 40)

        sys.exit(0)

    # Standard single agent invocation
    if len(sys.argv) < 3:
        print("Error: Please specify agent name and target path")
        print("Usage: python run_agent.py <agent_name> <target_path>")
        list_agents(config)
        sys.exit(1)

    agent_name = sys.argv[1]
    target = sys.argv[2]

    agent = get_agent_info(config, agent_name)
    task = format_task_command(agent, target)

    print(f"\nAgent: {agent['name']}")
    print(f"Model: {task['model']}")
    print(f"Target: {target}")
    print(f"\nTask configuration for Claude Code:")
    print(json.dumps(task, indent=2))


if __name__ == "__main__":
    main()
