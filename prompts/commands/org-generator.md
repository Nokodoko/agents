---
description: "Onboard corporate clients onto the Datadog platform via Jira project scaffolding and Terraform infrastructure provisioning"
argument-hint: "--name <client-name> [--dry-run] [--dark-factory] [--location <jira-url>] [--dd-instance commercial|gov-cloud] [--dd-api-key <env-var>] [--dd-app-key <env-var>]"
---

# Org-Generator Agent

Orchestrates the full lifecycle of onboarding a corporate client onto the Datadog platform. Creates a Jira project as the system of record, scaffolds the deterministic ticket hierarchy, and generates Terraform infrastructure code for monitors, dashboards, integrations, and agent configurations.

## Agent

Invokes the **org-generator** agent defined at `prompts/org-generator.md` (model: opus).

## Usage

```
/org-generator --name <client-name> [FLAGS]
```

## Arguments

- `--name <client-name>`: Project name in kebab-case (e.g., `acme-corp`). Used for Jira project key and all Terraform resource naming. **Required.**

## Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--dry-run` | Generate all artifacts and run `terraform plan` only -- no `terraform apply` | `false` |
| `--dark-factory` | Full automation mode -- all gates auto-approve, Terraform applies unattended | `false` |
| `--location <jira-url>` | Jira instance URL | `eccoselect-sandbox.atlassian.net` |
| `--dd-instance <type>` | Datadog instance type: `commercial` or `gov-cloud` | `commercial` |
| `--dd-api-key <env-var>` | Environment variable name holding the Datadog API key | `TF_VAR_ecco_dd_api_key` |
| `--dd-app-key <env-var>` | Environment variable name holding the Datadog App key | `TF_VAR_ecco_dd_app_key` |

## Workflow

1. Collect client intake via questionnaire (project type, cloud providers, products, tagging)
2. Create Jira project (`DD-<CLIENT_NAME>`) as the system of record
3. Scaffold deterministic Jira ticket hierarchy (epics, stories, tasks) via `/jira-board`
4. Generate Terraform codebase at `~/datadog_terraform/<client-name>/` via `/org-generator-tf`
5. Run `terraform init` + `terraform plan` (saved to `<client-name>/plan.out`)
6. Apply Terraform (skipped when `--dry-run`; unattended when `--dark-factory`)
7. Generate end-user artifacts (conf.yaml, install scripts, runbooks)
8. Update Jira tickets and hand off to client

## Examples

```bash
# Interactive onboarding with defaults
/org-generator --name acme-corp

# Dry-run to validate without applying
/org-generator --name acme-corp --dry-run

# Fully unattended dry-run (CI/CD validation)
/org-generator --name acme-corp --dry-run --dark-factory

# GovCloud instance with custom credentials
/org-generator --name acme-corp --dd-instance gov-cloud \
  --dd-api-key TF_VAR_custom_api_key \
  --dd-app-key TF_VAR_custom_app_key

# Custom Jira instance with full automation
/org-generator --name acme-corp --dark-factory \
  --location my-org.atlassian.net
```

---

$ARGUMENTS
