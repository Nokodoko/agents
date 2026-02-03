variable "alert_teams" {
  description = "Alert team configuration"
  type        = map(any)
  default = {
    notify = {
      default = []
    }
  }
}

variable "apm_tags" {
  description = "Tags for APM monitors"
  type        = list(string)
  default = [
    "service:apm",
    "managed_by:terraform"
  ]
}
