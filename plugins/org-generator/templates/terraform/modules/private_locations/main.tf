terraform {
  required_providers {
    datadog = {
      source = "Datadog/datadog"
    }
    local = {
      source = "hashicorp/local"
    }
  }
}

locals {
  config_filepath = var.config_output_path != "" ? var.config_output_path : "${path.root}/private_locations"
}

#---------------------------------------------
# Private Location Resource
#---------------------------------------------

resource "datadog_synthetics_private_location" "private_location" {
  name        = var.service_name
  description = var.description != "" ? var.description : "Private location for ${var.service_name}"

  tags = concat(var.default_tags, [
    "service:${var.service_name}",
    "env:${var.env}"
  ])
}

#---------------------------------------------
# Worker Configuration File
#---------------------------------------------

resource "local_file" "private_location_config" {
  count = var.generate_config_file ? 1 : 0

  filename = "${local.config_filepath}/worker-config-${datadog_synthetics_private_location.private_location.name}-${datadog_synthetics_private_location.private_location.id}.json"

  content = jsonencode({
    datadogApiKey   = var.api_key
    id              = datadog_synthetics_private_location.private_location.id
    site            = var.datadog_site
    accessKey       = datadog_synthetics_private_location.private_location.config[0].access_key
    secretAccessKey = datadog_synthetics_private_location.private_location.config[0].secret_access_key
    privateKey      = datadog_synthetics_private_location.private_location.config[0].private_key
    publicKey       = datadog_synthetics_private_location.private_location.config[0].public_key
    fingerprint     = datadog_synthetics_private_location.private_location.config[0].fingerprint
    name            = datadog_synthetics_private_location.private_location.name
    description     = datadog_synthetics_private_location.private_location.description
    tags            = datadog_synthetics_private_location.private_location.tags
  })

  depends_on = [datadog_synthetics_private_location.private_location]

  # Mark as sensitive since it contains keys
  file_permission = "0600"
}

#---------------------------------------------
# Outputs
#---------------------------------------------

output "private_location_id" {
  description = "ID of the private location"
  value       = datadog_synthetics_private_location.private_location.id
}

output "private_location_name" {
  description = "Name of the private location"
  value       = datadog_synthetics_private_location.private_location.name
}

output "config_file_path" {
  description = "Path to the generated config file"
  value       = var.generate_config_file ? local_file.private_location_config[0].filename : null
}

# Sensitive outputs for programmatic access
output "access_key" {
  description = "Access key for the private location"
  value       = datadog_synthetics_private_location.private_location.config[0].access_key
  sensitive   = true
}

output "secret_access_key" {
  description = "Secret access key for the private location"
  value       = datadog_synthetics_private_location.private_location.config[0].secret_access_key
  sensitive   = true
}
