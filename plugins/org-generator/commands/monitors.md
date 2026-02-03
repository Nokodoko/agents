---
name: monitors
description: Generate monitors based on questionnaire responses
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
argument-hint: "<client-name>"
---

# org-generator:monitors

Generates Datadog monitors based on questionnaire responses. Only creates monitors for selected infrastructure components.

## Usage

```
/org-generator:monitors <client-name>
```

## Arguments

- `client-name`: The client identifier (kebab-case, e.g., `acme-corp`)

## Prerequisites

1. Questionnaire must exist and be filled out
2. Terraform structure must exist (run after /org-generator:scaffold)

## Monitor Categories

### Generic Monitors (Always Generated)

These monitors apply to all deployments:

| Monitor | Query | Threshold |
|---------|-------|-----------|
| High CPU | `avg:system.cpu.user{*} by {host}` | > 90% |
| High Memory | `avg:system.mem.used{*} by {host}` | > 90% |
| Disk Space Low | `avg:system.disk.free{*} by {host,device}` | < 10% |
| Network Errors | `sum:system.net.errors{*} by {host}` | > 100 |

### AWS Monitors (if AWS selected)

| Monitor | Query | Threshold |
|---------|-------|-----------|
| EC2 Status Check Failed | `aws.ec2.status_check_failed` | > 0 |
| RDS High CPU | `aws.rds.cpuutilization` | > 85% |
| RDS Low Memory | `aws.rds.freeable_memory` | < 128MB |
| RDS Write Latency | `aws.rds.write_latency` | > 1s |
| ALB 5XX Errors | `aws.applicationelb.httpcode_elb_5xx` | > 20% |
| ALB High Latency | `aws.applicationelb.target_response_time` | > 5s |
| ECS High CPU | `aws.ecs.cpuutilization` | > 97% |
| Lambda Errors | `aws.lambda.errors` | > 5 |

### GCP Monitors (if GCP selected)

| Monitor | Query | Threshold |
|---------|-------|-----------|
| Compute High CPU | `gcp.compute.instance.cpu.utilization` | > 90% |
| Cloud SQL High CPU | `gcp.cloudsql.database.cpu.utilization` | > 85% |
| Cloud SQL Connections | `gcp.cloudsql.database.num_connections` | > 1000 |
| GKE Node Not Ready | `gcp.gke.node.status.condition` | condition=NotReady |

### Azure Monitors (if Azure selected)

| Monitor | Query | Threshold |
|---------|-------|-----------|
| VM High CPU | `azure.vm.percentage_cpu` | > 90% |
| SQL DTU High | `azure.sql_database.dtu_consumption_percent` | > 90% |
| App Service 5XX | `azure.app_services.http5xx` | > 20% |
| AKS Node Not Ready | `azure.aks.node.status` | NotReady |

### Kubernetes Monitors (if containers selected)

| Monitor | Query | Threshold |
|---------|-------|-----------|
| Deployment Replicas Down | `kubernetes_state.deployment.replicas_desired - replicas_ready` | >= 2 |
| Pods Restarting | `kubernetes.containers.restarts` | > 5 in 5m |
| DaemonSet Pod Down | `kubernetes_state.daemonset.desired - ready` | >= 1 |
| StatefulSet Replica Down | `kubernetes_state.statefulset.replicas_desired - ready` | >= 2 |
| Node Unschedulable | `kubernetes_state.node.status{schedulable}` | < 80% |
| ImagePullBackOff | `kubernetes_state.container.status_report.count.waiting{imagepullbackoff}` | >= 1 |
| Pending Pods | `kubernetes_state.pod.status_phase{pending}` | >= 1 for 30m |

## Monitor Template Pattern

Each monitor follows this pattern:

```hcl
resource "datadog_monitor" "<monitor_name>" {
  name    = "[<CATEGORY>] <Monitor Title>"
  type    = "query alert"
  query   = "<metric query>"

  monitor_thresholds {
    critical          = <threshold>
    critical_recovery = <recovery_threshold>
  }

  message = <<-EOF
    {{#is_alert}}
      <Alert message with template variables>
      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      RECOVERED: <Recovery message>
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.<category>_tags
}
```

## Tag Inheritance

Monitors inherit tags based on category:

```hcl
variable "aws_tags" {
  default = [
    "platform:aws",
    "managed_by:terraform"
  ]
}

variable "kube_tags" {
  default = [
    "platform:kubernetes",
    "managed_by:terraform"
  ]
}
```

## Alert Team Configuration

Generated in `notifications.tf`:

```hcl
variable "alert_teams" {
  type = map(any)
  default = {
    notify = {
      default          = ["@slack-alerts", "@pagerduty-oncall"]
      teamsDirect      = ["@teams-<client-name>-alerts"]
      ticket_teams     = ["@servicenow-<client-name>"]
    }
  }
}
```

## Generation Process

1. Parse questionnaire for selected components
2. For each selected component, include corresponding monitor file
3. Update `modules/<category>/monitors.tf` with appropriate monitors
4. Update variables with tag definitions
5. Run `terraform fmt` to format

## Customization

After generation, customize monitors by:
1. Adjusting thresholds in variables.tf
2. Modifying alert recipients in notifications.tf
3. Adding/removing specific monitors in module files

## Example

```
/org-generator:monitors acme-corp
```

If questionnaire indicates: AWS + RDS + Kubernetes

This will generate:
- Generic monitors (CPU, memory, disk, network)
- AWS monitors (EC2, RDS, ALB)
- Kubernetes monitors (deployments, pods, nodes)

And skip:
- GCP monitors
- Azure monitors
- Lambda monitors (if serverless not selected)
