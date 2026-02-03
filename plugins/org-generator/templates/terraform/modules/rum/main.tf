terraform {
  required_providers {
    datadog = {
      source = "Datadog/datadog"
    }
  }
}

#---------------------------------------------
# RUM Application Definition
#---------------------------------------------

# Note: RUM applications are typically created via UI or API
# This module defines monitors for RUM data

#---------------------------------------------
# RUM Monitors
#---------------------------------------------

resource "datadog_monitor" "rum_high_error_rate" {
  name  = "[RUM] {{application.id.name}} High Error Rate"
  type  = "query alert"
  query = "sum(last_10m):sum:rum.error.count{*} by {application.id,env}.as_count() / sum:rum.view.count{*} by {application.id,env}.as_count() * 100 > 5"

  monitor_thresholds {
    critical          = 5
    critical_recovery = 2
    warning           = 2
    warning_recovery  = 1
  }

  message = <<-EOF
    {{#is_alert}}
      High frontend error rate detected
      Application: {{application.id.name}}
      Environment: {{env.name}}
      Error rate: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Frontend error rate recovered for {{application.id.name}}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 2

  tags = var.rum_tags
}

resource "datadog_monitor" "rum_high_lcp" {
  name  = "[RUM] {{application.id.name}} High LCP (Largest Contentful Paint)"
  type  = "query alert"
  query = "avg(last_10m):avg:rum.view.largest_contentful_paint{*} by {application.id,env} > 4000000000"

  monitor_thresholds {
    critical          = 4000000000  # 4 seconds in nanoseconds
    critical_recovery = 2500000000
    warning           = 2500000000
    warning_recovery  = 2000000000
  }

  message = <<-EOF
    {{#is_alert}}
      High Largest Contentful Paint (LCP) detected
      Application: {{application.id.name}}
      Environment: {{env.name}}
      LCP: {{value}}ns

      This affects Core Web Vitals and SEO.

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      LCP recovered for {{application.id.name}}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.rum_tags
}

resource "datadog_monitor" "rum_high_fid" {
  name  = "[RUM] {{application.id.name}} High FID (First Input Delay)"
  type  = "query alert"
  query = "avg(last_10m):avg:rum.view.first_input_delay{*} by {application.id,env} > 300000000"

  monitor_thresholds {
    critical          = 300000000  # 300ms in nanoseconds
    critical_recovery = 100000000
    warning           = 100000000
    warning_recovery  = 50000000
  }

  message = <<-EOF
    {{#is_alert}}
      High First Input Delay (FID) detected
      Application: {{application.id.name}}
      Environment: {{env.name}}
      FID: {{value}}ns

      This affects user interactivity.

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      FID recovered for {{application.id.name}}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.rum_tags
}

resource "datadog_monitor" "rum_high_cls" {
  name  = "[RUM] {{application.id.name}} High CLS (Cumulative Layout Shift)"
  type  = "query alert"
  query = "avg(last_10m):avg:rum.view.cumulative_layout_shift{*} by {application.id,env} > 0.25"

  monitor_thresholds {
    critical          = 0.25
    critical_recovery = 0.1
    warning           = 0.1
    warning_recovery  = 0.05
  }

  message = <<-EOF
    {{#is_alert}}
      High Cumulative Layout Shift (CLS) detected
      Application: {{application.id.name}}
      Environment: {{env.name}}
      CLS: {{value}}

      This affects visual stability.

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      CLS recovered for {{application.id.name}}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.rum_tags
}

resource "datadog_monitor" "rum_resource_load_time" {
  name  = "[RUM] {{application.id.name}} High Resource Load Time"
  type  = "query alert"
  query = "avg(last_10m):avg:rum.resource.load_time{*} by {application.id,resource_type,env} > 3000000000"

  monitor_thresholds {
    critical          = 3000000000  # 3 seconds
    critical_recovery = 2000000000
    warning           = 2000000000
    warning_recovery  = 1000000000
  }

  message = <<-EOF
    {{#is_alert}}
      High resource load time detected
      Application: {{application.id.name}}
      Resource Type: {{resource_type.name}}
      Environment: {{env.name}}
      Load time: {{value}}ns

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Resource load time recovered for {{application.id.name}}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 4

  tags = var.rum_tags
}
