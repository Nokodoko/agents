# AWS Fargate Sidecar Deployment Guide

## Overview

For Fargate, the Datadog Agent runs as a sidecar container in each task.

## Task Definition

Add the Datadog Agent container as a sidecar:

```json
{
  "family": "my-app-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "my-app",
      "image": "my-app:latest",
      "essential": true,
      "portMappings": [
        {"containerPort": 8080, "protocol": "tcp"}
      ],
      "environment": [
        {"name": "DD_AGENT_HOST", "value": "localhost"},
        {"name": "DD_TRACE_AGENT_PORT", "value": "8126"}
      ],
      "logConfiguration": {
        "logDriver": "awsfirelens",
        "options": {
          "Name": "datadog",
          "apikey": "YOUR_API_KEY",
          "Host": "http-intake.logs.{{SITE}}",
          "dd_service": "my-app",
          "dd_source": "my-app",
          "dd_tags": "client:{{CLIENT_NAME}},env:production",
          "TLS": "on",
          "provider": "ecs"
        }
      },
      "dependsOn": [
        {"containerName": "datadog-agent", "condition": "START"}
      ]
    },
    {
      "name": "datadog-agent",
      "image": "gcr.io/datadoghq/agent:7",
      "essential": true,
      "environment": [
        {"name": "DD_API_KEY", "value": "YOUR_API_KEY"},
        {"name": "DD_SITE", "value": "{{SITE}}"},
        {"name": "ECS_FARGATE", "value": "true"},
        {"name": "DD_APM_ENABLED", "value": "{{APM_ENABLED}}"},
        {"name": "DD_LOGS_ENABLED", "value": "true"},
        {"name": "DD_TAGS", "value": "client:{{CLIENT_NAME}} env:production"}
      ],
      "portMappings": [
        {"containerPort": 8126, "protocol": "tcp"}
      ]
    },
    {
      "name": "log_router",
      "image": "amazon/aws-for-fluent-bit:stable",
      "essential": true,
      "firelensConfiguration": {
        "type": "fluentbit"
      }
    }
  ]
}
```

## Using AWS Secrets Manager

```json
{
  "secrets": [
    {
      "name": "DD_API_KEY",
      "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789:secret:datadog-api-key"
    }
  ]
}
```

## IAM Task Role

Add these permissions to the task role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecs:ListClusters",
        "ecs:ListContainerInstances",
        "ecs:DescribeContainerInstances"
      ],
      "Resource": "*"
    }
  ]
}
```

## Verify Installation

```bash
aws logs tail /ecs/my-app-task --filter-pattern "datadog-agent"
```

## Troubleshooting

### Agent sidecar not receiving traces

1. Ensure app connects to `localhost:8126`
2. Verify `DD_APM_ENABLED=true` in agent container
3. Check security groups allow internal communication

### Logs not appearing

1. Verify FireLens configuration
2. Check log router container is healthy
3. Verify API key is correct
