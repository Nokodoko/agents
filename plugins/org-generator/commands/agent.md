---
name: agent
description: Generate Datadog agent configuration files based on questionnaire responses
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
argument-hint: "<client-name>"
---

# org-generator:agent

Generates Datadog agent configuration files based on questionnaire responses. Creates a complete `datadog-agent/` directory inside the client's terraform manifest.

## Usage

```
/org-generator:agent <client-name>
```

## Arguments

- `client-name`: The client identifier (kebab-case, e.g., `acme-corp`)

## Prerequisites

1. Questionnaire must exist and be filled out
2. Terraform structure should exist (typically run after /org-generator:scaffold)

## Generated Structure

```
~/datadog_terraform/<client-name>/datadog-agent/
├── datadog.yaml              # Main agent configuration
├── conf.d/
│   ├── custom_logs.yaml      # Log collection (always)
│   ├── http_check.yaml       # HTTP endpoint checks (if web servers)
│   ├── tcp_check.yaml        # TCP port checks (if databases/queues)
│   ├── process.yaml          # Process monitoring (if hosts)
│   └── <service>.yaml        # Service-specific integrations
└── docs/
    ├── README.md             # Overview and getting started
    ├── linux-host.md         # Linux installation (always)
    ├── windows-host.md       # Windows installation (if windows)
    ├── docker.md             # Docker deployment (if containers)
    ├── kubernetes.md         # K8s DaemonSet (if kubernetes)
    ├── ecs.md                # ECS task definition (if ecs)
    └── fargate.md            # Fargate sidecar (if fargate)
```

## Main Configuration (datadog.yaml)

Generated with:
- API key placeholder (use environment variable)
- Correct site based on data residency selection
- Environment tag from questionnaire
- Process collection (if hosts enabled)
- APM configuration (if APM enabled)
- Network monitoring (if enabled)
- Custom tags from questionnaire

## Integration Configurations

### Always Generated
| File | Purpose |
|------|---------|
| `custom_logs.yaml` | Log collection paths |
| `process.yaml` | Process monitoring |

### Conditional Based on Services
| Selection | Generated File |
|-----------|---------------|
| nginx | `nginx.yaml` |
| MySQL (self-managed) | `mysql.yaml` |
| PostgreSQL | `postgres.yaml` |
| Redis | `redis.yaml` |
| RabbitMQ | `rabbitmq.yaml` |
| Kafka | `kafka.yaml` |
| Web servers | `http_check.yaml` |
| Databases/queues | `tcp_check.yaml` |

## Deployment Documentation

Based on infrastructure selections:

| Selection | Documentation |
|-----------|--------------|
| Linux hosts | `linux-host.md` (always) |
| Windows hosts | `windows-host.md` |
| Kubernetes/EKS/GKE/AKS | `kubernetes.md` |
| Docker | `docker.md` |
| ECS | `ecs.md` |
| Fargate | `fargate.md` |

Each doc includes:
- Prerequisites
- Installation commands
- Configuration file locations
- Verification steps
- Troubleshooting tips

## Data Residency Support

The `site` parameter in datadog.yaml is set based on Section 9.2 of the questionnaire:

| Selection | Site Value |
|-----------|-----------|
| US (default) | `datadoghq.com` |
| EU | `datadoghq.eu` |
| US Government (GovCloud) | `ddog-gov.com` |
| US3 | `us3.datadoghq.com` |
| US5 | `us5.datadoghq.com` |

## Workflow

1. Parse questionnaire for:
   - Infrastructure selections (hosts, containers)
   - Services (web servers, databases, queues)
   - Monitoring features (APM, process collection)
   - Data residency

2. Generate `datadog.yaml` with appropriate settings

3. Generate integration configs in `conf.d/` for each selected service

4. Generate deployment docs in `docs/` for each platform

5. Output summary of generated files

## Example

```
/org-generator:agent acme-corp
```

If questionnaire indicates:
- Linux hosts
- Kubernetes
- nginx, MySQL, Redis
- APM enabled
- US data residency

This will generate:
- `datadog.yaml` with APM enabled, site=datadoghq.com
- `conf.d/custom_logs.yaml`
- `conf.d/process.yaml`
- `conf.d/nginx.yaml`
- `conf.d/mysql.yaml`
- `conf.d/redis.yaml`
- `conf.d/http_check.yaml`
- `conf.d/tcp_check.yaml`
- `docs/README.md`
- `docs/linux-host.md`
- `docs/kubernetes.md`

## Integration with Apply Command

This command is automatically invoked as Step 7 of `/org-generator:apply`:

```
1. Parse Questionnaire
2. Create S3 Backend
3. Scaffold Terraform Structure
4. Prune Unused Modules
5. Validate Environment
6. Generate Monitors
7. Generate Agent Configurations  <-- This command
```

## Manual Usage

Can also be run independently after initial setup:

```bash
# Regenerate agent configs after questionnaire update
/org-generator:agent acme-corp
```
