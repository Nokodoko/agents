terraform {
  required_providers {
    datadog = {
      source  = "Datadog/datadog"
      version = ">= 3.86.0"
    }
    aws = {
      source = "hashicorp/aws"
    }
  }
  backend "s3" {
    bucket  = "{{CLIENT_NAME}}-backend"
    key     = "{{CLIENT_NAME}}-backend/backend"
    region  = "us-east-1"
    encrypt = true
  }
}

provider "aws" {
  region = var.region
}

provider "datadog" {
  api_key = var.{{CLIENT_NAME_UNDERSCORE}}_api_key
  app_key = var.{{CLIENT_NAME_UNDERSCORE}}_app_key
  api_url = var.api_url
}
