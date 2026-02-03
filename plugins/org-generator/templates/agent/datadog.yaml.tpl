# Datadog Agent Configuration Template for {{CLIENT_NAME}}
# Generated: {{DATE}}
#
# This template is processed by lib/agent-generator.py
# Variables:
#   {{CLIENT_NAME}} - Client name (kebab-case)
#   {{SITE}} - Datadog site (datadoghq.com, datadoghq.eu, etc.)
#   {{ENV}} - Environment tag
#
# IMPORTANT: Replace YOUR_API_KEY_HERE with your actual API key
# or set the DD_API_KEY environment variable.

api_key: "YOUR_API_KEY_HERE"  # Or use DD_API_KEY env var
site: {{SITE}}

# Remote configuration
remote_updates: true
inventories_configuration_enabled: true

# Logging
logs_enabled: true
logs_config:
  container_collect_all: true
  auto_multi_line_detection: true

# Process collection (if hosts enabled)
{{#if HOSTS_ENABLED}}
process_config:
  process_collection:
    enabled: true
  container_collection:
    enabled: true
{{/if}}

# APM Configuration (if APM enabled)
{{#if APM_ENABLED}}
apm_config:
  enabled: true
  max_traces_per_second: 100
{{/if}}

# Network monitoring (if containers enabled)
{{#if CONTAINERS_ENABLED}}
network_config:
  enabled: true
{{/if}}

# Tags
tags:
  - client:{{CLIENT_NAME}}
  - env:{{ENV}}
{{#each CUSTOM_TAGS}}
  - {{this}}
{{/each}}
  - managed_by:datadog-agent
