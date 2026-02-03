terraform {
  required_providers {
    datadog = {
      source = "Datadog/datadog"
    }
  }
}

# Fetch available permissions
data "datadog_permissions" "all" {}

#---------------------------------------------
# Admin Role
#---------------------------------------------
# Full access to all Datadog features
resource "datadog_role" "admin" {
  name = "Admin"

  # Admin gets all permissions - typically use built-in Datadog Admin Role
  # This custom role allows for specific permission customization
  permission {
    id = data.datadog_permissions.all.permissions.admin
  }
}

#---------------------------------------------
# Standard User Role
#---------------------------------------------
# Create/edit monitors, dashboards; no org settings
resource "datadog_role" "standard" {
  name = "Standard User"

  # Monitors
  permission {
    id = data.datadog_permissions.all.permissions.monitors_read
  }
  permission {
    id = data.datadog_permissions.all.permissions.monitors_write
  }
  permission {
    id = data.datadog_permissions.all.permissions.monitors_downtime
  }

  # Dashboards
  permission {
    id = data.datadog_permissions.all.permissions.dashboards_read
  }
  permission {
    id = data.datadog_permissions.all.permissions.dashboards_write
  }
  permission {
    id = data.datadog_permissions.all.permissions.dashboards_public_share
  }

  # Metrics
  permission {
    id = data.datadog_permissions.all.permissions.metrics_metadata_write
  }

  # Events
  permission {
    id = data.datadog_permissions.all.permissions.events_read
  }

  # Notebooks
  permission {
    id = data.datadog_permissions.all.permissions.notebooks_read
  }
  permission {
    id = data.datadog_permissions.all.permissions.notebooks_write
  }
}

#---------------------------------------------
# Read-Only User Role
#---------------------------------------------
# View-only access to all resources
resource "datadog_role" "read_only" {
  name = "Read-Only User"

  # Monitors (read only)
  permission {
    id = data.datadog_permissions.all.permissions.monitors_read
  }

  # Dashboards (read only)
  permission {
    id = data.datadog_permissions.all.permissions.dashboards_read
  }

  # Events (read only)
  permission {
    id = data.datadog_permissions.all.permissions.events_read
  }

  # Logs (read only)
  permission {
    id = data.datadog_permissions.all.permissions.logs_read_data
  }
  permission {
    id = data.datadog_permissions.all.permissions.logs_read_index_data
  }

  # APM (read only)
  permission {
    id = data.datadog_permissions.all.permissions.apm_read
  }

  # Notebooks (read only)
  permission {
    id = data.datadog_permissions.all.permissions.notebooks_read
  }
}

#---------------------------------------------
# Monitor-Only User Role
#---------------------------------------------
# Manage monitors only
resource "datadog_role" "monitor_only" {
  name = "Monitor-Only User"

  permission {
    id = data.datadog_permissions.all.permissions.monitors_read
  }
  permission {
    id = data.datadog_permissions.all.permissions.monitors_write
  }
  permission {
    id = data.datadog_permissions.all.permissions.monitors_downtime
  }

  # Need dashboard read to view monitor status
  permission {
    id = data.datadog_permissions.all.permissions.dashboards_read
  }
}

#---------------------------------------------
# Dashboard-Read-Only Role
#---------------------------------------------
# View dashboards only
resource "datadog_role" "dashboard_read" {
  name = "Dashboard-Read-Only"

  permission {
    id = data.datadog_permissions.all.permissions.dashboards_read
  }
}

#---------------------------------------------
# Dashboard-Write User Role
#---------------------------------------------
# Create/edit dashboards
resource "datadog_role" "dashboard_write" {
  name = "Dashboard-Write User"

  permission {
    id = data.datadog_permissions.all.permissions.dashboards_read
  }
  permission {
    id = data.datadog_permissions.all.permissions.dashboards_write
  }
  permission {
    id = data.datadog_permissions.all.permissions.dashboards_public_share
  }

  # Need metrics read to build dashboards
  permission {
    id = data.datadog_permissions.all.permissions.metrics_metadata_write
  }
}

#---------------------------------------------
# Outputs
#---------------------------------------------

output "admin_role_id" {
  description = "ID of the Admin role"
  value       = datadog_role.admin.id
}

output "standard_role_id" {
  description = "ID of the Standard User role"
  value       = datadog_role.standard.id
}

output "read_only_role_id" {
  description = "ID of the Read-Only User role"
  value       = datadog_role.read_only.id
}

output "monitor_only_role_id" {
  description = "ID of the Monitor-Only User role"
  value       = datadog_role.monitor_only.id
}

output "dashboard_read_role_id" {
  description = "ID of the Dashboard-Read-Only role"
  value       = datadog_role.dashboard_read.id
}

output "dashboard_write_role_id" {
  description = "ID of the Dashboard-Write User role"
  value       = datadog_role.dashboard_write.id
}
