terraform {
  required_providers {
    datadog = {
      source = "Datadog/datadog"
    }
  }
}

#---------------------------------------------
# Compute Engine Monitors
#---------------------------------------------

resource "datadog_monitor" "gce_high_cpu" {
  name  = "[GCP] Compute Engine High CPU"
  type  = "query alert"
  query = "avg(last_10m):avg:gcp.compute.instance.cpu.utilization{*} by {instance_name,project_id} * 100 > 90"

  monitor_thresholds {
    critical          = 90
    critical_recovery = 85
    warning           = 80
    warning_recovery  = 75
  }

  message = <<-EOF
    {{#is_alert}}
      GCE instance high CPU utilization
      Instance: {{instance_name.name}}
      Project: {{project_id.name}}
      CPU: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      GCE CPU recovered for {{instance_name.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.gcp_tags
}

resource "datadog_monitor" "gce_disk_utilization" {
  name  = "[GCP] Compute Engine Disk Utilization"
  type  = "query alert"
  query = "avg(last_10m):avg:gcp.compute.instance.disk.utilization{*} by {instance_name,project_id,device_name} * 100 > 85"

  monitor_thresholds {
    critical          = 85
    critical_recovery = 80
    warning           = 75
    warning_recovery  = 70
  }

  message = <<-EOF
    {{#is_alert}}
      GCE disk utilization high
      Instance: {{instance_name.name}}
      Device: {{device_name.name}}
      Utilization: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      GCE disk utilization recovered for {{instance_name.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.gcp_tags
}

#---------------------------------------------
# Cloud SQL Monitors
#---------------------------------------------

resource "datadog_monitor" "cloudsql_high_cpu" {
  name  = "[GCP] Cloud SQL High CPU"
  type  = "query alert"
  query = "avg(last_10m):avg:gcp.cloudsql.database.cpu.utilization{*} by {database_id,project_id} * 100 > 85"

  monitor_thresholds {
    critical          = 85
    critical_recovery = 80
    warning           = 75
    warning_recovery  = 70
  }

  message = <<-EOF
    {{#is_alert}}
      Cloud SQL high CPU utilization
      Database: {{database_id.name}}
      Project: {{project_id.name}}
      CPU: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Cloud SQL CPU recovered for {{database_id.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.gcp_tags
}

resource "datadog_monitor" "cloudsql_high_memory" {
  name  = "[GCP] Cloud SQL High Memory"
  type  = "query alert"
  query = "avg(last_10m):avg:gcp.cloudsql.database.memory.utilization{*} by {database_id,project_id} * 100 > 90"

  monitor_thresholds {
    critical          = 90
    critical_recovery = 85
    warning           = 80
    warning_recovery  = 75
  }

  message = <<-EOF
    {{#is_alert}}
      Cloud SQL high memory utilization
      Database: {{database_id.name}}
      Project: {{project_id.name}}
      Memory: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Cloud SQL memory recovered for {{database_id.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.gcp_tags
}

resource "datadog_monitor" "cloudsql_high_connections" {
  name  = "[GCP] Cloud SQL High Connections"
  type  = "query alert"
  query = "avg(last_10m):avg:gcp.cloudsql.database.num_connections{*} by {database_id,project_id} > 1000"

  monitor_thresholds {
    critical          = 1000
    critical_recovery = 800
    warning           = 800
    warning_recovery  = 600
  }

  message = <<-EOF
    {{#is_alert}}
      Cloud SQL high connection count
      Database: {{database_id.name}}
      Project: {{project_id.name}}
      Connections: {{value}}

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Cloud SQL connections recovered for {{database_id.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.gcp_tags
}

resource "datadog_monitor" "cloudsql_disk_utilization" {
  name  = "[GCP] Cloud SQL Disk Utilization"
  type  = "query alert"
  query = "avg(last_10m):avg:gcp.cloudsql.database.disk.utilization{*} by {database_id,project_id} * 100 > 85"

  monitor_thresholds {
    critical          = 85
    critical_recovery = 80
    warning           = 75
    warning_recovery  = 70
  }

  message = <<-EOF
    {{#is_alert}}
      Cloud SQL disk utilization high
      Database: {{database_id.name}}
      Project: {{project_id.name}}
      Disk: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Cloud SQL disk recovered for {{database_id.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 2

  tags = var.gcp_tags
}

#---------------------------------------------
# GKE Monitors
#---------------------------------------------

resource "datadog_monitor" "gke_node_not_ready" {
  name  = "[GCP] GKE Node Not Ready"
  type  = "query alert"
  query = "avg(last_10m):avg:gcp.gke.node.status.condition{condition:Ready,status:true} by {cluster_name,node_name} < 1"

  monitor_thresholds {
    critical          = 1
    critical_recovery = 1
  }

  message = <<-EOF
    {{#is_alert}}
      GKE node not ready
      Cluster: {{cluster_name.name}}
      Node: {{node_name.name}}

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      GKE node ready again: {{node_name.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 2

  tags = var.gcp_tags
}

resource "datadog_monitor" "gke_pod_crash_loop" {
  name  = "[GCP] GKE Pod CrashLoopBackOff"
  type  = "query alert"
  query = "sum(last_10m):sum:gcp.gke.pod.restart_count{*} by {cluster_name,namespace,pod_name}.as_count() > 5"

  monitor_thresholds {
    critical          = 5
    critical_recovery = 0
    warning           = 3
    warning_recovery  = 0
  }

  message = <<-EOF
    {{#is_alert}}
      GKE pod restarting frequently
      Cluster: {{cluster_name.name}}
      Namespace: {{namespace.name}}
      Pod: {{pod_name.name}}
      Restarts: {{value}}

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      GKE pod stable: {{pod_name.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.gcp_tags
}
