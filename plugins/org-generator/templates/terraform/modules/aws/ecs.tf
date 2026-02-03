#---------------------------------------------
# ECS Monitors
#---------------------------------------------

resource "datadog_monitor" "ecs_high_cpu" {
  name  = "[AWS] ECS High CPU Utilization"
  type  = "query alert"
  query = "avg(last_10m):avg:aws.ecs.cpuutilization{*} by {servicename,clustername,application_team} > 90"

  monitor_thresholds {
    critical          = 90
    critical_recovery = 85
    warning           = 80
    warning_recovery  = 75
  }

  message = <<-EOF
    {{#is_alert}}
      ECS high CPU utilization
      Service: {{servicename.name}}
      Cluster: {{clustername.name}}
      Application: {{application_team.name}}
      CPU: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      ECS CPU recovered for {{servicename.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  evaluation_delay         = 900
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.ecs_tags
}

resource "datadog_monitor" "ecs_high_memory" {
  name  = "[AWS] ECS High Memory Utilization"
  type  = "query alert"
  query = "avg(last_10m):avg:aws.ecs.memory_utilization{*} by {servicename,clustername,application_team} > 90"

  monitor_thresholds {
    critical          = 90
    critical_recovery = 85
    warning           = 80
    warning_recovery  = 75
  }

  message = <<-EOF
    {{#is_alert}}
      ECS high memory utilization
      Service: {{servicename.name}}
      Cluster: {{clustername.name}}
      Application: {{application_team.name}}
      Memory: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      ECS memory recovered for {{servicename.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  evaluation_delay         = 900
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.ecs_tags
}

resource "datadog_monitor" "fargate_cpu_limit" {
  name  = "[ECS] Fargate Task Reaching CPU Limit"
  type  = "query alert"
  query = "avg(last_5m):avg:ecs.fargate.cpu.percent{*} by {ecs_cluster,task_name,container_name} > 95"

  monitor_thresholds {
    critical          = 95
    critical_recovery = 80
    warning           = 85
    warning_recovery  = 70
  }

  message = <<-EOF
    {{#is_alert}}
      Fargate task reaching CPU limit
      Cluster: {{ecs_cluster.name}}
      Task: {{task_name.name}}
      Container: {{container_name.name}}
      CPU: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Fargate CPU recovered for {{task_name.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.ecs_tags
}

resource "datadog_monitor" "fargate_memory_limit" {
  name  = "[ECS] Fargate Task Reaching Memory Limit"
  type  = "query alert"
  query = "avg(last_5m):avg:ecs.fargate.mem.usage{*} by {ecs_cluster,task_name,container_name} / avg:ecs.fargate.mem.limit{*} by {ecs_cluster,task_name,container_name} * 100 > 90"

  monitor_thresholds {
    critical          = 90
    critical_recovery = 80
    warning           = 80
    warning_recovery  = 70
  }

  message = <<-EOF
    {{#is_alert}}
      Fargate task reaching memory limit
      Cluster: {{ecs_cluster.name}}
      Task: {{task_name.name}}
      Container: {{container_name.name}}
      Memory: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Fargate memory recovered for {{task_name.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.ecs_tags
}
