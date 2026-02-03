terraform {
  required_providers {
    datadog = {
      source = "Datadog/datadog"
    }
  }
}

#---------------------------------------------
# EC2 Monitors
#---------------------------------------------

resource "datadog_monitor" "ec2_status_check_failed" {
  name  = "[AWS] EC2 Status Check Failed"
  type  = "query alert"
  query = "sum(last_5m):sum:aws.ec2.status_check_failed{*} by {host,name} > 0"

  monitor_thresholds {
    critical          = 0
    critical_recovery = 0
  }

  message = <<-EOF
    {{#is_alert}}
      EC2 status check failed
      Instance: {{name.name}}
      Host: {{host.name}}

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      EC2 status check recovered
      Instance: {{name.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 2

  tags = var.aws_tags
}

resource "datadog_monitor" "ec2_high_cpu" {
  name  = "[AWS] EC2 High CPU Utilization"
  type  = "query alert"
  query = "avg(last_10m):avg:aws.ec2.cpuutilization{*} by {name,host} > 90"

  monitor_thresholds {
    critical          = 90
    critical_recovery = 85
    warning           = 80
    warning_recovery  = 75
  }

  message = <<-EOF
    {{#is_alert}}
      High CPU utilization on EC2 instance
      Instance: {{name.name}}
      CPU: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      CPU utilization recovered on {{name.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.aws_tags
}

#---------------------------------------------
# ALB/ELB Monitors
#---------------------------------------------

resource "datadog_monitor" "alb_5xx_errors" {
  name  = "[AWS] ALB 5XX Errors"
  type  = "query alert"
  query = "sum(last_1h):(sum:aws.applicationelb.httpcode_elb_5xx{*} by {application_team}.as_count() / (sum:aws.applicationelb.httpcode_elb_5xx{*} by {application_team}.as_count() + sum:aws.applicationelb.httpcode_target_2xx{*} by {application_team}.as_count())) * 100 > 20"

  monitor_thresholds {
    critical          = 20
    critical_recovery = 5
  }

  message = <<-EOF
    {{#is_alert}}
      5XX errors detected on ALB
      Application: {{application_team.name}}
      Error rate: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      5XX errors recovered for {{application_team.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  evaluation_delay         = 900
  require_full_window      = true
  include_tags             = true
  priority                 = 3

  tags = var.aws_tags
}

resource "datadog_monitor" "alb_high_response_time" {
  name  = "[AWS] ALB High Response Time"
  type  = "query alert"
  query = "avg(last_10m):avg:aws.applicationelb.target_response_time.average{*} by {application_team,loadbalancer} > 5"

  monitor_thresholds {
    critical          = 5
    critical_recovery = 3
    warning           = 3
    warning_recovery  = 2
  }

  message = <<-EOF
    {{#is_alert}}
      High response time on ALB
      Application: {{application_team.name}}
      Load Balancer: {{loadbalancer.name}}
      Response time: {{value}}s

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Response time recovered for {{application_team.name}}
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

resource "datadog_monitor" "alb_no_healthy_hosts" {
  name  = "[AWS] ALB No Healthy Hosts"
  type  = "query alert"
  query = "sum(last_5m):sum:aws.applicationelb.healthy_host_count{*} by {application_team,loadbalancer} < 1"

  monitor_thresholds {
    critical          = 1
    critical_recovery = 1.5
  }

  message = <<-EOF
    {{#is_alert}}
      No healthy hosts behind ALB!
      Application: {{application_team.name}}
      Load Balancer: {{loadbalancer.name}}

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Healthy hosts restored for {{application_team.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  evaluation_delay         = 900
  require_full_window      = false
  include_tags             = true
  priority                 = 1

  tags = var.aws_tags
}
