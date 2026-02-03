terraform {
  required_providers {
    datadog = {
      source = "Datadog/datadog"
    }
  }
}

#---------------------------------------------
# CPU Monitors
#---------------------------------------------

resource "datadog_monitor" "high_cpu_utilization" {
  name  = "[Generic] High CPU Utilization"
  type  = "query alert"
  query = "avg(last_10m):avg:system.cpu.user{*} by {host} > 90"

  monitor_thresholds {
    critical          = 90
    critical_recovery = 85
    warning           = 80
    warning_recovery  = 75
  }

  message = <<-EOF
    {{#is_alert}}
      High CPU utilization detected on {{host.name}}
      Current value: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_warning}}
      CPU utilization is elevated on {{host.name}}
      Current value: {{value}}%
    {{/is_warning}}

    {{#is_recovery}}
      CPU utilization has returned to normal on {{host.name}}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.default_tags
}

#---------------------------------------------
# Memory Monitors
#---------------------------------------------

resource "datadog_monitor" "high_memory_utilization" {
  name  = "[Generic] High Memory Utilization"
  type  = "query alert"
  query = "avg(last_10m):avg:system.mem.pct_usable{*} by {host} < 10"

  monitor_thresholds {
    critical          = 10
    critical_recovery = 15
    warning           = 20
    warning_recovery  = 25
  }

  message = <<-EOF
    {{#is_alert}}
      Low available memory on {{host.name}}
      Available memory: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_warning}}
      Memory is getting low on {{host.name}}
      Available memory: {{value}}%
    {{/is_warning}}

    {{#is_recovery}}
      Memory utilization has returned to normal on {{host.name}}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.default_tags
}

#---------------------------------------------
# Disk Monitors
#---------------------------------------------

resource "datadog_monitor" "disk_space_low" {
  name  = "[Generic] Disk Space Low"
  type  = "query alert"
  query = "avg(last_10m):avg:system.disk.free{*} by {host,device} / avg:system.disk.total{*} by {host,device} * 100 < 10"

  monitor_thresholds {
    critical          = 10
    critical_recovery = 15
    warning           = 20
    warning_recovery  = 25
  }

  message = <<-EOF
    {{#is_alert}}
      Disk space critically low on {{host.name}} ({{device.name}})
      Free space: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_warning}}
      Disk space getting low on {{host.name}} ({{device.name}})
      Free space: {{value}}%
    {{/is_warning}}

    {{#is_recovery}}
      Disk space has returned to normal on {{host.name}} ({{device.name}})
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 2

  tags = var.default_tags
}

resource "datadog_monitor" "disk_iops_high" {
  name  = "[Generic] High Disk I/O"
  type  = "query alert"
  query = "avg(last_10m):avg:system.io.util{*} by {host,device} > 90"

  monitor_thresholds {
    critical          = 90
    critical_recovery = 80
    warning           = 80
    warning_recovery  = 70
  }

  message = <<-EOF
    {{#is_alert}}
      High disk I/O utilization on {{host.name}} ({{device.name}})
      I/O utilization: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Disk I/O has returned to normal on {{host.name}} ({{device.name}})
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.default_tags
}

#---------------------------------------------
# Network Monitors
#---------------------------------------------

resource "datadog_monitor" "network_errors" {
  name  = "[Generic] Network Errors Detected"
  type  = "query alert"
  query = "sum(last_10m):sum:system.net.errors{*} by {host,interface} > 100"

  monitor_thresholds {
    critical          = 100
    critical_recovery = 50
    warning           = 50
    warning_recovery  = 25
  }

  message = <<-EOF
    {{#is_alert}}
      Network errors detected on {{host.name}} ({{interface.name}})
      Error count: {{value}}

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Network errors have returned to normal on {{host.name}} ({{interface.name}})
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.default_tags
}

resource "datadog_monitor" "network_packet_loss" {
  name  = "[Generic] Network Packet Loss"
  type  = "query alert"
  query = "avg(last_10m):avg:system.net.packets_in.error{*} by {host} / avg:system.net.packets_in.count{*} by {host} * 100 > 5"

  monitor_thresholds {
    critical          = 5
    critical_recovery = 2
    warning           = 2
    warning_recovery  = 1
  }

  message = <<-EOF
    {{#is_alert}}
      Packet loss detected on {{host.name}}
      Packet loss rate: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Packet loss has returned to normal on {{host.name}}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.default_tags
}

#---------------------------------------------
# Host Availability
#---------------------------------------------

resource "datadog_monitor" "host_not_reporting" {
  name  = "[Generic] Host Not Reporting"
  type  = "service check"
  query = "\"datadog.agent.up\".over(\"*\").by(\"host\").last(2).count_by_status()"

  message = <<-EOF
    {{#is_alert}}
      Host {{host.name}} is not reporting to Datadog
      Last seen: {{last_triggered_at}}

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Host {{host.name}} is reporting again
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  renotify_interval        = 60
  include_tags             = true
  priority                 = 2

  tags = var.default_tags
}
