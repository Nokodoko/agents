variable "alert_teams" {
  description = "Alert team configuration"
  type        = map(any)
  default = {
    notify = {
      default = []
    }
  }
}

variable "kube_tags" {
  description = "Tags for Kubernetes monitors"
  type        = list(string)
  default = [
    "platform:kubernetes",
    "managed_by:terraform"
  ]
}

variable "downtime_webhook" {
  description = "Webhook for auto-downtime on recovery"
  type        = string
  default     = ""
}
