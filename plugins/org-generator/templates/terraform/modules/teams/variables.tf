variable "name" {
  description = "Display name of the team"
  type        = string
}

variable "handle" {
  description = "Handle/identifier for the team (used in @team-handle mentions)"
  type        = string
}

variable "description" {
  description = "Description of the team"
  type        = string
  default     = ""
}
