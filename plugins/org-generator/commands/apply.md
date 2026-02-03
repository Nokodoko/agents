---
name: apply
description: Process a filled questionnaire and orchestrate full infrastructure setup
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - AskUserQuestion
  - Skill
argument-hint: "<client-name>"
---

# org-generator:apply

Processes a completed questionnaire and orchestrates the full infrastructure setup.

## Usage

```
/org-generator:apply <client-name>
```

## Arguments

- `client-name`: The client identifier (kebab-case, e.g., `acme-corp`)

## Prerequisites

Before running this command:
1. Questionnaire must exist at `~/datadog_terraform/<client-name>/questionnaire.md`
2. Questionnaire must be filled out by the user

## Workflow

This command orchestrates the following steps in sequence:

### Step 1: Parse Questionnaire

1. Read the questionnaire from `~/datadog_terraform/<client-name>/questionnaire.md`
2. Parse the responses using `lib/questionnaire-parser.py`
3. Generate a configuration object with:
   - Organization setup preferences
   - Selected cloud providers (AWS, GCP, Azure)
   - Infrastructure components
   - Monitoring requirements
   - Team structure
   - Tagging strategy

### Step 2: Create S3 Backend (via /org-generator:backend)

1. Add entry to `~/Portfolio/aws/variables.tf` for `<client-name>-backend`
2. Run `terraform init` in `~/Portfolio/aws/`
3. Run `terraform plan` to verify changes
4. Run `terraform apply` to create the bucket
5. Verify bucket creation with `aws s3 ls`

### Step 3: Scaffold Terraform Structure (via /org-generator:scaffold)

1. Generate FULL terraform directory structure at `~/datadog_terraform/<client-name>/`
2. Create all module directories (both required and optional)
3. Generate root terraform files (backend.tf, providers.tf, variables.tf, etc.)

### Step 4: Prune Unused Modules (via /org-generator:prune)

Based on questionnaire responses, remove:
- Unused cloud provider modules (aws/, gcp/, azure/)
- Unused infrastructure modules (kube/, synthetics/, private_locations/)
- Corresponding variables and outputs
- Monitor definitions for unselected infrastructure

### Step 5: Validate Environment (via /org-generator:validate)

1. Check for required environment variables:
   - `TF_VAR_<client_name>_api_key`
   - `TF_VAR_<client_name>_app_key`
2. Re-source shell profile if needed
3. Run `terraform init` in client directory
4. Run `terraform validate`

### Step 6: Generate Monitors (via /org-generator:monitors)

Based on questionnaire responses, generate monitors for:
- Selected cloud providers
- Selected infrastructure components
- Selected services

### Step 7: Generate Agent Configurations (via /org-generator:agent)

Based on questionnaire responses, generate Datadog agent configuration files:

1. Create `datadog-agent/` directory inside client terraform manifest
2. Generate `datadog.yaml` with:
   - Correct site based on data residency
   - APM configuration (if enabled)
   - Process collection (if hosts enabled)
   - Network monitoring (if containers enabled)
   - Client-specific tags

3. Generate integration configs in `conf.d/`:
   - `custom_logs.yaml` - Log collection paths
   - `process.yaml` - Process monitoring
   - Service-specific integrations (nginx, mysql, postgres, redis, kafka, rabbitmq)
   - `http_check.yaml` - HTTP endpoint checks
   - `tcp_check.yaml` - TCP port checks

4. Generate deployment documentation in `docs/`:
   - `README.md` - Overview and quick start
   - `linux-host.md` - Linux installation (always)
   - `windows-host.md` - Windows installation (if selected)
   - `kubernetes.md` - K8s DaemonSet (if containers)
   - `docker.md` - Docker deployment (if Docker)
   - `ecs.md` - ECS task definition (if ECS)
   - `fargate.md` - Fargate sidecar (if Fargate)

## Dependency Chain

```
S3 Backend Created
    └── terraform init succeeds
    └── bucket exists: {client}-backend

Environment Variables Set
    └── TF_VAR_{client}_api_key present
    └── TF_VAR_{client}_app_key present

Terraform Init
    └── backend configured
    └── providers initialized

Terraform Validate
    └── all variables present
    └── syntax valid

Ready for Plan/Apply
```

## Error Handling

If any step fails:
1. Display clear error message with step that failed
2. Provide remediation instructions
3. Allow user to re-run from failed step

## Example

```
/org-generator:apply acme-corp
```

This will:
1. Parse `~/datadog_terraform/acme-corp/questionnaire.md`
2. Create S3 backend `acme-corp-backend`
3. Scaffold terraform structure
4. Prune unused modules based on selections
5. Validate environment and terraform config
6. Generate appropriate monitors
7. Generate agent configurations in `datadog-agent/`
