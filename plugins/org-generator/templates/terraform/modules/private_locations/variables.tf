variable "service_name" {
  description = "Name of the private location"
  type        = string
}

variable "env" {
  description = "Environment (e.g., production, staging)"
  type        = string
  default     = "production"
}

variable "description" {
  description = "Description of the private location"
  type        = string
  default     = ""
}

variable "api_key" {
  description = "Datadog API key for worker configuration"
  type        = string
  sensitive   = true
}

variable "datadog_site" {
  description = "Datadog site URL"
  type        = string
  default     = "https://api.datadoghq.com"
}

variable "config_output_path" {
  description = "Path to output the worker configuration file"
  type        = string
  default     = ""
}

variable "generate_config_file" {
  description = "Whether to generate the worker configuration file"
  type        = bool
  default     = true
}

variable "default_tags" {
  description = "Default tags for the private location"
  type        = list(string)
  default = [
    "managed_by:terraform"
  ]
}
