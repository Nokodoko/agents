---
name: scaffold
description: Generate complete Terraform directory structure for a client
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
argument-hint: "<client-name>"
---

# org-generator:scaffold

Generates a complete Terraform directory structure for a new client engagement. Creates ALL modules initially; pruning happens in a separate step.

## Usage

```
/org-generator:scaffold <client-name>
```

## Arguments

- `client-name`: The client identifier (kebab-case, e.g., `acme-corp`)

## Directory Structure Generated

```
~/datadog_terraform/<client-name>/
├── backend.tf              # S3 backend configuration
├── providers.tf            # Provider versions and configuration
├── variables.tf            # Client-specific variables
├── outputs.tf              # Key outputs
├── modules.tf              # Module instantiation
├── tags.tf                 # Tag definitions
├── notifications.tf        # Alert team definitions
├── README.md               # Auto-generated documentation
├── questionnaire.md        # Original questionnaire (preserved)
├── modules/
│   ├── api_keys/           # API key generation
│   │   ├── main.tf
│   │   └── variables.tf
│   ├── app_keys/           # App key generation
│   │   ├── main.tf
│   │   └── variables.tf
│   ├── roles/              # Standard role definitions
│   │   ├── main.tf
│   │   └── variables.tf
│   ├── teams/              # Team structure
│   │   ├── main.tf
│   │   └── variables.tf
│   ├── users/              # User management
│   │   ├── main.tf
│   │   └── variables.tf
│   ├── aws/                # AWS monitors (conditional)
│   │   ├── monitors.tf
│   │   ├── rds.tf
│   │   ├── alb.tf
│   │   ├── ecs.tf
│   │   ├── lambda.tf
│   │   └── variables.tf
│   ├── gcp/                # GCP monitors (conditional)
│   │   ├── monitors.tf
│   │   ├── cloudsql.tf
│   │   ├── gke.tf
│   │   └── variables.tf
│   ├── azure/              # Azure monitors (conditional)
│   │   ├── monitors.tf
│   │   ├── sql.tf
│   │   ├── aks.tf
│   │   └── variables.tf
│   ├── kube/               # Kubernetes monitors (conditional)
│   │   ├── monitors.tf
│   │   └── variables.tf
│   ├── generic/            # Generic host monitors
│   │   ├── cpu.tf
│   │   ├── memory.tf
│   │   ├── disk.tf
│   │   ├── network.tf
│   │   └── variables.tf
│   ├── synthetics/         # Synthetic tests (conditional)
│   │   ├── http.tf
│   │   ├── ssl.tf
│   │   └── variables.tf
│   ├── private_locations/  # Private locations (conditional)
│   │   ├── main.tf
│   │   └── variables.tf
│   ├── apm/                # APM configuration (conditional)
│   │   ├── main.tf
│   │   └── variables.tf
│   └── rum/                # RUM configuration (conditional)
│       ├── main.tf
│       └── variables.tf
├── installs/               # Agent installation scripts
│   ├── agent.md
│   └── install.sh
├── add_tags/               # Monitor tagging scripts
│   ├── __init__.py
│   ├── keys.py             # API/App key retrieval from env vars
│   ├── headers.py          # HTTP headers for Datadog API
│   ├── monitors.py         # Monitor listing and tagging functions
│   └── caller.py           # CLI entry point for tagging
├── scripts/dd_lib/         # Comprehensive Datadog API library
│   ├── __init__.py         # Package marker and documentation
│   ├── keys.py             # API/App key retrieval (TF_VAR pattern)
│   ├── headers.py          # HTTP headers with pagination
│   ├── api.py              # Base API operations
│   ├── monitors.py         # Monitor CRUD, tagging, downtimes
│   ├── downtimes.py        # Downtime management, duplicate checking
│   ├── tags.py             # Tag operations on monitors
│   ├── hosts.py            # Host listing, tagging, metrics
│   ├── events.py           # Event retrieval, monitor correlation
│   ├── logs.py             # Log search and retrieval
│   ├── users.py            # User listing and management
│   ├── roles.py            # Role and permission operations
│   ├── metrics.py          # Host metrics retrieval
│   ├── synthetics.py       # Synthetic test operations
│   ├── webhooks.py         # Webhook creation
│   ├── orgs.py             # Organization operations
│   ├── rum.py              # RUM operations
│   └── services.py         # Service catalog operations
└── k8s/                    # Kubernetes configs (conditional)
    └── private-location-worker.yaml
```

## Core Files Generated

### backend.tf

```hcl
terraform {
  required_providers {
    datadog = {
      source  = "Datadog/datadog"
      version = ">= 3.86.0"
    }
    aws = {
      source = "hashicorp/aws"
    }
  }
  backend "s3" {
    bucket  = "<client-name>-backend"
    key     = "<client-name>-backend/backend"
    region  = "us-east-1"
    encrypt = true
  }
}

provider "datadog" {
  api_key = var.<client_name>_api_key
  app_key = var.<client_name>_app_key
  api_url = var.api_url
}

provider "aws" {
  region = var.region
}
```

### variables.tf

```hcl
variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "<client_name>_api_key" {
  description = "Datadog API key. Set via TF_VAR_<client_name>_api_key"
  type        = string
  sensitive   = true
}

variable "<client_name>_app_key" {
  description = "Datadog App key. Set via TF_VAR_<client_name>_app_key"
  type        = string
  sensitive   = true
}

variable "api_url" {
  description = "Datadog API URL"
  type        = string
  default     = "https://api.datadoghq.com"
}
```

## Template Sources

Templates are sourced from:
```
~/agents/plugins/org-generator/templates/terraform/
```

## Add Tags Script

The `add_tags/` directory contains Python scripts for adding `id:<monitor_id>` tags to all Datadog monitors. This makes monitors easier to search and filter in the Datadog UI.

### Usage

```bash
cd ~/datadog_terraform/<client-name>
make tags          # Add id tags to monitors
make check-tags    # Show monitors without id tags (dry run)
make list-monitors # List all monitors
make tfaa          # terraform apply -auto-approve && make tags
```

### Environment Variables

The scripts use the same TF_VAR pattern as Terraform:
```bash
export TF_VAR_<client_name>_api_key="your-api-key"
export TF_VAR_<client_name>_app_key="your-app-key"
```

Falls back to `DD_API_KEY` and `DD_APP_KEY` if TF_VAR versions are not set.

## Example

```
/org-generator:scaffold acme-corp
```

This will create the full directory structure at `~/datadog_terraform/acme-corp/` with all modules populated from templates.

## DD_Lib Script Library

The `scripts/dd_lib/` directory contains a comprehensive Python library for Datadog API operations. This provides utilities beyond the basic tagging functionality in `add_tags/`.

### Available Modules

| Module | Description |
|--------|-------------|
| `keys.py` | API/App key retrieval using TF_VAR pattern with DD_*_KEY fallback |
| `headers.py` | HTTP headers for GET, POST, PUT, DELETE with pagination support |
| `api.py` | Base API operations and request helpers |
| `monitors.py` | Monitor CRUD, ID tagging, triggered monitor listing, downtimes |
| `downtimes.py` | Downtime management, duplicate checking, bulk operations |
| `tags.py` | Monitor tag operations and listing |
| `hosts.py` | Host listing, metrics, tag management |
| `events.py` | Event retrieval, monitor correlation |
| `logs.py` | Log search and aggregation |
| `users.py` | User listing and management |
| `roles.py` | Role and permission operations |
| `metrics.py` | Host and active metrics retrieval |
| `synthetics.py` | Synthetic test operations, private locations |
| `webhooks.py` | Webhook CRUD operations |
| `orgs.py` | Organization operations, usage summary |
| `rum.py` | RUM application management and event queries |
| `services.py` | Service catalog operations, APM/RUM service filtering |

### Usage Example

```python
import sys
sys.path.insert(0, "scripts/dd_lib")

import monitors
import downtimes

# List all triggered monitors
triggered = monitors.get_triggered_monitors(prt=True, limit=10)

# Add downtime for a recovered monitor
downtimes.add_downtime_one_scope("env:production", monitor_id=12345)

# Append id tags to all monitors
monitors.append_id_tag_to_tags()
```

### Environment Variables

Uses the same TF_VAR pattern as Terraform:
```bash
export TF_VAR_<client_name>_api_key="your-api-key"
export TF_VAR_<client_name>_app_key="your-app-key"
```

Falls back to `DD_API_KEY` and `DD_APP_KEY` if TF_VAR versions are not set.

### API Site Configuration

The library templates include a `{{SITE}}` placeholder that is replaced with the appropriate API domain based on the client's data residency:

| Data Residency | Site Value |
|---------------|-----------|
| US (default) | api.datadoghq.com |
| EU | api.datadoghq.eu |
| US3 | api.us3.datadoghq.com |
| US5 | api.us5.datadoghq.com |
| US Government | api.ddog-gov.com |
