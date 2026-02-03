terraform {
  required_providers {
    datadog = {
      source = "Datadog/datadog"
    }
  }
}

# NOTE: Team handle is case sensitive in Datadog
resource "datadog_team" "team" {
  name        = var.name
  handle      = lower(var.handle)  # Ensure lowercase handle
  description = var.description
}

output "team_id" {
  description = "The ID of the created team"
  value       = datadog_team.team.id
}

output "team_handle" {
  description = "The handle of the created team"
  value       = datadog_team.team.handle
}
