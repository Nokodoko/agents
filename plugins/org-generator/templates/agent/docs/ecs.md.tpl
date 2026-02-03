# Amazon ECS Deployment Guide

## Prerequisites

- ECS cluster (EC2 or Fargate)
- IAM permissions for task registration
- Datadog API key stored in AWS Secrets Manager (recommended)

## EC2 Launch Type

### Task Definition

```json
{
  "family": "datadog-agent-task",
  "containerDefinitions": [
    {
      "name": "datadog-agent",
      "image": "gcr.io/datadoghq/agent:7",
      "cpu": 100,
      "memory": 512,
      "essential": true,
      "environment": [
        {"name": "DD_API_KEY", "value": "YOUR_API_KEY"},
        {"name": "DD_SITE", "value": "{{SITE}}"},
        {"name": "DD_LOGS_ENABLED", "value": "true"},
        {"name": "DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL", "value": "true"},
        {"name": "DD_PROCESS_AGENT_ENABLED", "value": "true"},
        {"name": "DD_TAGS", "value": "client:{{CLIENT_NAME}} env:production"},
        {"name": "ECS_FARGATE", "value": "false"}
      ],
      "mountPoints": [
        {
          "sourceVolume": "docker-sock",
          "containerPath": "/var/run/docker.sock",
          "readOnly": true
        },
        {
          "sourceVolume": "proc",
          "containerPath": "/host/proc",
          "readOnly": true
        },
        {
          "sourceVolume": "cgroup",
          "containerPath": "/host/sys/fs/cgroup",
          "readOnly": true
        }
      ]
    }
  ],
  "volumes": [
    {"name": "docker-sock", "host": {"sourcePath": "/var/run/docker.sock"}},
    {"name": "proc", "host": {"sourcePath": "/proc"}},
    {"name": "cgroup", "host": {"sourcePath": "/sys/fs/cgroup"}}
  ],
  "requiresCompatibilities": ["EC2"]
}
```

### Create Daemon Service

```bash
aws ecs create-service \
  --cluster your-cluster \
  --service-name datadog-agent \
  --task-definition datadog-agent-task \
  --scheduling-strategy DAEMON
```

## Using AWS Secrets Manager

```json
{
  "environment": [
    {"name": "DD_SITE", "value": "{{SITE}}"}
  ],
  "secrets": [
    {
      "name": "DD_API_KEY",
      "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789:secret:datadog-api-key"
    }
  ]
}
```

## Verify Installation

```bash
aws ecs describe-services \
  --cluster your-cluster \
  --services datadog-agent

aws logs tail /ecs/datadog-agent --follow
```

## Troubleshooting

### Task keeps stopping

1. Check CloudWatch Logs for the task
2. Verify API key is correct
3. Ensure sufficient memory allocation

### No container metrics

1. Verify Docker socket mount
2. Check task IAM role permissions
3. Ensure `DD_PROCESS_AGENT_ENABLED=true`
