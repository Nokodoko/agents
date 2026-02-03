#---------------------------------------------
# Core Modules - Always Included
#---------------------------------------------

# API Keys
module "api_keys" {
  source   = "./modules/api_keys/"
  for_each = var.api_keys
  key_name = each.key
  env      = each.value.env
}

# Application Keys
module "app_keys" {
  source   = "./modules/app_keys/"
  for_each = var.app_keys
  key_name = each.key
  env      = each.value.env
}

# Roles
module "roles" {
  source = "./modules/roles/"
}

# Teams
module "teams" {
  source   = "./modules/teams/"
  for_each = var.teams
  name     = each.value.name
  handle   = each.key
  description = lookup(each.value, "description", "Team ${each.value.name}")
}

# Users
module "users" {
  source   = "./modules/users/"
  for_each = var.users
  email    = each.value.email
  name     = each.value.name
  role_id  = lookup(each.value, "role_id", null)
}

# Generic Monitors (CPU, Memory, Disk, Network)
module "generic_monitors" {
  source       = "./modules/generic/"
  alert_teams  = var.alert_teams
  default_tags = var.default_tags
}

#---------------------------------------------
# Cloud Provider Modules - Conditional
#---------------------------------------------

# AWS Monitors
# Uncomment if AWS is selected in questionnaire
# module "aws_monitors" {
#   source           = "./modules/aws/"
#   alert_teams      = var.alert_teams
#   aws_tags         = var.aws_tags
#   rds_tags         = var.rds_tags
#   ecs_tags         = var.ecs_tags
#   downtime_webhook = var.downtime_webhook
# }

# GCP Monitors
# Uncomment if GCP is selected in questionnaire
# module "gcp_monitors" {
#   source           = "./modules/gcp/"
#   alert_teams      = var.alert_teams
#   gcp_tags         = var.gcp_tags
#   downtime_webhook = var.downtime_webhook
# }

# Azure Monitors
# Uncomment if Azure is selected in questionnaire
# module "azure_monitors" {
#   source           = "./modules/azure/"
#   alert_teams      = var.alert_teams
#   azure_tags       = var.azure_tags
#   downtime_webhook = var.downtime_webhook
# }

#---------------------------------------------
# Infrastructure Modules - Conditional
#---------------------------------------------

# Kubernetes Monitors
# Uncomment if containers/Kubernetes selected
# module "kube_monitors" {
#   source           = "./modules/kube/"
#   alert_teams      = var.alert_teams
#   kube_tags        = var.kube_tags
#   downtime_webhook = var.downtime_webhook
# }

# Synthetic Tests
# Uncomment if synthetics selected
# module "synthetics" {
#   source    = "./modules/synthetics/"
#   for_each  = var.synthetic_tests
#   site_name = each.key
#   url       = each.value.url
#   tag_name  = each.value.tag_name
#   location  = each.value.location
#   platform  = each.value.platform
# }

# Private Locations
# Uncomment if private locations selected
# module "private_locations" {
#   source       = "./modules/private_locations/"
#   for_each     = var.private_locations
#   service_name = each.key
#   env          = each.value.env
#   api_key      = var.{{CLIENT_NAME_UNDERSCORE}}_api_key
# }

#---------------------------------------------
# APM & RUM Modules - Conditional
#---------------------------------------------

# APM Configuration
# Uncomment if APM selected
# module "apm" {
#   source      = "./modules/apm/"
#   alert_teams = var.alert_teams
# }

# RUM Configuration
# Uncomment if RUM selected
# module "rum" {
#   source      = "./modules/rum/"
#   alert_teams = var.alert_teams
# }
