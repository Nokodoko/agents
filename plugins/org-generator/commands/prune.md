---
name: prune
description: Remove unused modules and resources based on questionnaire responses
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
argument-hint: "<client-name>"
---

# org-generator:prune

Removes unused modules, resources, and configurations based on questionnaire responses. This keeps the codebase lean and avoids confusion.

## Usage

```
/org-generator:prune <client-name>
```

## Arguments

- `client-name`: The client identifier (kebab-case, e.g., `acme-corp`)

## Prerequisites

1. Questionnaire must be parsed (run after /org-generator:scaffold)
2. Full terraform structure must exist at `~/datadog_terraform/<client-name>/`

## Pruning Logic

Based on questionnaire answers, the following are conditionally removed:

| Questionnaire Answer | Modules/Files Removed |
|---------------------|----------------------|
| Cloud: NOT AWS | `modules/aws/`, AWS integrations in modules.tf |
| Cloud: NOT GCP | `modules/gcp/`, GCP integrations in modules.tf |
| Cloud: NOT Azure | `modules/azure/`, Azure integrations in modules.tf |
| Containers: NO | `modules/kube/`, `k8s/` directory |
| Serverless: NO | Lambda/Cloud Functions monitors |
| APM: NO | `modules/apm/`, APM variables |
| RUM: NO | `modules/rum/`, RUM variables |
| Synthetics: NO | `modules/synthetics/`, synthetic variables |
| Private Locations: NO | `modules/private_locations/`, `k8s/` worker configs |
| Message Queues: NO | RabbitMQ/Kafka monitors |
| Databases: NOT RDS | RDS-specific monitors in aws module |
| Databases: NOT Cloud SQL | Cloud SQL monitors in gcp module |
| Databases: NOT Azure SQL | Azure SQL monitors in azure module |

## Pruning Steps

### Step 1: Parse Configuration

Read the parsed questionnaire configuration from previous step or re-parse `questionnaire.md`.

### Step 2: Identify Unused Modules

Build a list of modules to remove based on:
- Cloud providers not selected
- Infrastructure components not selected
- Services not needed

### Step 3: Remove Module Directories

```bash
# Example: Remove GCP module if not selected
rm -rf ~/datadog_terraform/<client-name>/modules/gcp/
```

### Step 4: Update modules.tf

Remove module instantiation blocks for pruned modules:

```hcl
# REMOVE this block if GCP not selected
module "gcp_monitors" {
  source = "./modules/gcp/"
  # ...
}
```

### Step 5: Update variables.tf

Remove variables only used by pruned modules:

```hcl
# REMOVE if GCP not selected
variable "gcp_project_id" {
  description = "GCP Project ID"
  type        = string
}
```

### Step 6: Update outputs.tf

Remove outputs from pruned modules.

### Step 7: Clean Up

```bash
cd ~/datadog_terraform/<client-name>/
terraform fmt -recursive
```

## Example Scenarios

### AWS-Only Client

**Selected**: AWS, RDS, ECS, Lambda
**Removed**: modules/gcp/, modules/azure/, modules/kube/

### GCP with Kubernetes Client

**Selected**: GCP, GKE, Cloud SQL
**Removed**: modules/aws/, modules/azure/, modules/apm/, modules/rum/

### Multi-Cloud Client

**Selected**: AWS, Azure, Kubernetes
**Kept**: modules/aws/, modules/azure/, modules/kube/
**Removed**: modules/gcp/, modules/apm/, modules/rum/, modules/synthetics/

## Dry Run Mode

To preview what would be pruned without making changes:

```bash
# Parse questionnaire and list modules to prune
python ~/agents/plugins/org-generator/lib/questionnaire-parser.py \
  ~/datadog_terraform/<client-name>/questionnaire.md \
  --dry-run
```

## Result

A minimal, clean codebase containing only:
- Core modules (api_keys, app_keys, roles, teams, users)
- Selected cloud provider modules
- Selected infrastructure modules
- Monitors relevant to the client's actual stack

## Example

```
/org-generator:prune acme-corp
```

This will:
1. Parse `questionnaire.md` for selections
2. Remove unused module directories
3. Update modules.tf, variables.tf, outputs.tf
4. Run `terraform fmt` to clean up
