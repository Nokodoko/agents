terraform {
  required_providers {
    datadog = {
      source = "Datadog/datadog"
    }
  }
}

#---------------------------------------------
# HTTP API Test
#---------------------------------------------

resource "datadog_synthetics_test" "http_test" {
  type      = "api"
  locations = [var.location]

  request_definition {
    method = "GET"
    url    = var.url
  }

  assertion {
    operator = "is"
    type     = "statusCode"
    target   = "200"
  }

  assertion {
    operator = "lessThan"
    type     = "responseTime"
    target   = var.response_time_threshold
  }

  options_list {
    tick_every       = var.tick_every
    follow_redirects = true
    min_failure_duration = 0
    min_location_failed  = 1
  }

  status  = "live"
  name    = "${title(var.site_name)} HTTP Synthetic Test"
  message = <<-EOF
    {{#is_alert}}
      ${title(var.site_name)} has failed the HTTP check
      URL: ${var.url}
      Location: ${var.location}

      ${join(",", var.alert_recipients)}
    {{/is_alert}}

    {{#is_recovery}}
      ${title(var.site_name)} HTTP check recovered
    {{/is_recovery}}
  EOF

  tags = concat(var.default_tags, [
    "application_team:${var.tag_name}",
    "test_type:api",
    "platform:${var.platform}",
    "env:production",
    "active:true"
  ])
}

#---------------------------------------------
# SSL Certificate Test
#---------------------------------------------

resource "datadog_synthetics_test" "ssl_test" {
  count = var.enable_ssl_check ? 1 : 0

  name      = "${title(var.site_name)} SSL Certificate Check"
  type      = "api"
  subtype   = "ssl"
  status    = "live"
  locations = [var.location]

  request_definition {
    host = replace(replace(var.url, "https://", ""), "/.*", "")
    port = 443
  }

  assertion {
    type     = "certificate"
    operator = "isInMoreThan"
    target   = 30  # Days until expiry
  }

  options_list {
    tick_every         = 900  # 15 minutes
    accept_self_signed = false
  }

  message = <<-EOF
    {{#is_alert}}
      SSL certificate expiring soon for ${title(var.site_name)}
      Host: ${replace(replace(var.url, "https://", ""), "/.*", "")}
      Days until expiry: {{value}}

      ${join(",", var.alert_recipients)}
    {{/is_alert}}

    {{#is_recovery}}
      SSL certificate is valid for ${title(var.site_name)}
    {{/is_recovery}}
  EOF

  tags = concat(var.default_tags, [
    "application_team:${var.tag_name}",
    "test_type:ssl",
    "platform:${var.platform}",
    "env:production"
  ])
}

#---------------------------------------------
# Outputs
#---------------------------------------------

output "http_test_id" {
  description = "ID of the HTTP synthetic test"
  value       = datadog_synthetics_test.http_test.id
}

output "ssl_test_id" {
  description = "ID of the SSL synthetic test"
  value       = var.enable_ssl_check ? datadog_synthetics_test.ssl_test[0].id : null
}
