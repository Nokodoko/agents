terraform {
  required_providers {
    datadog = {
      source = "Datadog/datadog"
    }
  }
}

resource "datadog_application_key" "app_key" {
  name = "${var.key_name}_${var.env}"
}

output "app_key_id" {
  description = "The ID of the created application key"
  value       = datadog_application_key.app_key.id
}

output "app_key_value" {
  description = "The value of the created application key (sensitive)"
  value       = datadog_application_key.app_key.key
  sensitive   = true
}
