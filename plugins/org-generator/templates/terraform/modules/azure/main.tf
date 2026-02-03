terraform {
  required_providers {
    datadog = {
      source = "Datadog/datadog"
    }
  }
}

#---------------------------------------------
# Azure VM Monitors
#---------------------------------------------

resource "datadog_monitor" "azure_vm_high_cpu" {
  name  = "[Azure] VM High CPU Utilization"
  type  = "query alert"
  query = "avg(last_10m):avg:azure.vm.percentage_cpu{*} by {name,resource_group} > 90"

  monitor_thresholds {
    critical          = 90
    critical_recovery = 85
    warning           = 80
    warning_recovery  = 75
  }

  message = <<-EOF
    {{#is_alert}}
      Azure VM high CPU utilization
      VM: {{name.name}}
      Resource Group: {{resource_group.name}}
      CPU: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Azure VM CPU recovered for {{name.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.azure_tags
}

resource "datadog_monitor" "azure_vm_disk_utilization" {
  name  = "[Azure] VM Disk Utilization"
  type  = "query alert"
  query = "avg(last_10m):avg:azure.vm.os_disk_usage_percentage{*} by {name,resource_group} > 85"

  monitor_thresholds {
    critical          = 85
    critical_recovery = 80
    warning           = 75
    warning_recovery  = 70
  }

  message = <<-EOF
    {{#is_alert}}
      Azure VM disk utilization high
      VM: {{name.name}}
      Resource Group: {{resource_group.name}}
      Disk: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Azure VM disk recovered for {{name.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 2

  tags = var.azure_tags
}

#---------------------------------------------
# Azure SQL Database Monitors
#---------------------------------------------

resource "datadog_monitor" "azure_sql_high_dtu" {
  name  = "[Azure] SQL Database High DTU"
  type  = "query alert"
  query = "avg(last_10m):avg:azure.sql_database.dtu_consumption_percent{*} by {name,resource_group,server_name} > 90"

  monitor_thresholds {
    critical          = 90
    critical_recovery = 85
    warning           = 80
    warning_recovery  = 75
  }

  message = <<-EOF
    {{#is_alert}}
      Azure SQL Database high DTU consumption
      Database: {{name.name}}
      Server: {{server_name.name}}
      DTU: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Azure SQL DTU recovered for {{name.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.azure_tags
}

resource "datadog_monitor" "azure_sql_storage" {
  name  = "[Azure] SQL Database Storage"
  type  = "query alert"
  query = "avg(last_10m):avg:azure.sql_database.storage_percent{*} by {name,resource_group,server_name} > 85"

  monitor_thresholds {
    critical          = 85
    critical_recovery = 80
    warning           = 75
    warning_recovery  = 70
  }

  message = <<-EOF
    {{#is_alert}}
      Azure SQL Database storage high
      Database: {{name.name}}
      Server: {{server_name.name}}
      Storage: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Azure SQL storage recovered for {{name.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 2

  tags = var.azure_tags
}

resource "datadog_monitor" "azure_sql_deadlocks" {
  name  = "[Azure] SQL Database Deadlocks"
  type  = "query alert"
  query = "sum(last_10m):sum:azure.sql_database.deadlock{*} by {name,resource_group,server_name}.as_count() > 5"

  monitor_thresholds {
    critical          = 5
    critical_recovery = 0
    warning           = 2
    warning_recovery  = 0
  }

  message = <<-EOF
    {{#is_alert}}
      Azure SQL Database deadlocks detected
      Database: {{name.name}}
      Server: {{server_name.name}}
      Deadlocks: {{value}}

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Azure SQL deadlocks resolved for {{name.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.azure_tags
}

#---------------------------------------------
# Azure App Service Monitors
#---------------------------------------------

resource "datadog_monitor" "azure_app_5xx" {
  name  = "[Azure] App Service 5XX Errors"
  type  = "query alert"
  query = "sum(last_10m):sum:azure.app_services.http5xx{*} by {name,resource_group}.as_count() > 50"

  monitor_thresholds {
    critical          = 50
    critical_recovery = 10
    warning           = 20
    warning_recovery  = 5
  }

  message = <<-EOF
    {{#is_alert}}
      Azure App Service 5XX errors
      App: {{name.name}}
      Resource Group: {{resource_group.name}}
      Errors: {{value}}

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Azure App Service errors recovered for {{name.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.azure_tags
}

resource "datadog_monitor" "azure_app_response_time" {
  name  = "[Azure] App Service High Response Time"
  type  = "query alert"
  query = "avg(last_10m):avg:azure.app_services.average_response_time{*} by {name,resource_group} > 5000"

  monitor_thresholds {
    critical          = 5000  # 5 seconds
    critical_recovery = 3000
    warning           = 3000
    warning_recovery  = 2000
  }

  message = <<-EOF
    {{#is_alert}}
      Azure App Service high response time
      App: {{name.name}}
      Resource Group: {{resource_group.name}}
      Response time: {{value}}ms

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Azure App Service response time recovered for {{name.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.azure_tags
}

#---------------------------------------------
# AKS Monitors
#---------------------------------------------

resource "datadog_monitor" "aks_node_not_ready" {
  name  = "[Azure] AKS Node Not Ready"
  type  = "query alert"
  query = "avg(last_10m):avg:azure.kubernetes_service.nodes.ready{*} by {cluster_name,node} < 1"

  monitor_thresholds {
    critical          = 1
    critical_recovery = 1
  }

  message = <<-EOF
    {{#is_alert}}
      AKS node not ready
      Cluster: {{cluster_name.name}}
      Node: {{node.name}}

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      AKS node ready again: {{node.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 2

  tags = var.azure_tags
}
