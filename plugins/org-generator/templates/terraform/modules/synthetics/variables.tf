variable "site_name" {
  description = "Name of the site being tested"
  type        = string
}

variable "url" {
  description = "URL to test"
  type        = string
}

variable "tag_name" {
  description = "Application team tag"
  type        = string
}

variable "location" {
  description = "Synthetic test location"
  type        = string
  default     = "aws:us-east-1"
}

variable "platform" {
  description = "Platform tag (aws, gcp, azure)"
  type        = string
  default     = "aws"
}

variable "tick_every" {
  description = "How often to run the test in seconds"
  type        = number
  default     = 300  # 5 minutes
}

variable "response_time_threshold" {
  description = "Response time threshold in ms"
  type        = number
  default     = 5000  # 5 seconds
}

variable "enable_ssl_check" {
  description = "Whether to enable SSL certificate checking"
  type        = bool
  default     = true
}

variable "alert_recipients" {
  description = "List of alert recipients"
  type        = list(string)
  default     = []
}

variable "default_tags" {
  description = "Default tags for all tests"
  type        = list(string)
  default = [
    "managed_by:terraform"
  ]
}
