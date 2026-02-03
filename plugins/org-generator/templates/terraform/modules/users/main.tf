terraform {
  required_providers {
    datadog = {
      source = "Datadog/datadog"
    }
  }
}

resource "datadog_user" "user" {
  email = var.email
  name  = var.name

  # Assign roles if provided (roles is a list of role IDs)
  roles = var.role_id != null ? [var.role_id] : []

  # Send user invitation email
  send_user_invitation = var.send_invitation
}

output "user_id" {
  description = "The ID of the created user"
  value       = datadog_user.user.id
}

output "user_verified" {
  description = "Whether the user has verified their account"
  value       = datadog_user.user.verified
}
