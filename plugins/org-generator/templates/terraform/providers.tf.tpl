# Provider version constraints
# This file is separate from backend.tf to allow for environment-specific overrides

terraform {
  required_version = ">= 1.0.0"

  required_providers {
    datadog = {
      source  = "Datadog/datadog"
      version = ">= 3.86.0"
    }
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
    local = {
      source  = "hashicorp/local"
      version = ">= 2.0"
    }
  }
}

# Provider configurations are in backend.tf
