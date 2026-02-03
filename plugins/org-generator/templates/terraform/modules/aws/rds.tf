#---------------------------------------------
# RDS Monitors
#---------------------------------------------

resource "datadog_monitor" "rds_high_cpu" {
  name  = "[AWS] RDS High CPU Utilization"
  type  = "query alert"
  query = "avg(last_10m):avg:aws.rds.cpuutilization{*} by {dbinstanceidentifier,application_team} > 85"

  monitor_thresholds {
    critical          = 85
    critical_recovery = 80
    warning           = 75
    warning_recovery  = 70
  }

  message = <<-EOF
    {{#is_alert}}
      RDS high CPU utilization
      Instance: {{dbinstanceidentifier.name}}
      Application: {{application_team.name}}
      CPU: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      RDS CPU recovered for {{dbinstanceidentifier.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  evaluation_delay         = 900
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.rds_tags
}

resource "datadog_monitor" "rds_low_memory" {
  name  = "[AWS] RDS Low Freeable Memory"
  type  = "metric alert"
  query = "avg(last_10m):avg:aws.rds.freeable_memory{*} by {dbinstanceidentifier,application_team} < 134217728"

  monitor_thresholds {
    critical          = 134217728   # 128 MB
    critical_recovery = 268435456   # 256 MB
    warning           = 268435456   # 256 MB
    warning_recovery  = 536870912   # 512 MB
  }

  message = <<-EOF
    {{#is_alert}}
      RDS freeable memory critically low
      Instance: {{dbinstanceidentifier.name}}
      Application: {{application_team.name}}
      Memory: {{value}} bytes

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      RDS memory recovered for {{dbinstanceidentifier.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  evaluation_delay         = 900
  require_full_window      = false
  include_tags             = true
  priority                 = 2

  tags = var.rds_tags
}

resource "datadog_monitor" "rds_high_write_latency" {
  name  = "[AWS] RDS High Write Latency"
  type  = "query alert"
  query = "avg(last_5m):avg:aws.rds.write_latency{*} by {dbinstanceidentifier,application_team} > 1"

  monitor_thresholds {
    critical          = 1
    critical_recovery = 0.5
    warning           = 0.5
    warning_recovery  = 0.25
  }

  message = <<-EOF
    {{#is_alert}}
      RDS high write latency
      Instance: {{dbinstanceidentifier.name}}
      Application: {{application_team.name}}
      Latency: {{value}}s

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      RDS write latency recovered for {{dbinstanceidentifier.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  evaluation_delay         = 900
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.rds_tags
}

resource "datadog_monitor" "rds_high_read_latency" {
  name  = "[AWS] RDS High Read Latency"
  type  = "query alert"
  query = "avg(last_5m):avg:aws.rds.read_latency{*} by {dbinstanceidentifier,application_team} > 1"

  monitor_thresholds {
    critical          = 1
    critical_recovery = 0.5
    warning           = 0.5
    warning_recovery  = 0.25
  }

  message = <<-EOF
    {{#is_alert}}
      RDS high read latency
      Instance: {{dbinstanceidentifier.name}}
      Application: {{application_team.name}}
      Latency: {{value}}s

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      RDS read latency recovered for {{dbinstanceidentifier.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  evaluation_delay         = 900
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.rds_tags
}

resource "datadog_monitor" "rds_high_connections" {
  name  = "[AWS] RDS High Database Connections"
  type  = "query alert"
  query = "avg(last_10m):avg:aws.rds.database_connections{*} by {dbinstanceidentifier,application_team} > 500"

  monitor_thresholds {
    critical          = 500
    critical_recovery = 400
    warning           = 400
    warning_recovery  = 300
  }

  message = <<-EOF
    {{#is_alert}}
      RDS high connection count
      Instance: {{dbinstanceidentifier.name}}
      Application: {{application_team.name}}
      Connections: {{value}}

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      RDS connections recovered for {{dbinstanceidentifier.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  evaluation_delay         = 900
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.rds_tags
}

resource "datadog_monitor" "rds_replica_lag" {
  name  = "[AWS] RDS Replica Lag"
  type  = "query alert"
  query = "avg(last_10m):avg:aws.rds.replica_lag{*} by {dbinstanceidentifier,application_team} > 60"

  monitor_thresholds {
    critical          = 60
    critical_recovery = 30
    warning           = 30
    warning_recovery  = 15
  }

  message = <<-EOF
    {{#is_alert}}
      RDS replica lag detected
      Instance: {{dbinstanceidentifier.name}}
      Application: {{application_team.name}}
      Lag: {{value}} seconds

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      RDS replica lag recovered for {{dbinstanceidentifier.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  evaluation_delay         = 900
  require_full_window      = false
  include_tags             = true
  priority                 = 2

  tags = var.rds_tags
}
