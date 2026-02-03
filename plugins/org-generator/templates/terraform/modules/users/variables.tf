variable "email" {
  description = "Email address of the user"
  type        = string
}

variable "name" {
  description = "Display name of the user"
  type        = string
}

variable "role_id" {
  description = "Role ID to assign to the user (optional)"
  type        = string
  default     = null
}

variable "send_invitation" {
  description = "Whether to send an invitation email to the user"
  type        = bool
  default     = true
}
