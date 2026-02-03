#!/usr/bin/env python3
"""
Agent Generator for org-generator plugin

Generates Datadog agent configuration files based on parsed questionnaire responses.
Creates datadog.yaml, integration configs, and deployment documentation.

Usage:
    python agent-generator.py <config-json> --output-dir <agent-dir>

Example:
    python questionnaire-parser.py ~/datadog_terraform/acme-corp/questionnaire.md | \
        python agent-generator.py - --output-dir ~/datadog_terraform/acme-corp/datadog-agent/
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


# Site mappings for data residency
SITE_MAPPINGS = {
    'us': 'datadoghq.com',
    'eu': 'datadoghq.eu',
    'us3': 'us3.datadoghq.com',
    'us5': 'us5.datadoghq.com',
    'gov': 'ddog-gov.com',
    'us_government': 'ddog-gov.com',
    'govcloud': 'ddog-gov.com'
}


def get_site(config: dict) -> str:
    """Determine the Datadog site based on data residency selection."""
    residency = config.get('data_residency', 'us').lower()
    return SITE_MAPPINGS.get(residency, 'datadoghq.com')


def generate_datadog_yaml(config: dict) -> str:
    """Generate main datadog.yaml configuration."""
    client_name = config.get('client_name', 'client')
    site = get_site(config)

    # Determine enabled features
    hosts_enabled = config.get('infrastructure', {}).get('hosts', {}).get('enabled', False)
    apm_enabled = config.get('monitoring', {}).get('apm', False)

    # Build tags
    tags = [f'client:{client_name}']
    env_tags = config.get('tagging', {}).get('environments', [])
    if env_tags:
        tags.append(f'env:{env_tags[0]}')

    custom_tags = config.get('tagging', {}).get('tags', {})
    for key, value in custom_tags.items():
        if key not in ['env', 'client']:
            tags.append(f'{key}:{value}')

    tags_yaml = '\n'.join([f'  - {tag}' for tag in tags])

    content = f'''# Datadog Agent Configuration for {client_name}
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Site: {site}
#
# IMPORTANT: Replace YOUR_API_KEY_HERE with your actual API key
# or set the DD_API_KEY environment variable.

api_key: "YOUR_API_KEY_HERE"  # Or use DD_API_KEY env var
site: {site}

# Remote configuration
remote_updates: true
inventories_configuration_enabled: true

# Logging
logs_enabled: true
logs_config:
  container_collect_all: true
  auto_multi_line_detection: true
'''

    if hosts_enabled:
        content += '''
# Process collection
process_config:
  process_collection:
    enabled: true
  container_collection:
    enabled: true
'''

    if apm_enabled:
        content += '''
# APM Configuration
apm_config:
  enabled: true
  max_traces_per_second: 100
  analyzed_spans:
    # Add service-specific analyzed spans here
    # my-service|servlet.request: 1
'''

    # Check if containers enabled for network monitoring
    containers_enabled = config.get('infrastructure', {}).get('containers', {}).get('enabled', False)
    if containers_enabled:
        content += '''
# Network monitoring (useful for containers/k8s)
network_config:
  enabled: true
'''

    content += f'''
# Tags applied to all metrics/logs
tags:
{tags_yaml}
  - managed_by:datadog-agent

# Hostname configuration
# hostname: <custom-hostname>  # Uncomment to override

# Proxy configuration (if needed)
# proxy:
#   https: http://proxy.example.com:3128
#   no_proxy:
#     - 169.254.169.254  # AWS metadata

# Additional configuration
# See: https://docs.datadoghq.com/agent/configuration/agent-configuration-files/
'''

    return content


def generate_custom_logs_yaml(config: dict) -> str:
    """Generate custom_logs.yaml for log collection."""
    client_name = config.get('client_name', 'client')

    services = config.get('services', {})
    web_servers = services.get('web_servers', [])
    app_servers = services.get('app_servers', [])

    content = f'''# Custom Log Collection for {client_name}
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# Place this file in /etc/datadog-agent/conf.d/custom_logs.d/conf.yaml

logs:
'''

    # Add web server logs
    if 'nginx' in web_servers:
        content += '''
  # nginx logs
  - type: file
    path: /var/log/nginx/access.log
    service: nginx
    source: nginx
    sourcecategory: http_web_access

  - type: file
    path: /var/log/nginx/error.log
    service: nginx
    source: nginx
    sourcecategory: http_web_error
'''

    if 'apache' in web_servers or 'Apache HTTP Server' in web_servers:
        content += '''
  # Apache logs
  - type: file
    path: /var/log/apache2/access.log
    service: apache
    source: apache
    sourcecategory: http_web_access

  - type: file
    path: /var/log/apache2/error.log
    service: apache
    source: apache
    sourcecategory: http_web_error
'''

    # Add application logs
    if 'java' in [s.lower() for s in app_servers] or 'Java' in app_servers:
        content += '''
  # Java application logs
  - type: file
    path: /var/log/app/*.log
    service: java-app
    source: java
    # log_processing_rules:
    #   - type: multi_line
    #     name: java_stack_trace
    #     pattern: "\\d{4}-\\d{2}-\\d{2}"
'''

    if 'node.js' in [s.lower() for s in app_servers] or 'Node.js' in app_servers:
        content += '''
  # Node.js application logs
  - type: file
    path: /var/log/node/*.log
    service: node-app
    source: nodejs
'''

    if 'python' in [s.lower() for s in app_servers] or 'Python' in app_servers:
        content += '''
  # Python application logs
  - type: file
    path: /var/log/python/*.log
    service: python-app
    source: python
'''

    # Add syslog
    content += '''
  # System logs
  - type: file
    path: /var/log/syslog
    service: system
    source: syslog

  - type: file
    path: /var/log/messages
    service: system
    source: syslog

  # Authentication logs
  - type: file
    path: /var/log/auth.log
    service: system
    source: auth
'''

    return content


def generate_process_yaml(config: dict) -> str:
    """Generate process.yaml for process monitoring."""
    client_name = config.get('client_name', 'client')
    services = config.get('services', {})

    content = f'''# Process Monitoring for {client_name}
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# Place this file in /etc/datadog-agent/conf.d/process.d/conf.yaml

init_config:

instances:
'''

    # Add processes based on services
    web_servers = services.get('web_servers', [])
    app_servers = services.get('app_servers', [])
    message_queues = services.get('message_queues', [])
    caching = services.get('caching', [])

    if 'nginx' in web_servers:
        content += '''
  - name: nginx
    search_string:
      - nginx
    exact_match: false
'''

    if 'apache' in web_servers or 'Apache HTTP Server' in web_servers:
        content += '''
  - name: apache
    search_string:
      - apache2
      - httpd
    exact_match: false
'''

    if 'java' in [s.lower() for s in app_servers] or 'Java' in app_servers:
        content += '''
  - name: java
    search_string:
      - java
    exact_match: false
'''

    if 'node.js' in [s.lower() for s in app_servers] or 'Node.js' in app_servers:
        content += '''
  - name: nodejs
    search_string:
      - node
    exact_match: false
'''

    if 'python' in [s.lower() for s in app_servers] or 'Python' in app_servers:
        content += '''
  - name: python
    search_string:
      - python
      - gunicorn
      - uwsgi
    exact_match: false
'''

    if 'Redis' in caching or 'redis' in [c.lower() for c in caching]:
        content += '''
  - name: redis
    search_string:
      - redis-server
    exact_match: false
'''

    if 'RabbitMQ' in message_queues:
        content += '''
  - name: rabbitmq
    search_string:
      - rabbitmq
      - beam.smp
    exact_match: false
'''

    if 'Apache Kafka' in message_queues or 'Kafka' in message_queues:
        content += '''
  - name: kafka
    search_string:
      - kafka
    exact_match: false
'''

    # Always add datadog-agent itself
    content += '''
  - name: datadog-agent
    search_string:
      - datadog-agent
    exact_match: false
'''

    return content


def generate_http_check_yaml(config: dict) -> str:
    """Generate http_check.yaml for HTTP endpoint monitoring."""
    client_name = config.get('client_name', 'client')

    content = f'''# HTTP Check Configuration for {client_name}
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# Place this file in /etc/datadog-agent/conf.d/http_check.d/conf.yaml
#
# Update the URLs below to match your actual endpoints

init_config:

instances:
  # Example health check endpoint
  - name: app-health
    url: http://localhost:8080/health
    timeout: 10
    http_response_status_code: 200
    tags:
      - service:app
      - client:{client_name}

  # Example API endpoint
  # - name: api-health
  #   url: https://api.example.com/health
  #   timeout: 10
  #   http_response_status_code: 200
  #   tls_verify: true
  #   tags:
  #     - service:api
  #     - client:{client_name}
'''

    return content


def generate_tcp_check_yaml(config: dict) -> str:
    """Generate tcp_check.yaml for TCP port monitoring."""
    client_name = config.get('client_name', 'client')
    services = config.get('services', {})
    infra = config.get('infrastructure', {})

    content = f'''# TCP Check Configuration for {client_name}
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# Place this file in /etc/datadog-agent/conf.d/tcp_check.d/conf.yaml

init_config:

instances:
'''

    # Add checks based on services
    databases = infra.get('databases', {})
    self_managed_dbs = databases.get('self_managed', [])
    message_queues = services.get('message_queues', [])
    caching = services.get('caching', [])

    if 'mysql' in [d.lower() for d in self_managed_dbs] or 'MySQL' in self_managed_dbs:
        content += '''
  # MySQL
  - name: mysql
    host: localhost
    port: 3306
    timeout: 5
    tags:
      - service:mysql
'''

    if 'postgresql' in [d.lower() for d in self_managed_dbs] or 'PostgreSQL' in self_managed_dbs:
        content += '''
  # PostgreSQL
  - name: postgres
    host: localhost
    port: 5432
    timeout: 5
    tags:
      - service:postgres
'''

    if 'mongodb' in [d.lower() for d in self_managed_dbs] or 'MongoDB' in self_managed_dbs:
        content += '''
  # MongoDB
  - name: mongodb
    host: localhost
    port: 27017
    timeout: 5
    tags:
      - service:mongodb
'''

    if 'redis' in [d.lower() for d in self_managed_dbs] or 'Redis' in self_managed_dbs or 'Redis' in caching:
        content += '''
  # Redis
  - name: redis
    host: localhost
    port: 6379
    timeout: 5
    tags:
      - service:redis
'''

    if 'RabbitMQ' in message_queues:
        content += '''
  # RabbitMQ
  - name: rabbitmq
    host: localhost
    port: 5672
    timeout: 5
    tags:
      - service:rabbitmq

  - name: rabbitmq-management
    host: localhost
    port: 15672
    timeout: 5
    tags:
      - service:rabbitmq
'''

    if 'Apache Kafka' in message_queues or 'Kafka' in message_queues:
        content += '''
  # Kafka
  - name: kafka
    host: localhost
    port: 9092
    timeout: 5
    tags:
      - service:kafka
'''

    if 'Elasticsearch' in self_managed_dbs:
        content += '''
  # Elasticsearch
  - name: elasticsearch
    host: localhost
    port: 9200
    timeout: 5
    tags:
      - service:elasticsearch
'''

    return content


def generate_nginx_yaml(config: dict) -> str:
    """Generate nginx.yaml integration config."""
    client_name = config.get('client_name', 'client')

    return f'''# nginx Integration for {client_name}
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# Place this file in /etc/datadog-agent/conf.d/nginx.d/conf.yaml
#
# Prerequisites:
# 1. Enable nginx stub_status module
# 2. Add to nginx.conf:
#    location /nginx_status {{
#        stub_status on;
#        allow 127.0.0.1;
#        deny all;
#    }}

init_config:

instances:
  - nginx_status_url: http://localhost/nginx_status
    tags:
      - client:{client_name}

logs:
  - type: file
    path: /var/log/nginx/access.log
    service: nginx
    source: nginx

  - type: file
    path: /var/log/nginx/error.log
    service: nginx
    source: nginx
'''


def generate_mysql_yaml(config: dict) -> str:
    """Generate mysql.yaml integration config."""
    client_name = config.get('client_name', 'client')

    return f'''# MySQL Integration for {client_name}
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# Place this file in /etc/datadog-agent/conf.d/mysql.d/conf.yaml
#
# Prerequisites:
# 1. Create Datadog user in MySQL:
#    CREATE USER 'datadog'@'localhost' IDENTIFIED BY '<PASSWORD>';
#    GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost';
#    GRANT PROCESS ON *.* TO 'datadog'@'localhost';
#    GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';

init_config:

instances:
  - host: localhost
    port: 3306
    username: datadog
    password: "<MYSQL_PASSWORD>"  # Use env var: ENC[datadog_user_password]

    options:
      replication: true
      galera_cluster: false
      extra_status_metrics: true
      extra_innodb_metrics: true
      schema_size_metrics: true
      disable_innodb_metrics: false

    tags:
      - client:{client_name}
      - service:mysql

logs:
  - type: file
    path: /var/log/mysql/error.log
    source: mysql
    service: mysql

  - type: file
    path: /var/log/mysql/mysql-slow.log
    source: mysql
    service: mysql
'''


def generate_postgres_yaml(config: dict) -> str:
    """Generate postgres.yaml integration config."""
    client_name = config.get('client_name', 'client')

    return f'''# PostgreSQL Integration for {client_name}
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# Place this file in /etc/datadog-agent/conf.d/postgres.d/conf.yaml
#
# Prerequisites:
# 1. Create Datadog user in PostgreSQL:
#    CREATE USER datadog WITH PASSWORD '<PASSWORD>';
#    GRANT pg_monitor TO datadog;
#    GRANT SELECT ON pg_stat_database TO datadog;

init_config:

instances:
  - host: localhost
    port: 5432
    username: datadog
    password: "<POSTGRES_PASSWORD>"  # Use env var
    dbname: postgres

    # Query metrics
    query_metrics:
      enabled: true

    # Relations to collect
    relations:
      - relation_regex: .*

    tags:
      - client:{client_name}
      - service:postgres

logs:
  - type: file
    path: /var/log/postgresql/*.log
    source: postgresql
    service: postgres
'''


def generate_redis_yaml(config: dict) -> str:
    """Generate redis.yaml integration config."""
    client_name = config.get('client_name', 'client')

    return f'''# Redis Integration for {client_name}
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# Place this file in /etc/datadog-agent/conf.d/redisdb.d/conf.yaml

init_config:

instances:
  - host: localhost
    port: 6379
    # password: "<REDIS_PASSWORD>"  # Uncomment if auth required

    # Keys to monitor (patterns)
    # keys:
    #   - key_pattern

    # Slow log
    slowlog-max-len: 128

    tags:
      - client:{client_name}
      - service:redis

logs:
  - type: file
    path: /var/log/redis/redis-server.log
    source: redis
    service: redis
'''


def generate_kafka_yaml(config: dict) -> str:
    """Generate kafka.yaml integration config."""
    client_name = config.get('client_name', 'client')

    return f'''# Kafka Integration for {client_name}
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# Place this file in /etc/datadog-agent/conf.d/kafka.d/conf.yaml
#
# Prerequisites:
# 1. Enable JMX for Kafka brokers
# 2. Set KAFKA_JMX_OPTS environment variable

init_config:
  is_jmx: true
  collect_default_metrics: true

instances:
  - host: localhost
    port: 9999  # JMX port

    tags:
      - client:{client_name}
      - service:kafka

logs:
  - type: file
    path: /var/log/kafka/*.log
    source: kafka
    service: kafka
'''


def generate_rabbitmq_yaml(config: dict) -> str:
    """Generate rabbitmq.yaml integration config."""
    client_name = config.get('client_name', 'client')

    return f'''# RabbitMQ Integration for {client_name}
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# Place this file in /etc/datadog-agent/conf.d/rabbitmq.d/conf.yaml
#
# Prerequisites:
# 1. Enable RabbitMQ management plugin:
#    rabbitmq-plugins enable rabbitmq_management
# 2. Create monitoring user or use existing credentials

init_config:

instances:
  - rabbitmq_api_url: http://localhost:15672/api/
    username: guest
    password: guest  # Update with actual credentials

    # Queue filtering
    # queues:
    #   - queue_name_1
    #   - queue_name_2

    # Queue regex filtering
    # queues_regexes:
    #   - "prefix-.*"

    tags:
      - client:{client_name}
      - service:rabbitmq

logs:
  - type: file
    path: /var/log/rabbitmq/*.log
    source: rabbitmq
    service: rabbitmq
'''


def generate_readme(config: dict) -> str:
    """Generate README.md for agent deployment documentation."""
    client_name = config.get('client_name', 'client')
    site = get_site(config)

    return f'''# Datadog Agent Configuration for {client_name}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

This directory contains Datadog Agent configuration files tailored for {client_name}.

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

1. **Get your API key** from [Datadog Organization Settings](https://{site.replace('datadoghq', 'app.datadoghq')}/organization-settings/api-keys)

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

- **Site**: `{site}`
- Replace `YOUR_API_KEY_HERE` in `datadog.yaml` with your actual API key
- Or set the `DD_API_KEY` environment variable

## Integration Configs

Each integration requires its own configuration in `/etc/datadog-agent/conf.d/<integration>.d/conf.yaml`.

See the individual YAML files in `conf.d/` for setup instructions.

## Support

- [Datadog Documentation](https://docs.datadoghq.com/)
- [Agent Troubleshooting](https://docs.datadoghq.com/agent/troubleshooting/)
'''


def generate_linux_host_doc(config: dict) -> str:
    """Generate linux-host.md deployment documentation."""
    client_name = config.get('client_name', 'client')
    site = get_site(config)

    # Determine site parameter for install script
    site_param = '' if site == 'datadoghq.com' else f'DD_SITE="{site}" '

    return f'''# Linux Host Installation Guide

## Prerequisites

- Linux distribution (Ubuntu, Debian, RHEL, CentOS, Amazon Linux, etc.)
- Root/sudo access
- Outbound internet access to `*.{site}`

## Installation

### One-Line Install (Recommended)

```bash
{site_param}DD_API_KEY="YOUR_API_KEY" DD_AGENT_MAJOR_VERSION=7 bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script_agent7.sh)"
```

### Manual Installation

#### Ubuntu/Debian

```bash
# Add Datadog repository
sudo sh -c "echo 'deb [signed-by=/usr/share/keyrings/datadog-archive-keyring.gpg] https://apt.datadoghq.com/ stable 7' > /etc/apt/sources.list.d/datadog.list"
sudo touch /usr/share/keyrings/datadog-archive-keyring.gpg
sudo chmod a+r /usr/share/keyrings/datadog-archive-keyring.gpg

curl https://keys.datadoghq.com/DATADOG_APT_KEY_CURRENT.public | sudo gpg --no-default-keyring --keyring /usr/share/keyrings/datadog-archive-keyring.gpg --import --batch

# Install agent
sudo apt-get update
sudo apt-get install datadog-agent datadog-signing-keys
```

#### RHEL/CentOS

```bash
# Add Datadog repository
cat <<EOF | sudo tee /etc/yum.repos.d/datadog.repo
[datadog]
name = Datadog, Inc.
baseurl = https://yum.datadoghq.com/stable/7/x86_64/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://keys.datadoghq.com/DATADOG_RPM_KEY_CURRENT.public
       https://keys.datadoghq.com/DATADOG_RPM_KEY_B01082D3.public
       https://keys.datadoghq.com/DATADOG_RPM_KEY_FD4BF915.public
       https://keys.datadoghq.com/DATADOG_RPM_KEY_E09422B3.public
EOF

# Install agent
sudo yum makecache
sudo yum install datadog-agent
```

## Configuration

1. Copy the main configuration:
   ```bash
   sudo cp datadog.yaml /etc/datadog-agent/datadog.yaml
   ```

2. Set your API key:
   ```bash
   sudo sed -i 's/YOUR_API_KEY_HERE/<your-actual-api-key>/' /etc/datadog-agent/datadog.yaml
   ```

3. Copy integration configs:
   ```bash
   # Example for custom logs
   sudo mkdir -p /etc/datadog-agent/conf.d/custom_logs.d
   sudo cp conf.d/custom_logs.yaml /etc/datadog-agent/conf.d/custom_logs.d/conf.yaml

   # Repeat for other integrations as needed
   ```

4. Set permissions:
   ```bash
   sudo chown -R dd-agent:dd-agent /etc/datadog-agent
   sudo chmod 640 /etc/datadog-agent/datadog.yaml
   ```

## Start the Agent

```bash
# Enable and start
sudo systemctl enable datadog-agent
sudo systemctl start datadog-agent

# Check status
sudo systemctl status datadog-agent
```

## Verify Installation

```bash
# Check agent status
sudo datadog-agent status

# Check for errors
sudo datadog-agent configcheck

# View logs
sudo journalctl -u datadog-agent -f
```

## Troubleshooting

### Agent won't start

```bash
# Check logs
sudo cat /var/log/datadog/agent.log

# Validate config
sudo datadog-agent configcheck
```

### No data in Datadog

1. Verify API key is correct
2. Check network connectivity: `curl -v https://api.{site}/api/v1/validate`
3. Review agent logs for errors

### Permission issues

```bash
# Fix ownership
sudo chown -R dd-agent:dd-agent /etc/datadog-agent

# Add dd-agent to required groups for log access
sudo usermod -a -G adm dd-agent
```

## Useful Commands

```bash
# Restart agent
sudo systemctl restart datadog-agent

# Stop agent
sudo systemctl stop datadog-agent

# View config
sudo datadog-agent config

# Run integration check
sudo datadog-agent check <integration_name>

# Flare (for support)
sudo datadog-agent flare
```
'''


def generate_windows_host_doc(config: dict) -> str:
    """Generate windows-host.md deployment documentation."""
    client_name = config.get('client_name', 'client')
    site = get_site(config)

    return f'''# Windows Host Installation Guide

## Prerequisites

- Windows Server 2012 R2 or later (Windows 10/11 for workstations)
- Administrator access
- Outbound internet access to `*.{site}`

## Installation

### GUI Installer

1. Download the latest Windows installer:
   - [64-bit](https://s3.amazonaws.com/ddagent-windows-stable/datadog-agent-7-latest.amd64.msi)

2. Run the installer as Administrator

3. Enter your API key when prompted

4. Complete the installation wizard

### Command Line Installation

```powershell
# Download installer
Invoke-WebRequest -Uri "https://s3.amazonaws.com/ddagent-windows-stable/datadog-agent-7-latest.amd64.msi" -OutFile "datadog-agent.msi"

# Install with API key
msiexec /qn /i datadog-agent.msi APIKEY="YOUR_API_KEY" SITE="{site}"
```

## Configuration

Configuration files are located at:
```
C:\\ProgramData\\Datadog\\datadog.yaml
C:\\ProgramData\\Datadog\\conf.d\\
```

1. Copy the main configuration:
   ```powershell
   Copy-Item datadog.yaml -Destination "C:\\ProgramData\\Datadog\\datadog.yaml"
   ```

2. Update the API key in the configuration file

3. Copy integration configs:
   ```powershell
   # Example for custom logs
   New-Item -ItemType Directory -Path "C:\\ProgramData\\Datadog\\conf.d\\custom_logs.d" -Force
   Copy-Item conf.d\\custom_logs.yaml -Destination "C:\\ProgramData\\Datadog\\conf.d\\custom_logs.d\\conf.yaml"
   ```

## Service Management

```powershell
# Restart agent
Restart-Service -Name "DatadogAgent"

# Stop agent
Stop-Service -Name "DatadogAgent"

# Start agent
Start-Service -Name "DatadogAgent"

# Check status
Get-Service -Name "DatadogAgent"
```

## Verify Installation

```powershell
# Check agent status
& "C:\\Program Files\\Datadog\\Datadog Agent\\bin\\agent.exe" status

# Check for config errors
& "C:\\Program Files\\Datadog\\Datadog Agent\\bin\\agent.exe" configcheck
```

## Log Locations

- Agent logs: `C:\\ProgramData\\Datadog\\logs\\agent.log`
- JMX logs: `C:\\ProgramData\\Datadog\\logs\\jmxfetch.log`

## Troubleshooting

### Agent service won't start

1. Check Windows Event Viewer for errors
2. Verify API key is correct
3. Check `C:\\ProgramData\\Datadog\\logs\\agent.log`

### Permissions issues

The Datadog Agent runs as `ddagentuser`. Ensure this account has:
- Read access to log files being collected
- Access to performance counters

```powershell
# Add to Performance Monitor Users group
Add-LocalGroupMember -Group "Performance Monitor Users" -Member "ddagentuser"
```

## Useful Commands

```powershell
# Agent executable path
$agent = "C:\\Program Files\\Datadog\\Datadog Agent\\bin\\agent.exe"

# View current config
& $agent config

# Run integration check
& $agent check <integration_name>

# Generate support flare
& $agent flare
```
'''


def generate_kubernetes_doc(config: dict) -> str:
    """Generate kubernetes.md deployment documentation."""
    client_name = config.get('client_name', 'client')
    site = get_site(config)
    apm_enabled = config.get('monitoring', {}).get('apm', False)

    return f'''# Kubernetes Deployment Guide

## Prerequisites

- Kubernetes cluster (1.22+)
- `kubectl` configured
- Helm 3 installed

## Installation with Helm

### 1. Add Datadog Helm Repository

```bash
helm repo add datadog https://helm.datadoghq.com
helm repo update
```

### 2. Create Secrets

```bash
# Create namespace
kubectl create namespace datadog

# Create API key secret
kubectl create secret generic datadog-secret \\
  --from-literal api-key="YOUR_API_KEY" \\
  --namespace datadog
```

### 3. Create values.yaml

```yaml
# values.yaml for {client_name}
datadog:
  site: {site}
  apiKeyExistingSecret: datadog-secret

  # Logs collection
  logs:
    enabled: true
    containerCollectAll: true

  # APM
  apm:
    portEnabled: true
    {'enabled: true' if apm_enabled else 'enabled: false'}

  # Process collection
  processAgent:
    enabled: true
    processCollection: true

  # Network monitoring
  networkMonitoring:
    enabled: true

  # Cluster checks
  clusterChecks:
    enabled: true

  # Tags
  tags:
    - "client:{client_name}"
    - "env:production"
    - "managed_by:helm"

# Cluster Agent
clusterAgent:
  enabled: true
  metricsProvider:
    enabled: true

# Kube State Metrics
kubeStateMetricsCore:
  enabled: true

# Node Agent
agents:
  # Tolerate all taints
  tolerations:
    - operator: Exists

  # Container resources
  containers:
    agent:
      resources:
        requests:
          cpu: 200m
          memory: 256Mi
        limits:
          cpu: 200m
          memory: 256Mi
```

### 4. Install the Datadog Agent

```bash
helm install datadog-agent datadog/datadog \\
  --namespace datadog \\
  --values values.yaml
```

## Verify Installation

```bash
# Check pods are running
kubectl get pods -n datadog

# Check agent status
kubectl exec -it $(kubectl get pods -n datadog -l app=datadog -o jsonpath='{{.items[0].metadata.name}}') -n datadog -- agent status

# Check cluster agent
kubectl exec -it $(kubectl get pods -n datadog -l app=datadog-cluster-agent -o jsonpath='{{.items[0].metadata.name}}') -n datadog -- datadog-cluster-agent status
```

## Configuration Updates

```bash
# Update values
helm upgrade datadog-agent datadog/datadog \\
  --namespace datadog \\
  --values values.yaml
```

## Integration Configs via ConfigMap

```yaml
# Example: nginx integration
apiVersion: v1
kind: ConfigMap
metadata:
  name: datadog-nginx-config
  namespace: datadog
data:
  nginx.yaml: |
    ad_identifiers:
      - nginx
    init_config:
    instances:
      - nginx_status_url: http://%%host%%/nginx_status
```

Then update Helm values:

```yaml
datadog:
  confd:
    nginx.yaml: |-
      ad_identifiers:
        - nginx
      init_config:
      instances:
        - nginx_status_url: http://%%host%%/nginx_status
```

## APM Instrumentation

For APM, applications need to send traces to the agent:

```yaml
# In application deployment
env:
  - name: DD_AGENT_HOST
    valueFrom:
      fieldRef:
        fieldPath: status.hostIP
  - name: DD_TRACE_AGENT_PORT
    value: "8126"
```

## Troubleshooting

### Pods not starting

```bash
# Check events
kubectl describe pod <pod-name> -n datadog

# Check logs
kubectl logs <pod-name> -n datadog -c agent
```

### No data in Datadog

1. Verify secret contains correct API key
2. Check network policies allow egress to `*.{site}`
3. Verify RBAC permissions

### Cluster Agent issues

```bash
# Check cluster agent logs
kubectl logs -l app=datadog-cluster-agent -n datadog

# Verify cluster role bindings
kubectl get clusterrolebinding | grep datadog
```

## Useful Commands

```bash
# Restart agent daemonset
kubectl rollout restart daemonset datadog-agent -n datadog

# Get agent logs
kubectl logs -l app=datadog -n datadog --tail=100

# Run agent check
kubectl exec -it <agent-pod> -n datadog -- agent check kubernetes
```
'''


def generate_docker_doc(config: dict) -> str:
    """Generate docker.md deployment documentation."""
    client_name = config.get('client_name', 'client')
    site = get_site(config)
    apm_enabled = config.get('monitoring', {}).get('apm', False)

    apm_port = '-p 8126:8126 \\\n  ' if apm_enabled else ''
    apm_env = '-e DD_APM_ENABLED=true \\\n  ' if apm_enabled else ''

    return f'''# Docker Deployment Guide

## Prerequisites

- Docker installed
- Access to Docker socket (for container discovery)

## Quick Start

```bash
docker run -d --name datadog-agent \\
  -e DD_API_KEY="YOUR_API_KEY" \\
  -e DD_SITE="{site}" \\
  -e DD_LOGS_ENABLED=true \\
  -e DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true \\
  -e DD_PROCESS_AGENT_ENABLED=true \\
  {apm_env}-e DD_TAGS="client:{client_name} env:production" \\
  -v /var/run/docker.sock:/var/run/docker.sock:ro \\
  -v /proc/:/host/proc/:ro \\
  -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \\
  -v /var/lib/docker/containers:/var/lib/docker/containers:ro \\
  {apm_port}gcr.io/datadoghq/agent:7
```

## Docker Compose

```yaml
# docker-compose.yaml
version: '3.8'

services:
  datadog-agent:
    image: gcr.io/datadoghq/agent:7
    container_name: datadog-agent
    environment:
      - DD_API_KEY=${{DD_API_KEY}}
      - DD_SITE={site}
      - DD_LOGS_ENABLED=true
      - DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true
      - DD_PROCESS_AGENT_ENABLED=true
      {f'- DD_APM_ENABLED=true' if apm_enabled else ''}
      - DD_TAGS=client:{client_name} env:production
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /proc/:/host/proc/:ro
      - /sys/fs/cgroup/:/host/sys/fs/cgroup:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - ./conf.d:/etc/datadog-agent/conf.d:ro
    {f'ports:\n      - "8126:8126"' if apm_enabled else ''}
    restart: unless-stopped
```

Run with:
```bash
DD_API_KEY="your-api-key" docker-compose up -d
```

## Custom Configuration

Mount your configuration files:

```bash
docker run -d --name datadog-agent \\
  -e DD_API_KEY="YOUR_API_KEY" \\
  -e DD_SITE="{site}" \\
  -v $(pwd)/datadog.yaml:/etc/datadog-agent/datadog.yaml:ro \\
  -v $(pwd)/conf.d:/etc/datadog-agent/conf.d:ro \\
  -v /var/run/docker.sock:/var/run/docker.sock:ro \\
  -v /proc/:/host/proc/:ro \\
  -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \\
  gcr.io/datadoghq/agent:7
```

## Container Autodiscovery

The agent automatically discovers containers via Docker labels:

```yaml
# Example: Label your nginx container
services:
  nginx:
    image: nginx
    labels:
      com.datadoghq.ad.check_names: '["nginx"]'
      com.datadoghq.ad.init_configs: '[{{}}]'
      com.datadoghq.ad.instances: '[{{"nginx_status_url": "http://%%host%%/nginx_status"}}]'
      com.datadoghq.ad.logs: '[{{"source": "nginx", "service": "nginx"}}]'
```

## Verify Installation

```bash
# Check agent status
docker exec datadog-agent agent status

# Check config
docker exec datadog-agent agent configcheck

# View logs
docker logs datadog-agent
```

## Troubleshooting

### Container not collecting logs

1. Verify `DD_LOGS_ENABLED=true`
2. Check volume mount for `/var/lib/docker/containers`
3. Verify container has logs labels or `DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true`

### APM traces not appearing

1. Verify `DD_APM_ENABLED=true`
2. Ensure port 8126 is exposed
3. Application must send traces to the agent host

### Docker socket permission denied

```bash
# Add user to docker group or run with appropriate permissions
sudo chmod 666 /var/run/docker.sock  # Not recommended for production
```
'''


def generate_ecs_doc(config: dict) -> str:
    """Generate ecs.md deployment documentation."""
    client_name = config.get('client_name', 'client')
    site = get_site(config)

    return f'''# Amazon ECS Deployment Guide

## Prerequisites

- ECS cluster (EC2 or Fargate)
- IAM permissions for task registration
- Datadog API key stored in AWS Secrets Manager (recommended)

## EC2 Launch Type

### Task Definition

```json
{{
  "family": "datadog-agent-task",
  "containerDefinitions": [
    {{
      "name": "datadog-agent",
      "image": "gcr.io/datadoghq/agent:7",
      "cpu": 100,
      "memory": 512,
      "essential": true,
      "environment": [
        {{"name": "DD_API_KEY", "value": "YOUR_API_KEY"}},
        {{"name": "DD_SITE", "value": "{site}"}},
        {{"name": "DD_LOGS_ENABLED", "value": "true"}},
        {{"name": "DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL", "value": "true"}},
        {{"name": "DD_PROCESS_AGENT_ENABLED", "value": "true"}},
        {{"name": "DD_TAGS", "value": "client:{client_name} env:production"}},
        {{"name": "ECS_FARGATE", "value": "false"}}
      ],
      "mountPoints": [
        {{
          "sourceVolume": "docker-sock",
          "containerPath": "/var/run/docker.sock",
          "readOnly": true
        }},
        {{
          "sourceVolume": "proc",
          "containerPath": "/host/proc",
          "readOnly": true
        }},
        {{
          "sourceVolume": "cgroup",
          "containerPath": "/host/sys/fs/cgroup",
          "readOnly": true
        }}
      ]
    }}
  ],
  "volumes": [
    {{"name": "docker-sock", "host": {{"sourcePath": "/var/run/docker.sock"}}}},
    {{"name": "proc", "host": {{"sourcePath": "/proc"}}}},
    {{"name": "cgroup", "host": {{"sourcePath": "/sys/fs/cgroup"}}}}
  ],
  "requiresCompatibilities": ["EC2"]
}}
```

### Create Daemon Service

```bash
aws ecs create-service \\
  --cluster your-cluster \\
  --service-name datadog-agent \\
  --task-definition datadog-agent-task \\
  --scheduling-strategy DAEMON
```

## Using AWS Secrets Manager

```json
{{
  "environment": [
    {{"name": "DD_SITE", "value": "{site}"}}
  ],
  "secrets": [
    {{
      "name": "DD_API_KEY",
      "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789:secret:datadog-api-key"
    }}
  ]
}}
```

## Verify Installation

```bash
# Check service status
aws ecs describe-services \\
  --cluster your-cluster \\
  --services datadog-agent

# View agent logs
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
'''


def generate_fargate_doc(config: dict) -> str:
    """Generate fargate.md deployment documentation."""
    client_name = config.get('client_name', 'client')
    site = get_site(config)
    apm_enabled = config.get('monitoring', {}).get('apm', False)

    return f'''# AWS Fargate Sidecar Deployment Guide

## Overview

For Fargate, the Datadog Agent runs as a sidecar container in each task.

## Task Definition

Add the Datadog Agent container as a sidecar:

```json
{{
  "family": "my-app-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {{
      "name": "my-app",
      "image": "my-app:latest",
      "essential": true,
      "portMappings": [
        {{"containerPort": 8080, "protocol": "tcp"}}
      ],
      "environment": [
        {{"name": "DD_AGENT_HOST", "value": "localhost"}},
        {{"name": "DD_TRACE_AGENT_PORT", "value": "8126"}}
      ],
      "logConfiguration": {{
        "logDriver": "awsfirelens",
        "options": {{
          "Name": "datadog",
          "apikey": "YOUR_API_KEY",
          "Host": "http-intake.logs.{site}",
          "dd_service": "my-app",
          "dd_source": "my-app",
          "dd_tags": "client:{client_name},env:production",
          "TLS": "on",
          "provider": "ecs"
        }}
      }},
      "dependsOn": [
        {{"containerName": "datadog-agent", "condition": "START"}}
      ]
    }},
    {{
      "name": "datadog-agent",
      "image": "gcr.io/datadoghq/agent:7",
      "essential": true,
      "environment": [
        {{"name": "DD_API_KEY", "value": "YOUR_API_KEY"}},
        {{"name": "DD_SITE", "value": "{site}"}},
        {{"name": "ECS_FARGATE", "value": "true"}},
        {{"name": "DD_APM_ENABLED", "value": "{'true' if apm_enabled else 'false'}"}},
        {{"name": "DD_LOGS_ENABLED", "value": "true"}},
        {{"name": "DD_TAGS", "value": "client:{client_name} env:production"}}
      ],
      "portMappings": [
        {{"containerPort": 8126, "protocol": "tcp"}}
      ]
    }},
    {{
      "name": "log_router",
      "image": "amazon/aws-for-fluent-bit:stable",
      "essential": true,
      "firelensConfiguration": {{
        "type": "fluentbit"
      }}
    }}
  ]
}}
```

## Using AWS Secrets Manager

```json
{{
  "secrets": [
    {{
      "name": "DD_API_KEY",
      "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789:secret:datadog-api-key"
    }}
  ]
}}
```

## IAM Task Role

Add these permissions to the task role:

```json
{{
  "Version": "2012-10-17",
  "Statement": [
    {{
      "Effect": "Allow",
      "Action": [
        "ecs:ListClusters",
        "ecs:ListContainerInstances",
        "ecs:DescribeContainerInstances"
      ],
      "Resource": "*"
    }}
  ]
}}
```

## Verify Installation

Check agent container logs:

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
'''


def generate_agent_configs(config: dict, output_dir: str, dry_run: bool = False):
    """Generate all agent configuration files."""
    output_path = Path(output_dir)

    # Track generated files
    generated_files = []

    # Create directory structure
    if not dry_run:
        (output_path / 'conf.d').mkdir(parents=True, exist_ok=True)
        (output_path / 'docs').mkdir(parents=True, exist_ok=True)

    # Generate main datadog.yaml
    content = generate_datadog_yaml(config)
    filepath = output_path / 'datadog.yaml'
    generated_files.append(('datadog.yaml', content))
    if not dry_run:
        with open(filepath, 'w') as f:
            f.write(content)

    # Generate conf.d files
    services = config.get('services', {})
    infra = config.get('infrastructure', {})

    # Always generate
    configs_to_generate = [
        ('custom_logs.yaml', generate_custom_logs_yaml(config)),
        ('process.yaml', generate_process_yaml(config)),
    ]

    # Conditional configs based on services
    web_servers = services.get('web_servers', [])
    message_queues = services.get('message_queues', [])
    caching = services.get('caching', [])
    databases = infra.get('databases', {})
    self_managed_dbs = databases.get('self_managed', [])

    if web_servers or services.get('app_servers'):
        configs_to_generate.append(('http_check.yaml', generate_http_check_yaml(config)))

    if self_managed_dbs or message_queues or caching:
        configs_to_generate.append(('tcp_check.yaml', generate_tcp_check_yaml(config)))

    if 'nginx' in web_servers:
        configs_to_generate.append(('nginx.yaml', generate_nginx_yaml(config)))

    if 'mysql' in [d.lower() for d in self_managed_dbs] or 'MySQL' in self_managed_dbs:
        configs_to_generate.append(('mysql.yaml', generate_mysql_yaml(config)))

    if 'postgresql' in [d.lower() for d in self_managed_dbs] or 'PostgreSQL' in self_managed_dbs:
        configs_to_generate.append(('postgres.yaml', generate_postgres_yaml(config)))

    if 'redis' in [d.lower() for d in self_managed_dbs] or 'Redis' in self_managed_dbs or 'Redis' in caching:
        configs_to_generate.append(('redis.yaml', generate_redis_yaml(config)))

    if 'RabbitMQ' in message_queues:
        configs_to_generate.append(('rabbitmq.yaml', generate_rabbitmq_yaml(config)))

    if 'Apache Kafka' in message_queues or 'Kafka' in message_queues:
        configs_to_generate.append(('kafka.yaml', generate_kafka_yaml(config)))

    # Write conf.d files
    for filename, content in configs_to_generate:
        filepath = output_path / 'conf.d' / filename
        generated_files.append((f'conf.d/{filename}', content))
        if not dry_run:
            with open(filepath, 'w') as f:
                f.write(content)

    # Generate documentation
    docs_to_generate = [
        ('README.md', generate_readme(config)),
        ('linux-host.md', generate_linux_host_doc(config)),
    ]

    # Conditional docs
    hosts = infra.get('hosts', {})
    containers = infra.get('containers', {})
    serverless = infra.get('serverless', {})

    if hosts.get('windows'):
        docs_to_generate.append(('windows-host.md', generate_windows_host_doc(config)))

    if containers.get('enabled'):
        if containers.get('kubernetes') or containers.get('eks') or containers.get('gke') or containers.get('aks'):
            docs_to_generate.append(('kubernetes.md', generate_kubernetes_doc(config)))

        if containers.get('docker_swarm') or not (containers.get('kubernetes') or containers.get('eks') or containers.get('ecs')):
            docs_to_generate.append(('docker.md', generate_docker_doc(config)))

        if containers.get('ecs'):
            docs_to_generate.append(('ecs.md', generate_ecs_doc(config)))

    if serverless.get('fargate'):
        docs_to_generate.append(('fargate.md', generate_fargate_doc(config)))

    # Write docs
    for filename, content in docs_to_generate:
        filepath = output_path / 'docs' / filename
        generated_files.append((f'docs/{filename}', content))
        if not dry_run:
            with open(filepath, 'w') as f:
                f.write(content)

    return generated_files


def main():
    parser = argparse.ArgumentParser(
        description='Generate Datadog agent configurations from questionnaire'
    )
    parser.add_argument(
        'config_path',
        help='Path to config JSON file (use - for stdin)'
    )
    parser.add_argument(
        '--output-dir',
        required=True,
        help='Output directory for agent configuration files'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be generated without writing files'
    )

    args = parser.parse_args()

    # Read configuration
    if args.config_path == '-':
        config = json.load(sys.stdin)
    else:
        with open(args.config_path, 'r') as f:
            config = json.load(f)

    # Generate configs
    generated_files = generate_agent_configs(config, args.output_dir, args.dry_run)

    if args.dry_run:
        print("=== Dry Run: Would Generate ===\n")
        for filepath, content in generated_files:
            print(f"--- {filepath} ---")
            # Show first 30 lines
            lines = content.split('\n')[:30]
            print('\n'.join(lines))
            if len(content.split('\n')) > 30:
                print('... (truncated)')
            print()
    else:
        print(f"Generated {len(generated_files)} files in {args.output_dir}:")
        for filepath, _ in generated_files:
            print(f"  - {filepath}")


if __name__ == '__main__':
    main()
