variable "alert_teams" {
  description = "Alert team configuration"
  type        = map(any)
  default = {
    notify = {
      default = []
    }
  }
}

variable "gcp_tags" {
  description = "Tags for GCP monitors"
  type        = list(string)
  default = [
    "platform:gcp",
    "managed_by:terraform"
  ]
}

variable "downtime_webhook" {
  description = "Webhook for auto-downtime on recovery"
  type        = string
  default     = ""
}
