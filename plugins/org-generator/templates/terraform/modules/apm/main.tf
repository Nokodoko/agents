terraform {
  required_providers {
    datadog = {
      source = "Datadog/datadog"
    }
  }
}

#---------------------------------------------
# APM Service Monitors
#---------------------------------------------

resource "datadog_monitor" "apm_high_error_rate" {
  name  = "[APM] {{service.name}} High Error Rate"
  type  = "query alert"
  query = "sum(last_10m):sum:trace.http.request.errors{*} by {service,env}.as_count() / sum:trace.http.request.hits{*} by {service,env}.as_count() * 100 > 5"

  monitor_thresholds {
    critical          = 5
    critical_recovery = 2
    warning           = 2
    warning_recovery  = 1
  }

  message = <<-EOF
    {{#is_alert}}
      High error rate detected for service
      Service: {{service.name}}
      Environment: {{env.name}}
      Error rate: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Error rate recovered for {{service.name}}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 2

  tags = var.apm_tags
}

resource "datadog_monitor" "apm_high_latency" {
  name  = "[APM] {{service.name}} High Latency (p99)"
  type  = "query alert"
  query = "avg(last_10m):avg:trace.http.request.duration.by.service.99p{*} by {service,env} > 5000000000"

  monitor_thresholds {
    critical          = 5000000000  # 5 seconds in nanoseconds
    critical_recovery = 3000000000
    warning           = 3000000000
    warning_recovery  = 2000000000
  }

  message = <<-EOF
    {{#is_alert}}
      High p99 latency detected for service
      Service: {{service.name}}
      Environment: {{env.name}}
      Latency: {{value}}ns

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Latency recovered for {{service.name}}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.apm_tags
}

resource "datadog_monitor" "apm_throughput_anomaly" {
  name  = "[APM] {{service.name}} Throughput Anomaly"
  type  = "query alert"
  query = "avg(last_1h):anomalies(sum:trace.http.request.hits{*} by {service,env}.as_count(), 'basic', 2, direction='both') >= 1"

  monitor_thresholds {
    critical = 1
  }

  message = <<-EOF
    {{#is_alert}}
      Throughput anomaly detected for service
      Service: {{service.name}}
      Environment: {{env.name}}
      This may indicate unusual traffic patterns.

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Throughput returned to normal for {{service.name}}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 4

  tags = var.apm_tags
}
