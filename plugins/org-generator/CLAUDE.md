# CLAUDE.md

This file provides guidance to Claude Code when working with the org-generator plugin.

## Overview

The org-generator plugin generates Datadog Terraform infrastructure for new client POC engagements and production setups. It automates the creation of:

- S3 backends for Terraform state
- Datadog Terraform directory structures
- Monitors based on client infrastructure
- Standard roles and team structures
- Synthetic tests and private locations
- Datadog agent configurations and deployment documentation

## Plugin Structure

```
org-generator/
├── .claude-plugin/plugin.json    # Plugin manifest
├── .mcp.json                     # MCP server config
├── .lsp.json                     # LSP server config
├── CLAUDE.md                     # This file
├── commands/
│   ├── generate.md               # Entry point - generates questionnaire
│   ├── apply.md                  # Processes questionnaire, orchestrates setup
│   ├── backend.md                # Creates S3 backend
│   ├── scaffold.md               # Generates terraform structure
│   ├── prune.md                  # Removes unused modules
│   ├── validate.md               # Validates environment and terraform
│   ├── monitors.md               # Generates monitors from questionnaire
│   └── agent.md                  # Generates Datadog agent configurations
├── skills/
│   ├── generate/SKILL.md         # Auto-detects new client setup
│   └── questionnaire/SKILL.md    # Helps fill questionnaires
├── hooks/
│   └── terraform-context.sh      # Detects terraform blocks
├── templates/
│   ├── questionnaire/
│   │   └── client-questionnaire.md
│   ├── terraform/
│   │   ├── backend.tf.tpl
│   │   ├── providers.tf.tpl
│   │   ├── variables.tf.tpl
│   │   ├── outputs.tf.tpl
│   │   ├── modules.tf.tpl
│   │   ├── tags.tf.tpl
│   │   ├── notifications.tf.tpl
│   │   ├── Makefile.tpl              # Make targets for terraform + tagging
│   │   ├── add_tags/                 # Monitor tagging scripts
│   │   │   ├── __init__.py
│   │   │   ├── keys.py
│   │   │   ├── headers.py
│   │   │   ├── monitors.py
│   │   │   └── caller.py
│   │   ├── scripts/dd_lib/           # Comprehensive Datadog API library
│   │   │   ├── __init__.py
│   │   │   ├── keys.py
│   │   │   ├── headers.py
│   │   │   ├── api.py
│   │   │   ├── monitors.py
│   │   │   ├── downtimes.py
│   │   │   ├── tags.py
│   │   │   ├── hosts.py
│   │   │   ├── events.py
│   │   │   ├── logs.py
│   │   │   ├── users.py
│   │   │   ├── roles.py
│   │   │   ├── metrics.py
│   │   │   ├── synthetics.py
│   │   │   ├── webhooks.py
│   │   │   ├── orgs.py
│   │   │   ├── rum.py
│   │   │   └── services.py
│   │   └── modules/
│   │       ├── api_keys/
│   │       ├── app_keys/
│   │       ├── roles/
│   │       ├── teams/
│   │       ├── users/
│   │       ├── aws/
│   │       ├── gcp/
│   │       ├── azure/
│   │       ├── kube/
│   │       ├── generic/
│   │       ├── synthetics/
│   │       ├── private_locations/
│   │       ├── apm/
│   │       └── rum/
│   ├── k8s/
│   │   └── private-location-worker.yaml
│   └── agent/
│       ├── datadog.yaml.tpl      # Main agent configuration
│       ├── conf.d/               # Integration configurations
│       │   ├── custom_logs.yaml.tpl
│       │   ├── http_check.yaml.tpl
│       │   ├── tcp_check.yaml.tpl
│       │   ├── process.yaml.tpl
│       │   ├── nginx.yaml.tpl
│       │   ├── mysql.yaml.tpl
│       │   ├── postgres.yaml.tpl
│       │   ├── redis.yaml.tpl
│       │   ├── kafka.yaml.tpl
│       │   └── rabbitmq.yaml.tpl
│       └── docs/                 # Deployment documentation
│           ├── README.md.tpl
│           ├── linux-host.md.tpl
│           ├── windows-host.md.tpl
│           ├── kubernetes.md.tpl
│           ├── docker.md.tpl
│           ├── ecs.md.tpl
│           └── fargate.md.tpl
└── lib/
    ├── questionnaire-parser.py   # Parses questionnaire markdown
    ├── monitor-generator.py      # Generates monitors from config
    └── agent-generator.py        # Generates agent configs from questionnaire
```

## Commands

### /org-generator:generate <client-name>

Entry point for new client setup. Generates a questionnaire at `~/datadog_terraform/<client-name>/questionnaire.md`.

### /org-generator:apply <client-name>

Processes a completed questionnaire and orchestrates the full setup:
1. Parse questionnaire
2. Create S3 backend
3. Scaffold terraform structure
4. Prune unused modules
5. Validate environment
6. Generate monitors

### /org-generator:backend <client-name>

Creates the S3 backend bucket at `<client-name>-backend` in `~/Portfolio/aws/`.

### /org-generator:scaffold <client-name>

Generates the full Terraform directory structure with all modules.

### /org-generator:prune <client-name>

Removes unused modules based on questionnaire selections.

### /org-generator:validate <client-name>

Validates:
- S3 backend exists
- Environment variables set (TF_VAR_<client>_api_key, TF_VAR_<client>_app_key)
- Terraform init/validate succeeds

### /org-generator:monitors <client-name>

Generates monitors for selected infrastructure components.

### /org-generator:agent <client-name>

Generates Datadog agent configuration files including:
- `datadog.yaml` - Main agent configuration with correct site, APM, process collection
- `conf.d/` - Integration configs (nginx, mysql, postgres, redis, kafka, rabbitmq, etc.)
- `docs/` - Deployment documentation for Linux, Windows, Kubernetes, Docker, ECS, Fargate

## Workflow

1. User runs `/org-generator:generate acme-corp`
2. Plugin creates questionnaire at `~/datadog_terraform/acme-corp/questionnaire.md`
3. User fills out questionnaire
4. User runs `/org-generator:apply acme-corp`
5. Plugin creates backend, scaffolds, prunes, validates, generates monitors
6. Plugin generates agent configurations in `datadog-agent/` directory

## Environment Variables

Client credentials use the TF_VAR pattern:

```bash
export TF_VAR_acme_corp_api_key="your-api-key"
export TF_VAR_acme_corp_app_key="your-app-key"
```

Note: Hyphens in client names become underscores in variable names.

## Template Variables

Templates use these placeholders:
- `{{CLIENT_NAME}}` - kebab-case client name (e.g., acme-corp)
- `{{CLIENT_NAME_UNDERSCORE}}` - underscore version (e.g., acme_corp)
- `{{DATE}}` - Current date
- `{{SITE}}` - Datadog site based on data residency (datadoghq.com, datadoghq.eu, etc.)
- `{{APM_ENABLED}}` - true/false based on APM selection
- `{{HOSTS_ENABLED}}` - true/false based on hosts selection
- `{{CONTAINERS_ENABLED}}` - true/false based on containers selection

## Reference Patterns

Based on `~/datadog_terraform/forest/terraform/`:
- Uses `for_each` pattern for dynamic resource creation
- S3 backend following `{client}-backend` naming
- Consistent tagging: `managed_by:terraform`, `platform:*`, `application_team:*`
- Monitor message templates with `{{#is_alert}}` / `{{#is_recovery}}` blocks

## Standard Roles

| Role | Permissions |
|------|-------------|
| Admin | Full access |
| Standard User | Create/edit monitors, dashboards |
| Read-Only User | View only |
| Monitor-Only User | Manage monitors only |
| Dashboard-Read-Only | View dashboards only |
| Dashboard-Write User | Create/edit dashboards |

## Monitor Categories

### Always Generated
- Generic (CPU, memory, disk, network)

### Conditional
- AWS (EC2, RDS, ALB, ECS, Lambda)
- GCP (Compute, Cloud SQL, GKE)
- Azure (VMs, SQL, AKS, App Service)
- Kubernetes (deployments, pods, nodes)
- APM (error rates, latency)
- RUM (Core Web Vitals)

## Library Scripts

### questionnaire-parser.py

```bash
python lib/questionnaire-parser.py ~/datadog_terraform/acme-corp/questionnaire.md --output json
python lib/questionnaire-parser.py <path> --dry-run  # Preview pruning
```

### monitor-generator.py

```bash
python lib/questionnaire-parser.py <questionnaire> | \
  python lib/monitor-generator.py - --output-dir ~/datadog_terraform/acme-corp/modules/
```

### agent-generator.py

```bash
python lib/questionnaire-parser.py <questionnaire> | \
  python lib/agent-generator.py - --output-dir ~/datadog_terraform/acme-corp/datadog-agent/
```

## Add Tags Script

The plugin generates a `add_tags/` directory with Python scripts that add `id:<monitor_id>` tags to all Datadog monitors. This makes monitors easier to search and filter in the Datadog UI.

### Generated Files

```
~/datadog_terraform/<client-name>/
├── Makefile                # Terraform + tagging make targets
└── add_tags/
    ├── __init__.py
    ├── keys.py             # API/App key retrieval from env vars
    ├── headers.py          # HTTP headers for Datadog API
    ├── monitors.py         # Monitor listing and tagging functions
    └── caller.py           # CLI entry point
```

### Make Targets

| Target | Description |
|--------|-------------|
| `make tags` | Add id tags to monitors that don't have them |
| `make check-tags` | Show monitors without id tags (dry run) |
| `make list-monitors` | List all monitors with their tags |
| `make tfaa` | terraform apply -auto-approve && make tags |
| `make apply-target MODULE=aws` | Apply specific module and run tagging |

### Direct Usage

```bash
cd ~/datadog_terraform/acme-corp/add_tags
python caller.py append      # Add id tags
python caller.py check       # Show monitors without id tags
python caller.py list        # List all monitors
```

### Environment Variables

Uses the TF_VAR pattern (falls back to DD_API_KEY/DD_APP_KEY):
```bash
export TF_VAR_acme_corp_api_key="your-api-key"
export TF_VAR_acme_corp_app_key="your-app-key"
```

## Data Residency Support

The plugin supports different Datadog sites based on data residency requirements:

| Selection | Site Value |
|-----------|-----------|
| US (default) | datadoghq.com |
| EU | datadoghq.eu |
| US3 | us3.datadoghq.com |
| US5 | us5.datadoghq.com |
| US Government (GovCloud) | ddog-gov.com |

## Agent Configuration Output

When `/org-generator:agent` is run, it generates:

```
~/datadog_terraform/<client-name>/datadog-agent/
├── datadog.yaml              # Main agent configuration
├── conf.d/
│   ├── custom_logs.yaml      # Log collection
│   ├── process.yaml          # Process monitoring
│   ├── http_check.yaml       # HTTP checks (if web servers)
│   ├── tcp_check.yaml        # TCP checks (if databases/queues)
│   └── <service>.yaml        # Service-specific (nginx, mysql, etc.)
└── docs/
    ├── README.md             # Quick start guide
    ├── linux-host.md         # Linux installation
    ├── windows-host.md       # Windows installation (if selected)
    ├── kubernetes.md         # K8s DaemonSet (if containers)
    ├── docker.md             # Docker deployment (if Docker)
    ├── ecs.md                # ECS task definition (if ECS)
    └── fargate.md            # Fargate sidecar (if Fargate)
```

## DD_Lib API Library

The plugin generates a comprehensive `scripts/dd_lib/` directory containing Python modules for Datadog API operations. This provides utilities beyond the basic tagging functionality in `add_tags/`.

### Generated Structure

```
~/datadog_terraform/<client-name>/scripts/dd_lib/
├── __init__.py         # Package marker and documentation
├── keys.py             # API/App key retrieval (TF_VAR pattern)
├── headers.py          # HTTP headers with pagination
├── api.py              # Base API operations
├── monitors.py         # Monitor CRUD, tagging, downtimes
├── downtimes.py        # Downtime management, duplicate checking
├── tags.py             # Monitor tag operations
├── hosts.py            # Host listing, tagging, metrics
├── events.py           # Event retrieval, monitor correlation
├── logs.py             # Log search and aggregation
├── users.py            # User listing and management
├── roles.py            # Role and permission operations
├── metrics.py          # Host and active metrics retrieval
├── synthetics.py       # Synthetic test operations, private locations
├── webhooks.py         # Webhook CRUD operations
├── orgs.py             # Organization operations, usage summary
├── rum.py              # RUM application management
└── services.py         # Service catalog operations
```

### Key Functions

| Module | Functions |
|--------|-----------|
| `monitors.py` | `list_monitors()`, `append_id_tag_to_tags()`, `get_triggered_monitors()`, `add_downtime()` |
| `downtimes.py` | `get_all_downtimes()`, `delete_downtime()`, `check_for_duplicate()`, `add_downtime_one_scope()` |
| `hosts.py` | `get_hosts()`, `total_active_hosts()`, `add_host_tag_key_value()`, `delete_host_tags()` |
| `events.py` | `get_events()`, `get_monitor_id_from_event()` |
| `logs.py` | `log_search()`, `get_logs()`, `log_aggregate()` |
| `roles.py` | `get_roles()`, `get_permissions()`, `get_role_templates()` |
| `synthetics.py` | `get_synthetics()`, `list_all_tests()`, `get_private_locations()` |
| `rum.py` | `get_rum_applications()`, `create_rum_application()`, `aggregate_rum_events()` |
| `services.py` | `get_services()`, `get_apm_services()`, `get_rum_services()` |

### Usage Example

```python
import sys
sys.path.insert(0, "scripts/dd_lib")

import monitors
import downtimes
import hosts

# List triggered monitors
triggered = monitors.get_triggered_monitors(prt=True, limit=10)

# Add downtime with duplicate checking
downtimes.get_all_downtimes_duplicate_checker(12345, "env:production")

# Get total active hosts
total = hosts.total_active_hosts()
print(total)  # up:150, active:145
```

### Template Variables

Templates use these placeholders (replaced during scaffold):
- `{{SITE}}` - API base URL domain (api.datadoghq.com, api.datadoghq.eu, api.ddog-gov.com)
- `{{CLIENT_NAME_UNDERSCORE}}` - Client name with underscores for TF_VAR pattern

## Development Notes

- Templates use `.tpl` extension for clarity
- Module templates are complete Terraform files (not templates)
- Python scripts require Python 3.10+
- Hook script requires bash
- dd_lib import warnings are expected (templates reference local modules)
