variable "alert_teams" {
  description = "Alert team configuration"
  type        = map(any)
  default = {
    notify = {
      default = []
    }
  }
}

variable "default_tags" {
  description = "Default tags for all monitors"
  type        = list(string)
  default = [
    "managed_by:terraform"
  ]
}

variable "downtime_webhook" {
  description = "Webhook for auto-downtime on recovery"
  type        = string
  default     = ""
}
