# Hook-Based Plugin Development Guide

This guide documents lessons learned from building hook-based plugins for Claude Code, including critical registration details, input/output formats, and best practices.

## Table of Contents

1. [Hook Registration](#hook-registration)
2. [Hook Input Format](#hook-input-format)
3. [Hook Output Behavior](#hook-output-behavior)
4. [Error Handling](#error-handling)
5. [Desktop Notifications](#desktop-notifications)
6. [Shell Script Template](#shell-script-template)
7. [Testing & Verification](#testing--verification)
8. [Common Pitfalls](#common-pitfalls)

---

## Hook Registration

**CRITICAL**: Hooks are **NOT** registered via the plugin manifest (`plugin.json`). They must be added directly to `~/.claude/settings.json`.

### Configuration Structure

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/absolute/path/to/hook-script.sh"
          }
        ]
      }
    ]
  }
}
```

### Available Hook Events

| Event | When It Fires |
|-------|---------------|
| `SessionStart` | When a new Claude session begins |
| `UserPromptSubmit` | When user submits a prompt (before processing) |
| `PreToolUse` | Before a tool is executed |
| `PostToolUse` | After a tool completes |
| `SubagentStart` | When a subagent is spawned |
| `SubagentStop` | When a subagent terminates |

### Matcher Patterns

The `matcher` field filters when the hook runs:
- `""` (empty string) - matches all prompts/events
- `"terraform"` - matches prompts containing "terraform"
- Use regex patterns for complex matching

---

## Hook Input Format

Hooks receive JSON via **stdin** containing context about the triggering event.

### UserPromptSubmit Input

```json
{
  "session_id": "abc123-def456",
  "transcript_path": "/home/user/.claude/projects/project-name/session-id.jsonl",
  "cwd": "/current/working/directory",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "the user's prompt text"
}
```

### Parsing in Bash

```bash
INPUT=$(cat)
PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty')
CWD=$(echo "$INPUT" | jq -r '.cwd // empty')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty')
TRANSCRIPT=$(echo "$INPUT" | jq -r '.transcript_path // empty')
```

### Parsing with Fallback

For robustness when `jq` parsing fails:

```bash
PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty' 2>/dev/null || echo "$INPUT")
```

---

## Hook Output Behavior

How your hook communicates with Claude:

| Channel | Effect |
|---------|--------|
| **stdout** | Content injected as context to Claude (wrapped in tags) |
| **stderr** | Displayed to user as error message |
| **Exit 0** | Allow prompt to proceed normally |
| **Exit 2** | Block prompt from being processed |

### Injecting Context

Output to stdout gets wrapped and shown to Claude:

```bash
echo "<my-hook-context>"
echo "key: value"
echo "detected_patterns: foo, bar"
echo "</my-hook-context>"
```

### Blocking Prompts

```bash
echo "Blocking: dangerous operation detected" >&2
exit 2
```

---

## Error Handling

### Avoid `set -e`

The `set -e` option causes scripts to exit on any error, which can cause unexpected hook failures. Instead, use explicit error handling:

```bash
#!/bin/bash
set -uo pipefail  # Use these instead of -e

# Handle errors explicitly
result=$(some_command) || {
    echo "Warning: command failed" >&2
    result=""
}
```

### Non-Critical Commands

Use `|| true` for commands that may fail but shouldn't abort the hook:

```bash
# Pattern matching that may not find anything
MATCHES=$(echo "$PROMPT" | grep -oE 'pattern' || true)

# Optional notifications
notify-send "Hook" "Message" 2>/dev/null || true
```

### Safe jq Parsing

```bash
VALUE=$(echo "$INPUT" | jq -r '.field // empty' 2>/dev/null || echo "default")
```

---

## Desktop Notifications

### Using notify-send (libnotify)

```bash
notify-send -u normal -t 3000 "Title" "Body message"
```

Options:
- `-u` urgency: `low`, `normal`, `critical`
- `-t` timeout in milliseconds (3000 = 3 seconds)
- `-i` icon path (optional)

### Styling with dunst

To customize notification appearance, add rules to `~/.config/dunst/dunstrc`:

```ini
[my-hook-notifications]
    summary = "MY_HOOK*"
    frame_color = "#FFA500"
    background = "#1a1000"
    foreground = "#ffffff"
    timeout = 3
    urgency = normal
```

The `summary` field matches notification titles using glob patterns.

### Applying dunst Changes

```bash
killall dunst && dunst &
```

Or simply `dunstctl reload` on newer versions.

---

## Shell Script Template

See `/templates/hook.sh.template` for a complete working template. Key structure:

```bash
#!/bin/bash
set -uo pipefail

# Read input from stdin
INPUT=$(cat)

# Parse JSON fields with fallback
PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty' 2>/dev/null || echo "$INPUT")
CWD=$(echo "$INPUT" | jq -r '.cwd // empty' 2>/dev/null || echo ".")

# Detection function
detect_pattern() {
    local text="$1"
    if echo "$text" | grep -qE 'your-pattern-here'; then
        echo "detected-value"
        return 0
    fi
    return 1
}

# Main logic
main() {
    local detected
    detected=$(detect_pattern "$PROMPT" || echo "")

    if [ -n "$detected" ]; then
        # Optional notification
        notify-send -u normal -t 3000 "Hook Triggered" "Detected: $detected" 2>/dev/null || true

        # Output context for Claude
        echo "<hook-context>"
        echo "detected: $detected"
        echo "cwd: $CWD"
        echo "</hook-context>"
    fi

    # Exit 0 to allow prompt, exit 2 to block
    exit 0
}

main "$@"
```

---

## Testing & Verification

### 1. Manual Script Testing

```bash
# Test with sample input
echo '{"prompt": "terraform apply", "cwd": "/project"}' | ./hook.sh

# Test with empty prompt
echo '{"prompt": ""}' | ./hook.sh
```

### 2. Notification Testing

```bash
# Verify notifications work
notify-send "Test" "If you see this, notifications work"
```

### 3. Integration Testing

1. Add hook to `~/.claude/settings.json`
2. Start a **new** Claude session (hooks load at session start)
3. Enter a prompt that matches your hook's pattern
4. Verify:
   - Notification appears (if implemented)
   - Context is injected (check Claude's response)
   - No errors in stderr

### 4. Debug Mode

Add logging to troubleshoot:

```bash
LOG_FILE="/tmp/my-hook.log"
echo "$(date): Input: $INPUT" >> "$LOG_FILE"
echo "$(date): Detected: $detected" >> "$LOG_FILE"
```

---

## Common Pitfalls

### 1. Hook Not Triggering

- **Cause**: Hooks registered in plugin manifest instead of settings.json
- **Fix**: Move hook config to `~/.claude/settings.json`

### 2. Script Exits Unexpectedly

- **Cause**: Using `set -e` with commands that can fail
- **Fix**: Remove `-e`, use explicit error handling

### 3. Empty or Missing Context

- **Cause**: jq parsing errors silently failing
- **Fix**: Add `2>/dev/null || echo ""` fallback

### 4. Notifications Not Appearing

- **Cause**: `notify-send` not installed or display not set
- **Fix**: Install `libnotify`, ensure `$DISPLAY` is set

### 5. Hook Works in Terminal But Not Claude

- **Cause**: Different environment (PATH, shell, etc.)
- **Fix**: Use absolute paths, don't rely on shell aliases

### 6. Special Characters Breaking Parsing

- **Cause**: Prompts containing quotes, newlines, special chars
- **Fix**: Use `jq` for JSON parsing, quote variables properly

---

## Further Reading

- Claude Code hooks documentation
- [jq Manual](https://stedolan.github.io/jq/manual/)
- [Bash strict mode](http://redsymbol.net/articles/unofficial-bash-strict-mode/)
- dunst notification daemon documentation
