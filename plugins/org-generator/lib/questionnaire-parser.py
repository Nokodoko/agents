#!/usr/bin/env python3
"""
Questionnaire Parser for org-generator plugin

Parses filled questionnaire markdown files and extracts configuration
for terraform scaffold generation and pruning decisions.

Usage:
    python questionnaire-parser.py <questionnaire-path> [--output json|yaml] [--dry-run]

Example:
    python questionnaire-parser.py ~/datadog_terraform/acme-corp/questionnaire.md --output json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def parse_checkbox(line: str) -> tuple[bool, str]:
    """Parse a checkbox line and return (is_checked, label)."""
    # Match [x], [X], or [ ] checkboxes
    match = re.match(r'^\s*-\s*\[([xX ])\]\s*(.+)$', line)
    if match:
        is_checked = match.group(1).lower() == 'x'
        label = match.group(2).strip()
        return is_checked, label
    return False, ""


def parse_text_field(line: str) -> str | None:
    """Parse an 'Other: ___' or blank field and return the value."""
    # Match patterns like "Other: some value" or "Name: value"
    match = re.match(r'^.*?:\s*(.+)$', line)
    if match:
        value = match.group(1).strip()
        # Ignore placeholder underscores
        if value and not re.match(r'^_+$', value):
            return value
    return None


def parse_table_row(line: str) -> list[str]:
    """Parse a markdown table row and return cell values."""
    if '|' not in line:
        return []
    cells = [cell.strip() for cell in line.split('|')[1:-1]]
    return cells


def extract_section(content: str, section_name: str) -> str:
    """Extract content from a specific section."""
    pattern = rf'##\s*{re.escape(section_name)}\s*\n(.*?)(?=\n##|\Z)'
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)
    return ""


def parse_questionnaire(filepath: str) -> dict[str, Any]:
    """Parse a questionnaire markdown file and return configuration dict."""

    with open(filepath, 'r') as f:
        content = f.read()

    config = {
        'client_name': '',
        'engagement_type': '',
        'organization': {
            'create_child_org': False,
            'use_existing': False,
            'name': '',
            'parent_org': ''
        },
        'cloud_providers': {
            'aws': False,
            'gcp': False,
            'azure': False,
            'on_premise': False,
            'primary': ''
        },
        'infrastructure': {
            'hosts': {
                'enabled': False,
                'linux': False,
                'windows': False,
                'solaris': False
            },
            'containers': {
                'enabled': False,
                'kubernetes': False,
                'eks': False,
                'gke': False,
                'aks': False,
                'ecs': False,
                'docker_swarm': False
            },
            'serverless': {
                'enabled': False,
                'lambda': False,
                'cloud_functions': False,
                'azure_functions': False,
                'fargate': False
            },
            'databases': {
                'rds': False,
                'aurora': False,
                'dynamodb': False,
                'cloudsql': False,
                'azure_sql': False,
                'self_managed': []
            }
        },
        'services': {
            'web_servers': [],
            'app_servers': [],
            'message_queues': [],
            'caching': []
        },
        'monitoring': {
            'apm': False,
            'rum': False,
            'synthetics': False,
            'private_locations': False
        },
        'team_structure': {
            'admin_count': 0,
            'standard_count': 0,
            'readonly_count': 0,
            'roles_needed': []
        },
        'tagging': {
            'environments': [],
            'tags': {}
        },
        'data_residency': 'us',
        'modules_to_include': [],
        'modules_to_exclude': []
    }

    # Extract client name from header
    client_match = re.search(r'\*\*Client Name\*\*:\s*(\S+)', content)
    if client_match:
        config['client_name'] = client_match.group(1)

    # Parse engagement type
    if '[ ] POC' in content and '[x] Production' in content.lower():
        config['engagement_type'] = 'production'
    elif '[x] POC' in content.lower():
        config['engagement_type'] = 'poc'

    # Parse organization setup
    org_section = extract_section(content, '1. Organization Setup')
    for line in org_section.split('\n'):
        checked, label = parse_checkbox(line)
        if checked:
            if 'child organization' in label.lower():
                config['organization']['create_child_org'] = True
            elif 'existing organization' in label.lower():
                config['organization']['use_existing'] = True

    # Parse cloud providers
    cloud_section = extract_section(content, '2. Cloud Providers')
    for line in cloud_section.split('\n'):
        checked, label = parse_checkbox(line)
        if checked:
            label_lower = label.lower()
            if 'aws' in label_lower:
                config['cloud_providers']['aws'] = True
            elif 'gcp' in label_lower or 'google' in label_lower:
                config['cloud_providers']['gcp'] = True
            elif 'azure' in label_lower:
                config['cloud_providers']['azure'] = True
            elif 'on-premise' in label_lower or 'vdc' in label_lower:
                config['cloud_providers']['on_premise'] = True

    # Parse ALL infrastructure components from full content (not just one section)
    # This handles nested checkboxes better

    # Hosts
    for line in content.split('\n'):
        checked, label = parse_checkbox(line)
        if checked:
            label_lower = label.lower()
            if 'linux' in label_lower and 'server' not in label_lower:
                config['infrastructure']['hosts']['linux'] = True
                config['infrastructure']['hosts']['enabled'] = True
            elif 'windows' in label_lower:
                config['infrastructure']['hosts']['windows'] = True
                config['infrastructure']['hosts']['enabled'] = True
            elif 'solaris' in label_lower:
                config['infrastructure']['hosts']['solaris'] = True
                config['infrastructure']['hosts']['enabled'] = True

    # Containers - check full content for better matching
    container_keywords = {
        'kubernetes (self-managed)': 'kubernetes',
        'amazon eks': 'eks',
        'google gke': 'gke',
        'azure aks': 'aks',
        'amazon ecs': 'ecs',
        'docker swarm': 'docker_swarm'
    }
    for line in content.split('\n'):
        checked, label = parse_checkbox(line)
        if checked:
            label_lower = label.lower()
            for keyword, key in container_keywords.items():
                if keyword in label_lower:
                    config['infrastructure']['containers'][key] = True
                    config['infrastructure']['containers']['enabled'] = True

    # Serverless
    serverless_keywords = {
        'aws lambda': 'lambda',
        'google cloud functions': 'cloud_functions',
        'azure functions': 'azure_functions',
        'aws fargate': 'fargate'
    }
    for line in content.split('\n'):
        checked, label = parse_checkbox(line)
        if checked:
            label_lower = label.lower()
            for keyword, key in serverless_keywords.items():
                if keyword in label_lower:
                    config['infrastructure']['serverless'][key] = True
                    config['infrastructure']['serverless']['enabled'] = True

    # Databases
    db_keywords = {
        'amazon rds': 'rds',
        'amazon aurora': 'aurora',
        'amazon dynamodb': 'dynamodb',
        'cloud sql': 'cloudsql',
        'azure sql': 'azure_sql'
    }
    for line in content.split('\n'):
        checked, label = parse_checkbox(line)
        if checked:
            label_lower = label.lower()
            for keyword, key in db_keywords.items():
                if keyword in label_lower:
                    config['infrastructure']['databases'][key] = True

    # Parse monitoring requirements
    # Use regex to find sections and their Yes/No answers

    # APM - look between "### 5.1 APM" and next section
    apm_match = re.search(r'###\s*5\.1.*?APM.*?\n(.*?)(?=###|\Z)', content, re.DOTALL | re.IGNORECASE)
    if apm_match:
        for line in apm_match.group(1).split('\n'):
            checked, label = parse_checkbox(line)
            if checked and label.lower() == 'yes':
                config['monitoring']['apm'] = True

    # RUM
    rum_match = re.search(r'###\s*5\.2.*?RUM.*?\n(.*?)(?=###|\Z)', content, re.DOTALL | re.IGNORECASE)
    if rum_match:
        for line in rum_match.group(1).split('\n'):
            checked, label = parse_checkbox(line)
            if checked and label.lower() == 'yes':
                config['monitoring']['rum'] = True

    # Synthetics
    synth_match = re.search(r'###\s*5\.3.*?Synthetic.*?\n(.*?)(?=###|\Z)', content, re.DOTALL | re.IGNORECASE)
    if synth_match:
        for line in synth_match.group(1).split('\n'):
            checked, label = parse_checkbox(line)
            if checked and label.lower() == 'yes':
                config['monitoring']['synthetics'] = True

    # Private Locations
    pl_match = re.search(r'###\s*5\.4.*?Private.*?\n(.*?)(?=###|---|\Z)', content, re.DOTALL | re.IGNORECASE)
    if pl_match:
        for line in pl_match.group(1).split('\n'):
            checked, label = parse_checkbox(line)
            if checked and 'yes' in label.lower():
                config['monitoring']['private_locations'] = True

    # Parse Services & Applications (Section 4)
    # Web Servers (Section 4.1)
    web_server_keywords = ['nginx', 'apache http server', 'iis']
    for line in content.split('\n'):
        checked, label = parse_checkbox(line)
        if checked:
            label_lower = label.lower()
            for keyword in web_server_keywords:
                if keyword in label_lower:
                    config['services']['web_servers'].append(label)
                    break

    # Application Servers (Section 4.2)
    app_server_keywords = ['node.js', 'java', 'python', '.net', 'go', 'ruby', 'php']
    for line in content.split('\n'):
        checked, label = parse_checkbox(line)
        if checked:
            label_lower = label.lower()
            for keyword in app_server_keywords:
                if keyword in label_lower:
                    config['services']['app_servers'].append(label)
                    break

    # Message Queues (Section 4.3)
    queue_keywords = ['sqs', 'sns', 'rabbitmq', 'kafka', 'service bus', 'pub/sub']
    for line in content.split('\n'):
        checked, label = parse_checkbox(line)
        if checked:
            label_lower = label.lower()
            for keyword in queue_keywords:
                if keyword in label_lower:
                    config['services']['message_queues'].append(label)
                    break

    # Caching (Section 4.4)
    cache_keywords = ['redis', 'memcached', 'varnish', 'cloudfront']
    for line in content.split('\n'):
        checked, label = parse_checkbox(line)
        if checked:
            label_lower = label.lower()
            for keyword in cache_keywords:
                if keyword in label_lower:
                    config['services']['caching'].append(label)
                    break

    # Self-managed databases (under Section 3.4)
    self_managed_db_keywords = ['mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch']
    self_managed_section = re.search(r'\*\*Self-Managed Databases\*\*:(.*?)(?=---|\*\*|\Z)', content, re.DOTALL)
    if self_managed_section:
        for line in self_managed_section.group(1).split('\n'):
            checked, label = parse_checkbox(line)
            if checked:
                label_lower = label.lower()
                for keyword in self_managed_db_keywords:
                    if keyword in label_lower:
                        config['infrastructure']['databases']['self_managed'].append(label)
                        break

    # Parse Data Residency (Section 9.2)
    residency_section = re.search(r'###\s*9\.2\s*Data Residency(.*?)(?=###|---|\Z)', content, re.DOTALL | re.IGNORECASE)
    if residency_section:
        for line in residency_section.group(1).split('\n'):
            checked, label = parse_checkbox(line)
            if checked:
                label_lower = label.lower()
                if 'eu' in label_lower:
                    config['data_residency'] = 'eu'
                elif 'us government' in label_lower or 'govcloud' in label_lower:
                    config['data_residency'] = 'gov'
                elif 'us3' in label_lower:
                    config['data_residency'] = 'us3'
                elif 'us5' in label_lower:
                    config['data_residency'] = 'us5'
                elif 'us' in label_lower:
                    config['data_residency'] = 'us'

    # Determine modules to include/exclude based on selections
    config['modules_to_include'] = determine_modules(config)
    config['modules_to_exclude'] = determine_excluded_modules(config)

    return config


def determine_modules(config: dict) -> list[str]:
    """Determine which modules should be included based on configuration."""
    modules = [
        'api_keys',
        'app_keys',
        'roles',
        'teams',
        'users',
        'generic'  # Always include generic monitors
    ]

    # Cloud providers
    if config['cloud_providers']['aws']:
        modules.append('aws')
    if config['cloud_providers']['gcp']:
        modules.append('gcp')
    if config['cloud_providers']['azure']:
        modules.append('azure')

    # Containers
    if config['infrastructure']['containers']['enabled']:
        modules.append('kube')

    # Monitoring features
    if config['monitoring']['apm']:
        modules.append('apm')
    if config['monitoring']['rum']:
        modules.append('rum')
    if config['monitoring']['synthetics']:
        modules.append('synthetics')
    if config['monitoring']['private_locations']:
        modules.append('private_locations')

    return modules


def determine_excluded_modules(config: dict) -> list[str]:
    """Determine which modules should be excluded based on configuration."""
    all_modules = [
        'aws', 'gcp', 'azure', 'kube',
        'apm', 'rum', 'synthetics', 'private_locations'
    ]

    included = determine_modules(config)
    excluded = [m for m in all_modules if m not in included]

    return excluded


def main():
    parser = argparse.ArgumentParser(
        description='Parse org-generator questionnaire markdown files'
    )
    parser.add_argument(
        'questionnaire_path',
        help='Path to the questionnaire markdown file'
    )
    parser.add_argument(
        '--output',
        choices=['json', 'yaml', 'summary'],
        default='json',
        help='Output format (default: json)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be pruned without making changes'
    )

    args = parser.parse_args()

    if not Path(args.questionnaire_path).exists():
        print(f"Error: File not found: {args.questionnaire_path}", file=sys.stderr)
        sys.exit(1)

    config = parse_questionnaire(args.questionnaire_path)

    if args.dry_run:
        print("=== Dry Run: Pruning Analysis ===\n")
        print(f"Client: {config['client_name']}")
        print(f"Engagement: {config['engagement_type']}")
        print(f"\nModules to INCLUDE ({len(config['modules_to_include'])}):")
        for m in config['modules_to_include']:
            print(f"  + {m}")
        print(f"\nModules to EXCLUDE ({len(config['modules_to_exclude'])}):")
        for m in config['modules_to_exclude']:
            print(f"  - {m}")
        return

    if args.output == 'json':
        print(json.dumps(config, indent=2))
    elif args.output == 'yaml':
        try:
            import yaml
            print(yaml.dump(config, default_flow_style=False))
        except ImportError:
            print("Error: PyYAML not installed. Use --output json instead.", file=sys.stderr)
            sys.exit(1)
    elif args.output == 'summary':
        print(f"Client: {config['client_name']}")
        print(f"Cloud Providers: ", end='')
        providers = [k for k, v in config['cloud_providers'].items() if v and k != 'primary']
        print(', '.join(providers) if providers else 'None')
        print(f"Containers: {'Yes' if config['infrastructure']['containers']['enabled'] else 'No'}")
        print(f"APM: {'Yes' if config['monitoring']['apm'] else 'No'}")
        print(f"RUM: {'Yes' if config['monitoring']['rum'] else 'No'}")
        print(f"Synthetics: {'Yes' if config['monitoring']['synthetics'] else 'No'}")


if __name__ == '__main__':
    main()
