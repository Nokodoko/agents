# Datadog Agent Configuration for {{CLIENT_NAME}}

Generated: {{DATE}}

## Overview

This directory contains Datadog Agent configuration files tailored for {{CLIENT_NAME}}.

## Contents

```
datadog-agent/
├── datadog.yaml          # Main agent configuration
├── conf.d/               # Integration configurations
│   ├── custom_logs.yaml  # Log collection
│   ├── process.yaml      # Process monitoring
│   └── *.yaml            # Service-specific integrations
└── docs/                 # Deployment documentation
    └── *.md              # Platform-specific guides
```

## Quick Start

1. **Get your API key** from Datadog Organization Settings

2. **Choose your deployment method**:
   - [Linux Host](./linux-host.md)
   - [Docker](./docker.md) (if available)
   - [Kubernetes](./kubernetes.md) (if available)

3. **Apply configurations**:
   - Copy `datadog.yaml` to `/etc/datadog-agent/datadog.yaml`
   - Copy relevant `conf.d/*.yaml` files to `/etc/datadog-agent/conf.d/`

4. **Restart the agent**:
   ```bash
   sudo systemctl restart datadog-agent
   ```

5. **Verify**:
   ```bash
   sudo datadog-agent status
   ```

## Configuration Notes

- **Site**: `{{SITE}}`
- Replace `YOUR_API_KEY_HERE` in `datadog.yaml` with your actual API key
- Or set the `DD_API_KEY` environment variable

## Integration Configs

Each integration requires its own configuration in `/etc/datadog-agent/conf.d/<integration>.d/conf.yaml`.

See the individual YAML files in `conf.d/` for setup instructions.

## Support

- [Datadog Documentation](https://docs.datadoghq.com/)
- [Agent Troubleshooting](https://docs.datadoghq.com/agent/troubleshooting/)
