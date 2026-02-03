variable "key_name" {
  description = "Name prefix for the application key"
  type        = string
}

variable "env" {
  description = "Environment (e.g., production, staging)"
  type        = string
  default     = "production"
}
