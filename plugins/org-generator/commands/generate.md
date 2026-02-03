---
name: generate
description: Generate a complete Datadog Terraform infrastructure for a new client
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - AskUserQuestion
argument-hint: "<client-name>"
---

# org-generator:generate

Generates complete Datadog Terraform infrastructure for a new client engagement.

## Usage

```
/org-generator:generate <client-name>
```

## Arguments

- `client-name`: The client identifier (kebab-case, e.g., `acme-corp`)

## Workflow

### Phase 1: Questionnaire Generation

1. Generate a professional markdown questionnaire at `~/datadog_terraform/<client-name>/questionnaire.md`
2. The questionnaire covers:
   - Organization setup (child org vs existing)
   - Cloud providers (AWS, GCP, Azure)
   - Infrastructure components (hosts, containers, serverless)
   - Services to monitor
   - Tagging strategy
   - Team structure and roles

3. **STOP and inform user**: "Questionnaire generated at `~/datadog_terraform/<client-name>/questionnaire.md`. Please fill it out and run `/org-generator:apply <client-name>` when ready."

### Phase 2: S3 Backend Creation (via /org-generator:backend)

After questionnaire is complete, create the S3 backend:

1. Add entry to `~/Portfolio/aws/variables.tf` for `<client-name>-backend`
2. Run `terraform init`, `plan`, and `apply` in `~/Portfolio/aws/`
3. Verify bucket creation

### Phase 3: Terraform Scaffold (via /org-generator:scaffold)

Generate the client's Datadog Terraform structure:

```
~/datadog_terraform/<client-name>/
├── backend.tf
├── providers.tf
├── variables.tf
├── outputs.tf
├── modules.tf
├── README.md
├── modules/
│   ├── api_keys/
│   ├── app_keys/
│   ├── roles/
│   ├── teams/
│   ├── users/
│   └── [cloud-specific modules based on questionnaire]
├── installs/
│   ├── agent.md
│   ├── install.sh
│   └── [platform-specific install scripts]
└── k8s/ (if applicable)
```

### Phase 4: Monitor Generation (via /org-generator:monitors)

Based on questionnaire answers, generate appropriate monitors:

- **AWS**: EC2, RDS, ALB, ECS, Lambda monitors
- **GCP**: Compute Engine, Cloud SQL, GKE monitors
- **Azure**: VMs, SQL Database, AKS monitors
- **Kubernetes**: Cluster health, pod status, node pressure
- **Generic**: CPU, memory, disk, network, latency

## Output

- Questionnaire markdown file
- Complete Terraform directory structure
- Initialized and applied S3 backend
- Generated monitors based on infrastructure

## Example

```
/org-generator:generate acme-corp
```

This will:
1. Create `~/datadog_terraform/acme-corp/questionnaire.md`
2. Wait for user to complete questionnaire
3. Continue with `/org-generator:apply acme-corp`
