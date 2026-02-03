#!/usr/bin/env python3
"""
Monitor Generator for org-generator plugin

Generates Datadog monitor configurations based on parsed questionnaire responses.
Produces terraform configurations for the monitors module.

Usage:
    python monitor-generator.py <config-json> --output-dir <terraform-dir>

Example:
    python questionnaire-parser.py ~/datadog_terraform/acme-corp/questionnaire.md | \
        python monitor-generator.py - --output-dir ~/datadog_terraform/acme-corp/modules/
"""

import argparse
import json
import sys
from pathlib import Path


# Monitor templates by category
MONITOR_TEMPLATES = {
    'generic': {
        'high_cpu': {
            'name': '[Generic] High CPU Utilization',
            'type': 'query alert',
            'query': 'avg(last_10m):avg:system.cpu.user{*} by {host} > 90',
            'critical': 90,
            'warning': 80,
            'priority': 3
        },
        'high_memory': {
            'name': '[Generic] High Memory Utilization',
            'type': 'query alert',
            'query': 'avg(last_10m):avg:system.mem.pct_usable{*} by {host} < 10',
            'critical': 10,
            'warning': 20,
            'priority': 3
        },
        'disk_space_low': {
            'name': '[Generic] Disk Space Low',
            'type': 'query alert',
            'query': 'avg(last_10m):avg:system.disk.free{*} by {host,device} / avg:system.disk.total{*} by {host,device} * 100 < 10',
            'critical': 10,
            'warning': 20,
            'priority': 2
        }
    },
    'aws': {
        'ec2_status_check': {
            'name': '[AWS] EC2 Status Check Failed',
            'type': 'query alert',
            'query': 'sum(last_5m):sum:aws.ec2.status_check_failed{*} by {host,name} > 0',
            'critical': 0,
            'priority': 2
        },
        'alb_5xx': {
            'name': '[AWS] ALB 5XX Errors',
            'type': 'query alert',
            'query': 'sum(last_1h):(sum:aws.applicationelb.httpcode_elb_5xx{*} by {application_team}.as_count() / (sum:aws.applicationelb.httpcode_elb_5xx{*} by {application_team}.as_count() + sum:aws.applicationelb.httpcode_target_2xx{*} by {application_team}.as_count())) * 100 > 20',
            'critical': 20,
            'priority': 3
        },
        'rds_high_cpu': {
            'name': '[AWS] RDS High CPU Utilization',
            'type': 'query alert',
            'query': 'avg(last_10m):avg:aws.rds.cpuutilization{*} by {dbinstanceidentifier,application_team} > 85',
            'critical': 85,
            'warning': 75,
            'priority': 3
        },
        'rds_low_memory': {
            'name': '[AWS] RDS Low Freeable Memory',
            'type': 'metric alert',
            'query': 'avg(last_10m):avg:aws.rds.freeable_memory{*} by {dbinstanceidentifier,application_team} < 134217728',
            'critical': 134217728,
            'priority': 2
        }
    },
    'gcp': {
        'gce_high_cpu': {
            'name': '[GCP] Compute Engine High CPU',
            'type': 'query alert',
            'query': 'avg(last_10m):avg:gcp.compute.instance.cpu.utilization{*} by {instance_name,project_id} * 100 > 90',
            'critical': 90,
            'warning': 80,
            'priority': 3
        },
        'cloudsql_high_cpu': {
            'name': '[GCP] Cloud SQL High CPU',
            'type': 'query alert',
            'query': 'avg(last_10m):avg:gcp.cloudsql.database.cpu.utilization{*} by {database_id,project_id} * 100 > 85',
            'critical': 85,
            'warning': 75,
            'priority': 3
        }
    },
    'azure': {
        'vm_high_cpu': {
            'name': '[Azure] VM High CPU Utilization',
            'type': 'query alert',
            'query': 'avg(last_10m):avg:azure.vm.percentage_cpu{*} by {name,resource_group} > 90',
            'critical': 90,
            'warning': 80,
            'priority': 3
        },
        'sql_high_dtu': {
            'name': '[Azure] SQL Database High DTU',
            'type': 'query alert',
            'query': 'avg(last_10m):avg:azure.sql_database.dtu_consumption_percent{*} by {name,resource_group,server_name} > 90',
            'critical': 90,
            'warning': 80,
            'priority': 3
        }
    },
    'kube': {
        'deployment_replica_down': {
            'name': '(k8s) Deployment Replica is Down',
            'type': 'query alert',
            'query': 'avg(last_15m):avg:kubernetes_state.deployment.replicas_desired{*} by {cluster_name,deployment} - avg:kubernetes_state.deployment.replicas_ready{*} by {cluster_name,deployment} >= 2',
            'critical': 2,
            'priority': 3
        },
        'pods_restarting': {
            'name': '(k8s) Pods are Restarting',
            'type': 'query alert',
            'query': 'change(sum(last_5m),last_5m):exclude_null(avg:kubernetes.containers.restarts{*} by {cluster_name,kube_namespace,pod_name}) > 5',
            'critical': 5,
            'warning': 3,
            'priority': 3
        },
        'imagepullbackoff': {
            'name': '(k8s) ImagePullBackOff',
            'type': 'query alert',
            'query': 'max(last_10m):max:kubernetes_state.container.status_report.count.waiting{reason:imagepullbackoff} by {kube_cluster_name,kube_namespace,pod_name} >= 1',
            'critical': 1,
            'priority': 3
        }
    }
}


def generate_terraform_monitor(name: str, monitor: dict, tags: list[str]) -> str:
    """Generate terraform resource block for a monitor."""
    resource_name = name.lower().replace(' ', '_').replace('[', '').replace(']', '').replace('(', '').replace(')', '')

    # Build thresholds block
    thresholds = []
    if 'critical' in monitor:
        thresholds.append(f'    critical = {monitor["critical"]}')
    if 'warning' in monitor:
        thresholds.append(f'    warning  = {monitor["warning"]}')
    thresholds_block = '\n'.join(thresholds)

    tags_str = ', '.join([f'"{t}"' for t in tags])

    # Note: In HCL heredocs, $${...} escapes to literal ${...}
    # Datadog template variables use {{...}} - we use {{{{ }}}} in f-string to output {{ }}
    return f'''
resource "datadog_monitor" "{resource_name}" {{
  name  = "{monitor['name']}"
  type  = "{monitor['type']}"
  query = "{monitor['query']}"

  monitor_thresholds {{
{thresholds_block}
  }}

  message = <<-EOF
    {{{{#is_alert}}}}
      Alert: {monitor['name']}
      $${{join(",", var.alert_teams["notify"]["default"])}}
    {{{{/is_alert}}}}

    {{{{#is_recovery}}}}
      Recovered: {monitor['name']}
    {{{{/is_recovery}}}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = {monitor.get('priority', 3)}

  tags = [{tags_str}]
}}
'''


def generate_monitors_for_category(category: str, monitors: dict, config: dict) -> str:
    """Generate terraform file content for a category of monitors."""
    output = f'''terraform {{
  required_providers {{
    datadog = {{
      source = "Datadog/datadog"
    }}
  }}
}}

#---------------------------------------------
# {category.upper()} Monitors
# Generated based on questionnaire responses
#---------------------------------------------

'''

    # Determine tags based on category
    tags = ['managed_by:terraform']
    if category == 'aws':
        tags.append('platform:aws')
    elif category == 'gcp':
        tags.append('platform:gcp')
    elif category == 'azure':
        tags.append('platform:azure')
    elif category == 'kube':
        tags.append('platform:kubernetes')

    if config.get('client_name'):
        tags.append(f"client:{config['client_name']}")

    # Generate each monitor
    for name, monitor in monitors.items():
        output += generate_terraform_monitor(name, monitor, tags)

    return output


def generate_monitors(config: dict) -> dict[str, str]:
    """Generate monitor terraform files based on configuration."""
    generated_files = {}

    # Always generate generic monitors
    if 'generic' not in config.get('modules_to_exclude', []):
        content = generate_monitors_for_category('generic', MONITOR_TEMPLATES['generic'], config)
        generated_files['generic'] = content

    # Conditional monitors based on cloud providers
    if config['cloud_providers'].get('aws') and 'aws' not in config.get('modules_to_exclude', []):
        content = generate_monitors_for_category('aws', MONITOR_TEMPLATES['aws'], config)
        generated_files['aws'] = content

    if config['cloud_providers'].get('gcp') and 'gcp' not in config.get('modules_to_exclude', []):
        content = generate_monitors_for_category('gcp', MONITOR_TEMPLATES['gcp'], config)
        generated_files['gcp'] = content

    if config['cloud_providers'].get('azure') and 'azure' not in config.get('modules_to_exclude', []):
        content = generate_monitors_for_category('azure', MONITOR_TEMPLATES['azure'], config)
        generated_files['azure'] = content

    # Kubernetes monitors
    if config['infrastructure']['containers'].get('enabled') and 'kube' not in config.get('modules_to_exclude', []):
        content = generate_monitors_for_category('kube', MONITOR_TEMPLATES['kube'], config)
        generated_files['kube'] = content

    return generated_files


def write_monitors(generated_files: dict[str, str], output_dir: str):
    """Write generated monitor files to the output directory."""
    output_path = Path(output_dir)

    for category, content in generated_files.items():
        module_dir = output_path / category
        module_dir.mkdir(parents=True, exist_ok=True)

        filepath = module_dir / 'monitors_generated.tf'
        with open(filepath, 'w') as f:
            f.write(content)

        print(f"Generated: {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate Datadog monitors from questionnaire configuration'
    )
    parser.add_argument(
        'config_path',
        help='Path to config JSON file (use - for stdin)'
    )
    parser.add_argument(
        '--output-dir',
        required=True,
        help='Output directory for generated terraform files'
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

    # Generate monitors
    generated_files = generate_monitors(config)

    if args.dry_run:
        print("=== Dry Run: Would Generate ===\n")
        for category, content in generated_files.items():
            print(f"--- {category}/monitors_generated.tf ---")
            print(content[:500] + "..." if len(content) > 500 else content)
            print()
        return

    # Write files
    write_monitors(generated_files, args.output_dir)

    print(f"\nGenerated {len(generated_files)} monitor files")


if __name__ == '__main__':
    main()
