#---------------------------------------------
# Core Variables
#---------------------------------------------

variable "region" {
  description = "AWS region for provider and backend"
  type        = string
  default     = "us-east-1"
}

#---------------------------------------------
# Datadog Credentials
#---------------------------------------------

variable "{{CLIENT_NAME_UNDERSCORE}}_api_key" {
  description = "Datadog API key for {{CLIENT_NAME}}. Set via TF_VAR_{{CLIENT_NAME_UNDERSCORE}}_api_key"
  type        = string
  sensitive   = true
}

variable "{{CLIENT_NAME_UNDERSCORE}}_app_key" {
  description = "Datadog Application key for {{CLIENT_NAME}}. Set via TF_VAR_{{CLIENT_NAME_UNDERSCORE}}_app_key"
  type        = string
  sensitive   = true
}

variable "api_url" {
  description = "Datadog API URL (use https://api.ddog-gov.com for GovCloud)"
  type        = string
  default     = "https://api.datadoghq.com"
}

#---------------------------------------------
# Platform Configuration
#---------------------------------------------

variable "platform" {
  description = "Platform-wide configuration"
  type        = map(any)
  default = {
    # Uncomment platforms as needed
    # aws = {
    #   platform_name = "aws"
    # }
    # gcp = {
    #   platform_name = "gcp"
    # }
    # azure = {
    #   platform_name = "azure"
    # }
  }
}

#---------------------------------------------
# Alert Teams
#---------------------------------------------

variable "alert_recipients" {
  description = "Alert recipients by platform"
  type        = any
  default = {
    # Example structure:
    # aws = {
    #   service_name = {
    #     operators  = ["user@example.com"]
    #     developers = ["dev@example.com"]
    #   }
    # }
  }
}

variable "alert_teams" {
  description = "Alert team notification channels"
  type        = map(any)
  default = {
    notify = {
      default              = []
      teamsDirect          = []
      teamsDirect_no_ticket = []
      ticket_teams         = []
      teams_channel        = []
    }
  }
}

#---------------------------------------------
# Webhooks
#---------------------------------------------

variable "downtime_webhook" {
  description = "Webhook for auto-downtime on recovery"
  type        = string
  default     = ""
}

#---------------------------------------------
# Tags
#---------------------------------------------

variable "default_tags" {
  description = "Default tags applied to all resources"
  type        = list(string)
  default = [
    "managed_by:terraform",
    "client:{{CLIENT_NAME}}"
  ]
}

variable "aws_tags" {
  description = "Tags for AWS monitors"
  type        = list(string)
  default = [
    "platform:aws",
    "managed_by:terraform"
  ]
}

variable "gcp_tags" {
  description = "Tags for GCP monitors"
  type        = list(string)
  default = [
    "platform:gcp",
    "managed_by:terraform"
  ]
}

variable "azure_tags" {
  description = "Tags for Azure monitors"
  type        = list(string)
  default = [
    "platform:azure",
    "managed_by:terraform"
  ]
}

variable "kube_tags" {
  description = "Tags for Kubernetes monitors"
  type        = list(string)
  default = [
    "platform:kubernetes",
    "managed_by:terraform"
  ]
}

variable "rds_tags" {
  description = "Tags for RDS monitors"
  type        = list(string)
  default = [
    "service:rds",
    "platform:aws",
    "managed_by:terraform"
  ]
}

variable "ecs_tags" {
  description = "Tags for ECS monitors"
  type        = list(string)
  default = [
    "service:ecs",
    "platform:aws",
    "managed_by:terraform"
  ]
}

#---------------------------------------------
# API Keys
#---------------------------------------------

variable "api_keys" {
  description = "API keys to create"
  type        = map(any)
  default = {
    # Example:
    # main = {
    #   env = "production"
    # }
  }
}

#---------------------------------------------
# App Keys
#---------------------------------------------

variable "app_keys" {
  description = "Application keys to create"
  type        = map(any)
  default = {
    # Example:
    # main = {
    #   env = "production"
    # }
  }
}

#---------------------------------------------
# Users
#---------------------------------------------

variable "users" {
  description = "Users to create"
  type        = map(any)
  default = {
    # Example:
    # admin = {
    #   email = "admin@example.com"
    #   name  = "Admin User"
    #   role  = "admin"
    # }
  }
}

#---------------------------------------------
# Teams
#---------------------------------------------

variable "teams" {
  description = "Teams to create"
  type        = map(any)
  default = {
    # Example:
    # platform = {
    #   name        = "Platform Team"
    #   description = "Platform engineering team"
    # }
  }
}

#---------------------------------------------
# Synthetics Configuration
#---------------------------------------------

variable "synthetic_tests" {
  description = "Synthetic tests to create"
  type        = map(any)
  default = {
    # Example:
    # main_site = {
    #   url       = "https://example.com"
    #   tag_name  = "main-site"
    #   location  = "aws:us-east-1"
    #   platform  = "aws"
    # }
  }
}

variable "private_locations" {
  description = "Private locations to create"
  type        = map(any)
  default = {
    # Example:
    # internal = {
    #   env = "production"
    # }
  }
}
