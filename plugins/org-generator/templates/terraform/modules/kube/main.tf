terraform {
  required_providers {
    datadog = {
      source = "Datadog/datadog"
    }
  }
}

#---------------------------------------------
# Deployment Monitors
#---------------------------------------------

resource "datadog_monitor" "deployment_replica_down" {
  name    = "(k8s) {{deployment.name}} Deployment Replica is Down"
  type    = "query alert"
  query   = "avg(last_15m):avg:kubernetes_state.deployment.replicas_desired{*} by {cluster_name,deployment} - avg:kubernetes_state.deployment.replicas_ready{*} by {cluster_name,deployment} >= 2"

  monitor_thresholds {
    critical = 2
  }

  message = <<-EOF
    {{#is_alert}}
      More than one Deployment Replica's pods are down
      Cluster: {{cluster_name.name}}
      Deployment: {{deployment.name}}

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Deployment replicas recovered: {{deployment.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.kube_tags
}

#---------------------------------------------
# Pod Monitors
#---------------------------------------------

resource "datadog_monitor" "pods_restarting" {
  name    = "(k8s) {{pod_name.name}} Pods are Restarting"
  type    = "query alert"
  query   = "change(sum(last_5m),last_5m):exclude_null(avg:kubernetes.containers.restarts{*} by {cluster_name,kube_namespace,pod_name}) > 5"

  monitor_thresholds {
    critical = 5
    warning  = 3
  }

  message = <<-EOF
    {{#is_alert}}
      Pod is restarting multiple times
      Cluster: {{cluster_name.name}}
      Namespace: {{kube_namespace.name}}
      Pod: {{pod_name.name}}
      Restarts: {{value}}

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Pod stable: {{pod_name.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.kube_tags
}

resource "datadog_monitor" "pending_pods" {
  name    = "(k8s) {{cluster_name.name}} Pods Pending"
  type    = "metric alert"
  query   = "min(last_30m):sum:kubernetes_state.pod.status_phase{phase:running} by {cluster_name} - sum:kubernetes_state.pod.status_phase{phase:running} by {cluster_name} + sum:kubernetes_state.pod.status_phase{phase:pending} by {cluster_name}.fill(zero) >= 1"

  monitor_thresholds {
    critical = 1
  }

  message = <<-EOF
    {{#is_alert}}
      Pods have been pending for 30+ minutes
      Cluster: {{cluster_name.name}}
      Pending pods: {{value}}

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      No more pending pods on {{cluster_name.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = false
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.kube_tags
}

resource "datadog_monitor" "multi_pods_failing" {
  name    = "(k8s) {{kube_namespace.name}} Multiple Pods Failing"
  type    = "query alert"
  query   = "change(avg(last_5m),last_5m):sum:kubernetes_state.pod.status_phase{phase:failed} by {cluster_name,kube_namespace} > 10"

  monitor_thresholds {
    critical = 10
    warning  = 5
  }

  message = <<-EOF
    {{#is_alert}}
      Multiple pods failing in namespace
      Cluster: {{cluster_name.name}}
      Namespace: {{kube_namespace.name}}
      Failed pods: {{value}}

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Pod failures stabilized in {{kube_namespace.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 2

  tags = var.kube_tags
}

#---------------------------------------------
# DaemonSet Monitors
#---------------------------------------------

resource "datadog_monitor" "daemonset_pod_down" {
  name    = "(k8s) {{daemonset.name}} DaemonSet Pod is Down"
  type    = "query alert"
  query   = "max(last_15m):sum:kubernetes_state.daemonset.desired{*} by {cluster_name,kube_namespace,daemonset} - sum:kubernetes_state.daemonset.ready{*} by {cluster_name,kube_namespace,daemonset} >= 1"

  monitor_thresholds {
    critical = 1
  }

  message = <<-EOF
    {{#is_alert}}
      DaemonSet pod is down
      Cluster: {{cluster_name.name}}
      Namespace: {{kube_namespace.name}}
      DaemonSet: {{daemonset.name}}

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      DaemonSet pods recovered: {{daemonset.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.kube_tags
}

#---------------------------------------------
# StatefulSet Monitors
#---------------------------------------------

resource "datadog_monitor" "statefulset_replica_down" {
  name  = "(k8s) {{statefulset.name}} StatefulSet Replica is Down"
  type  = "query alert"
  query = "max(last_15m):sum:kubernetes_state.statefulset.replicas_desired{*} by {cluster_name,kube_namespace,statefulset} - sum:kubernetes_state.statefulset.replicas_ready{*} by {cluster_name,kube_namespace,statefulset} >= 2"

  monitor_thresholds {
    critical = 2
    warning  = 1
  }

  message = <<-EOF
    {{#is_alert}}
      StatefulSet replicas are down
      Cluster: {{cluster_name.name}}
      Namespace: {{kube_namespace.name}}
      StatefulSet: {{statefulset.name}}

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      StatefulSet replicas recovered: {{statefulset.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.kube_tags
}

#---------------------------------------------
# Node Monitors
#---------------------------------------------

resource "datadog_monitor" "node_unschedulable" {
  name    = "(k8s) {{cluster_name.name}} Node Unschedulable"
  type    = "query alert"
  query   = "max(last_15m):sum:kubernetes_state.node.status{status:schedulable} by {cluster_name} * 100 / sum:kubernetes_state.node.status{*} by {cluster_name} < 80"

  monitor_thresholds {
    critical = 80
    warning  = 90
  }

  message = <<-EOF
    {{#is_alert}}
      More than 20% of nodes are unschedulable
      Cluster: {{cluster_name.name}}
      Schedulable: {{value}}%

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Nodes schedulable again on {{cluster_name.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 2

  tags = var.kube_tags
}

#---------------------------------------------
# Image Monitors
#---------------------------------------------

resource "datadog_monitor" "imagepullbackoff" {
  name    = "(k8s) {{kube_namespace.name}} ImagePullBackOff"
  type    = "query alert"
  query   = "max(last_10m):max:kubernetes_state.container.status_report.count.waiting{reason:imagepullbackoff} by {kube_cluster_name,kube_namespace,pod_name} >= 1"

  monitor_thresholds {
    critical = 1
  }

  message = <<-EOF
    {{#is_alert}}
      ImagePullBackOff detected
      Cluster: {{kube_cluster_name.name}}
      Namespace: {{kube_namespace.name}}
      Pod: {{pod_name.name}}

      ${join(",", var.alert_teams["notify"]["default"])}
    {{/is_alert}}

    {{#is_recovery}}
      Image pull recovered: {{pod_name.name}}
      ${var.downtime_webhook}
    {{/is_recovery}}
  EOF

  notify_audit             = true
  notification_preset_name = "hide_handles"
  require_full_window      = false
  include_tags             = true
  priority                 = 3

  tags = var.kube_tags
}
