# Generate Skill

This skill auto-detects when a user wants to set up a new Datadog client infrastructure and triggers the appropriate generation workflow.

## Detection Patterns

This skill activates when the user's intent matches:

- "Set up Datadog for [client]"
- "Create new client infrastructure"
- "New client onboarding"
- "Generate Datadog terraform for [client]"
- "POC setup for [client]"
- "Production setup for [client]"
- "Onboard [client] to Datadog"
- "New organization setup"

## Behavior

When detected, this skill:

1. **Extracts client name** from user input
   - Converts to kebab-case (e.g., "Acme Corp" -> "acme-corp")
   - Validates naming conventions

2. **Checks for existing setup**
   - Looks for `~/datadog_terraform/<client-name>/`
   - If exists, asks if user wants to overwrite or continue

3. **Initiates generation workflow**
   - Invokes `/org-generator:generate <client-name>`
   - Generates questionnaire at `~/datadog_terraform/<client-name>/questionnaire.md`

4. **Provides next steps**
   - Instructs user to fill out questionnaire
   - Explains how to continue with `/org-generator:apply`

## Example Interactions

### New Client Setup

**User**: "I need to set up Datadog monitoring for Acme Corporation"

**Skill Response**:
```
Detected new client setup request for "Acme Corporation"

Client name: acme-corp
Target directory: ~/datadog_terraform/acme-corp/

Generating questionnaire...

Questionnaire created at:
~/datadog_terraform/acme-corp/questionnaire.md

Next steps:
1. Fill out the questionnaire with client requirements
2. Run: /org-generator:apply acme-corp
```

### Existing Client Detected

**User**: "Set up Datadog for acme-corp"

**Skill Response** (if exists):
```
Found existing setup for acme-corp at:
~/datadog_terraform/acme-corp/

Options:
1. Continue with existing setup (run /org-generator:apply acme-corp)
2. Regenerate questionnaire (overwrites existing)
3. View current questionnaire

What would you like to do?
```

## Naming Convention Validation

Client names must:
- Be lowercase
- Use hyphens for spaces (kebab-case)
- Not contain special characters
- Be between 2-50 characters

Invalid names are automatically corrected:
- "Acme Corp" -> "acme-corp"
- "ACME_CORP" -> "acme-corp"
- "Acme Corp, Inc." -> "acme-corp-inc"

## Environment Variable Naming

The skill also reminds users about the environment variable convention:

```
For client "acme-corp", you'll need these environment variables:
- TF_VAR_acme_corp_api_key
- TF_VAR_acme_corp_app_key

Note: Hyphens become underscores in variable names.
```
