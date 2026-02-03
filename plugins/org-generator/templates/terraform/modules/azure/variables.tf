variable "alert_teams" {
  description = "Alert team configuration"
  type        = map(any)
  default = {
    notify = {
      default = []
    }
  }
}

variable "azure_tags" {
  description = "Tags for Azure monitors"
  type        = list(string)
  default = [
    "platform:azure",
    "managed_by:terraform"
  ]
}

variable "downtime_webhook" {
  description = "Webhook for auto-downtime on recovery"
  type        = string
  default     = ""
}
