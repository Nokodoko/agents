variable "alert_teams" {
  description = "Alert team configuration"
  type        = map(any)
  default = {
    notify = {
      default = []
    }
  }
}

variable "aws_tags" {
  description = "Tags for AWS monitors"
  type        = list(string)
  default = [
    "platform:aws",
    "managed_by:terraform"
  ]
}

variable "rds_tags" {
  description = "Tags for RDS monitors"
  type        = list(string)
  default = [
    "service:rds",
    "platform:aws",
    "managed_by:terraform"
  ]
}

variable "ecs_tags" {
  description = "Tags for ECS monitors"
  type        = list(string)
  default = [
    "service:ecs",
    "platform:aws",
    "managed_by:terraform"
  ]
}

variable "downtime_webhook" {
  description = "Webhook for auto-downtime on recovery"
  type        = string
  default     = ""
}
