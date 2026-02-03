# Docker Deployment Guide

## Prerequisites

- Docker installed
- Access to Docker socket (for container discovery)

## Quick Start

```bash
docker run -d --name datadog-agent \
  -e DD_API_KEY="YOUR_API_KEY" \
  -e DD_SITE="{{SITE}}" \
  -e DD_LOGS_ENABLED=true \
  -e DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true \
  -e DD_PROCESS_AGENT_ENABLED=true \
  {{#if APM_ENABLED}}-e DD_APM_ENABLED=true \{{/if}}
  -e DD_TAGS="client:{{CLIENT_NAME}} env:production" \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /proc/:/host/proc/:ro \
  -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
  -v /var/lib/docker/containers:/var/lib/docker/containers:ro \
  {{#if APM_ENABLED}}-p 8126:8126 \{{/if}}
  gcr.io/datadoghq/agent:7
```

## Docker Compose

```yaml
version: '3.8'

services:
  datadog-agent:
    image: gcr.io/datadoghq/agent:7
    container_name: datadog-agent
    environment:
      - DD_API_KEY=${DD_API_KEY}
      - DD_SITE={{SITE}}
      - DD_LOGS_ENABLED=true
      - DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true
      - DD_PROCESS_AGENT_ENABLED=true
      {{#if APM_ENABLED}}- DD_APM_ENABLED=true{{/if}}
      - DD_TAGS=client:{{CLIENT_NAME}} env:production
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /proc/:/host/proc/:ro
      - /sys/fs/cgroup/:/host/sys/fs/cgroup:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - ./conf.d:/etc/datadog-agent/conf.d:ro
    {{#if APM_ENABLED}}
    ports:
      - "8126:8126"
    {{/if}}
    restart: unless-stopped
```

Run with:
```bash
DD_API_KEY="your-api-key" docker-compose up -d
```

## Custom Configuration

Mount your configuration files:

```bash
docker run -d --name datadog-agent \
  -e DD_API_KEY="YOUR_API_KEY" \
  -e DD_SITE="{{SITE}}" \
  -v $(pwd)/datadog.yaml:/etc/datadog-agent/datadog.yaml:ro \
  -v $(pwd)/conf.d:/etc/datadog-agent/conf.d:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /proc/:/host/proc/:ro \
  -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
  gcr.io/datadoghq/agent:7
```

## Container Autodiscovery

Label containers for automatic integration:

```yaml
services:
  nginx:
    image: nginx
    labels:
      com.datadoghq.ad.check_names: '["nginx"]'
      com.datadoghq.ad.init_configs: '[{}]'
      com.datadoghq.ad.instances: '[{"nginx_status_url": "http://%%host%%/nginx_status"}]'
      com.datadoghq.ad.logs: '[{"source": "nginx", "service": "nginx"}]'
```

## Verify Installation

```bash
docker exec datadog-agent agent status
docker exec datadog-agent agent configcheck
docker logs datadog-agent
```

## Troubleshooting

### Container not collecting logs

1. Verify `DD_LOGS_ENABLED=true`
2. Check volume mount for `/var/lib/docker/containers`
3. Verify `DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true`

### APM traces not appearing

1. Verify `DD_APM_ENABLED=true`
2. Ensure port 8126 is exposed
3. Application must send traces to the agent host
