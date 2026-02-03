#---------------------------------------------
# Notification Configuration
#---------------------------------------------
# Configure alert recipients and notification channels

#---------------------------------------------
# Alert Recipients by Platform
#---------------------------------------------

# Override in terraform.tfvars with actual team members
variable "alert_recipients_config" {
  description = "Alert recipients organized by platform and service"
  type        = any
  default = {
    # AWS Services
    aws = {
      default = {
        operators  = []
        developers = []
      }
      # Add service-specific recipients:
      # rds = {
      #   operators  = ["dba@example.com"]
      #   developers = ["backend@example.com"]
      # }
    }

    # GCP Services
    gcp = {
      default = {
        operators  = []
        developers = []
      }
    }

    # Azure Services
    azure = {
      default = {
        operators  = []
        developers = []
      }
    }

    # Kubernetes
    kubernetes = {
      default = {
        operators  = []
        developers = []
      }
    }
  }
}

#---------------------------------------------
# Notification Channels
#---------------------------------------------

variable "slack_channels" {
  description = "Slack channels for notifications"
  type        = map(string)
  default = {
    # alerts    = "#{{CLIENT_NAME}}-alerts"
    # incidents = "#{{CLIENT_NAME}}-incidents"
    # oncall    = "#{{CLIENT_NAME}}-oncall"
  }
}

variable "teams_channels" {
  description = "Microsoft Teams channels for notifications"
  type        = map(string)
  default = {
    # alerts = "@teams-{{CLIENT_NAME}}-alerts"
  }
}

variable "pagerduty_services" {
  description = "PagerDuty services for escalation"
  type        = map(string)
  default = {
    # oncall = "@pagerduty-{{CLIENT_NAME}}-oncall"
  }
}

#---------------------------------------------
# Alert Team Definitions
#---------------------------------------------

# Main notification configuration used by monitors
locals {
  alert_teams = {
    notify = {
      # Default recipients (all alerts)
      default = concat(
        [for email in lookup(lookup(var.alert_recipients_config, "aws", {}), "default", {operators = []}).operators : "@${email}"],
        lookup(var.slack_channels, "alerts", "") != "" ? ["@slack-${var.slack_channels["alerts"]}"] : []
      )

      # Direct Teams notifications (no ticket)
      teamsDirect_no_ticket = lookup(var.teams_channels, "alerts", "") != "" ? [var.teams_channels["alerts"]] : []

      # Teams channel for general notifications
      teams_channel = lookup(var.teams_channels, "alerts", "") != "" ? [var.teams_channels["alerts"]] : []

      # Ticket-creating notifications (ServiceNow, etc.)
      ticket_teams = []

      # Critical escalation (PagerDuty)
      critical_escalation = lookup(var.pagerduty_services, "oncall", "") != "" ? [var.pagerduty_services["oncall"]] : []
    }
  }

  # Downtime webhook for auto-resolving scheduled downtime
  downtime_webhook = ""  # Set to "@webhook-auto_downtime_webhook" if configured
}

#---------------------------------------------
# Escalation Policies
#---------------------------------------------

# Define escalation paths for different severity levels
locals {
  escalation = {
    critical = {
      initial_notify = local.alert_teams.notify.default
      escalate_to    = local.alert_teams.notify.critical_escalation
      renotify_interval = 30  # minutes
    }
    high = {
      initial_notify = local.alert_teams.notify.default
      escalate_to    = local.alert_teams.notify.teams_channel
      renotify_interval = 60
    }
    medium = {
      initial_notify = local.alert_teams.notify.teamsDirect_no_ticket
      escalate_to    = []
      renotify_interval = 120
    }
    low = {
      initial_notify = local.alert_teams.notify.teams_channel
      escalate_to    = []
      renotify_interval = 0  # no renotify
    }
  }
}

#---------------------------------------------
# Message Templates
#---------------------------------------------

locals {
  # Standard alert message template
  alert_message_template = <<-EOF
    {{#is_alert}}
      ALERT: {{monitor_name}}
      Application: {{application_team.name}}
      Environment: {{env.name}}
      Host: {{host.name}}
      Time: {{last_triggered_at_epoch}}

      ${join(",", local.alert_teams.notify.default)}
    {{/is_alert}}

    {{#is_warning}}
      WARNING: {{monitor_name}}
      Application: {{application_team.name}}

      ${join(",", local.alert_teams.notify.teamsDirect_no_ticket)}
    {{/is_warning}}

    {{#is_recovery}}
      RECOVERED: {{monitor_name}}
      Application: {{application_team.name}}
      Time: {{last_triggered_at_epoch}}

      ${local.downtime_webhook}
    {{/is_recovery}}
  EOF

  # Simple message template for low-priority alerts
  simple_message_template = <<-EOF
    {{#is_alert}}
      {{monitor_name}} triggered on {{host.name}}
      ${join(",", local.alert_teams.notify.teams_channel)}
    {{/is_alert}}

    {{#is_recovery}}
      {{monitor_name}} recovered
    {{/is_recovery}}
  EOF
}
