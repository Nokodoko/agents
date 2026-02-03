variable "alert_teams" {
  description = "Alert team configuration"
  type        = map(any)
  default = {
    notify = {
      default = []
    }
  }
}

variable "rum_tags" {
  description = "Tags for RUM monitors"
  type        = list(string)
  default = [
    "service:rum",
    "managed_by:terraform"
  ]
}
