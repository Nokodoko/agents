terraform {
  required_providers {
    datadog = {
      source = "Datadog/datadog"
    }
  }
}

resource "datadog_api_key" "api_key" {
  name = "${var.key_name}_${var.env}"
}

output "api_key_id" {
  description = "The ID of the created API key"
  value       = datadog_api_key.api_key.id
}

output "api_key_value" {
  description = "The value of the created API key (sensitive)"
  value       = datadog_api_key.api_key.key
  sensitive   = true
}
