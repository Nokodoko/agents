#---------------------------------------------
# Tag Definitions
#---------------------------------------------
# This file contains tag variable definitions and locals for consistent tagging

locals {
  # Common tags applied to all resources
  common_tags = [
    "managed_by:terraform",
    "client:{{CLIENT_NAME}}"
  ]

  # Environment-specific tag prefix
  env_prefix = "env:"

  # Platform-specific tags
  platform_tags = {
    aws   = concat(local.common_tags, ["platform:aws"])
    gcp   = concat(local.common_tags, ["platform:gcp"])
    azure = concat(local.common_tags, ["platform:azure"])
    kube  = concat(local.common_tags, ["platform:kubernetes"])
  }

  # Service-specific tags
  service_tags = {
    rds = concat(local.platform_tags["aws"], ["service:rds"])
    ecs = concat(local.platform_tags["aws"], ["service:ecs"])
    alb = concat(local.platform_tags["aws"], ["service:alb"])
    lambda = concat(local.platform_tags["aws"], ["service:lambda"])
    cloudsql = concat(local.platform_tags["gcp"], ["service:cloudsql"])
    gke = concat(local.platform_tags["gcp"], ["service:gke"])
    sql_database = concat(local.platform_tags["azure"], ["service:sql"])
    aks = concat(local.platform_tags["azure"], ["service:aks"])
  }

  # Monitor priority levels
  priority_critical = 1
  priority_high     = 2
  priority_medium   = 3
  priority_low      = 4
  priority_info     = 5
}

#---------------------------------------------
# Tag Helper Variables
#---------------------------------------------

# These can be overridden in terraform.tfvars or via environment

variable "environment" {
  description = "Environment name (e.g., production, staging, development)"
  type        = string
  default     = "production"
}

variable "application_team" {
  description = "Name of the application team"
  type        = string
  default     = "{{CLIENT_NAME}}"
}

#---------------------------------------------
# Dynamic Tag Generation
#---------------------------------------------

locals {
  # Generate environment tag
  env_tag = "${local.env_prefix}${var.environment}"

  # Generate application team tag
  app_team_tag = "application_team:${var.application_team}"

  # Full tag set for monitors
  monitor_tags = concat(local.common_tags, [local.env_tag, local.app_team_tag])
}
