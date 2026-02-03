#---------------------------------------------
# API Key Outputs
#---------------------------------------------

output "api_key_ids" {
  description = "IDs of created API keys"
  value       = { for key, mod in module.api_keys : key => mod.api_key_id }
}

# Note: API key values are sensitive and output separately
# Use: terraform output -json api_key_values
output "api_key_values" {
  description = "Values of created API keys (sensitive)"
  value       = { for key, mod in module.api_keys : key => mod.api_key_value }
  sensitive   = true
}

#---------------------------------------------
# App Key Outputs
#---------------------------------------------

output "app_key_ids" {
  description = "IDs of created application keys"
  value       = { for key, mod in module.app_keys : key => mod.app_key_id }
}

#---------------------------------------------
# Role Outputs
#---------------------------------------------

output "role_ids" {
  description = "IDs of created roles"
  value = {
    admin          = module.roles.admin_role_id
    standard       = module.roles.standard_role_id
    read_only      = module.roles.read_only_role_id
    monitor_only   = module.roles.monitor_only_role_id
    dashboard_read = module.roles.dashboard_read_role_id
    dashboard_write = module.roles.dashboard_write_role_id
  }
}

#---------------------------------------------
# Team Outputs
#---------------------------------------------

output "team_ids" {
  description = "IDs of created teams"
  value       = { for key, mod in module.teams : key => mod.team_id }
}

#---------------------------------------------
# Private Location Outputs
#---------------------------------------------

# output "private_location_ids" {
#   description = "IDs of created private locations"
#   value       = { for key, mod in module.private_locations : key => mod.private_location_id }
# }

# output "private_location_configs" {
#   description = "Configuration files for private location workers"
#   value       = { for key, mod in module.private_locations : key => mod.config_file_path }
# }

#---------------------------------------------
# Summary Output
#---------------------------------------------

output "deployment_summary" {
  description = "Summary of deployed resources"
  value = {
    client_name = "{{CLIENT_NAME}}"
    backend     = "{{CLIENT_NAME}}-backend"
    api_keys    = length(module.api_keys)
    app_keys    = length(module.app_keys)
    teams       = length(module.teams)
    # Add counts for other resources as they're enabled
  }
}
