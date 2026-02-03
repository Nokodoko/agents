# Roles module doesn't require variables as it creates standard roles
# Add custom role configuration here if needed

variable "custom_roles" {
  description = "Additional custom roles to create"
  type = map(object({
    name        = string
    permissions = list(string)
  }))
  default = {}
}
