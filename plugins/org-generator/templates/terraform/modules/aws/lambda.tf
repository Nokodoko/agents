#---------------------------------------------
# Lambda Monitors
#---------------------------------------------

resource "datadog_monitor" "lambda_errors" {
  name  = "[AWS] Lambda Errors"
  type  = "query alert"
  query = "sum(last_10m):sum:aws.lambda.errors{*} by {functionname,application_team}.as_count() > 5"

  monitor_thresholds {
    critical          = 5
    critical_recovery = 0
    warning           = 2
    warning_recovery  = 0
  }

  message = <<-EOF
    {{#is_alert}}
      Lambda function errors detected
      Function: {{functionname.name}}
      Application: {{application_team.name}}
      Error count: {{value}}

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Lambda errors recovered for {{functionname.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  evaluation_delay         = 900
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.aws_tags
}

resource "datadog_monitor" "lambda_throttles" {
  name  = "[AWS] Lambda Throttles"
  type  = "query alert"
  query = "sum(last_10m):sum:aws.lambda.throttles{*} by {functionname,application_team}.as_count() > 10"

  monitor_thresholds {
    critical          = 10
    critical_recovery = 0
    warning           = 5
    warning_recovery  = 0
  }

  message = <<-EOF
    {{#is_alert}}
      Lambda function being throttled
      Function: {{functionname.name}}
      Application: {{application_team.name}}
      Throttle count: {{value}}

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Lambda throttling recovered for {{functionname.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  evaluation_delay         = 900
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.aws_tags
}

resource "datadog_monitor" "lambda_duration" {
  name  = "[AWS] Lambda High Duration"
  type  = "query alert"
  query = "avg(last_10m):avg:aws.lambda.duration.average{*} by {functionname,application_team} > 10000"

  monitor_thresholds {
    critical          = 10000  # 10 seconds
    critical_recovery = 5000
    warning           = 5000   # 5 seconds
    warning_recovery  = 3000
  }

  message = <<-EOF
    {{#is_alert}}
      Lambda function high execution duration
      Function: {{functionname.name}}
      Application: {{application_team.name}}
      Duration: {{value}}ms

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Lambda duration recovered for {{functionname.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  evaluation_delay         = 900
  require_full_window      = false
  include_tags             = true
  priority                 = 4

  tags = var.aws_tags
}

resource "datadog_monitor" "lambda_concurrent_executions" {
  name  = "[AWS] Lambda High Concurrent Executions"
  type  = "query alert"
  query = "avg(last_10m):avg:aws.lambda.concurrent_executions{*} by {functionname,application_team} > 500"

  monitor_thresholds {
    critical          = 500
    critical_recovery = 400
    warning           = 400
    warning_recovery  = 300
  }

  message = <<-EOF
    {{#is_alert}}
      Lambda high concurrent executions
      Function: {{functionname.name}}
      Application: {{application_team.name}}
      Concurrent executions: {{value}}

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Lambda concurrent executions recovered for {{functionname.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  evaluation_delay         = 900
  require_full_window      = false
  include_tags             = true
  priority                 = 4

  tags = var.aws_tags
}
