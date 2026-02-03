# Kubernetes Deployment Guide

## Prerequisites

- Kubernetes cluster (1.22+)
- `kubectl` configured
- Helm 3 installed

## Installation with Helm

### 1. Add Datadog Helm Repository

```bash
helm repo add datadog https://helm.datadoghq.com
helm repo update
```

### 2. Create Secrets

```bash
kubectl create namespace datadog

kubectl create secret generic datadog-secret \
  --from-literal api-key="YOUR_API_KEY" \
  --namespace datadog
```

### 3. Create values.yaml

```yaml
# values.yaml for {{CLIENT_NAME}}
datadog:
  site: {{SITE}}
  apiKeyExistingSecret: datadog-secret

  logs:
    enabled: true
    containerCollectAll: true

  apm:
    portEnabled: true
    enabled: {{APM_ENABLED}}

  processAgent:
    enabled: true
    processCollection: true

  networkMonitoring:
    enabled: true

  clusterChecks:
    enabled: true

  tags:
    - "client:{{CLIENT_NAME}}"
    - "env:production"
    - "managed_by:helm"

clusterAgent:
  enabled: true
  metricsProvider:
    enabled: true

kubeStateMetricsCore:
  enabled: true

agents:
  tolerations:
    - operator: Exists

  containers:
    agent:
      resources:
        requests:
          cpu: 200m
          memory: 256Mi
        limits:
          cpu: 200m
          memory: 256Mi
```

### 4. Install the Datadog Agent

```bash
helm install datadog-agent datadog/datadog \
  --namespace datadog \
  --values values.yaml
```

## Verify Installation

```bash
kubectl get pods -n datadog

kubectl exec -it $(kubectl get pods -n datadog -l app=datadog -o jsonpath='{.items[0].metadata.name}') -n datadog -- agent status
```

## Configuration Updates

```bash
helm upgrade datadog-agent datadog/datadog \
  --namespace datadog \
  --values values.yaml
```

## APM Instrumentation

For APM, applications need environment variables:

```yaml
env:
  - name: DD_AGENT_HOST
    valueFrom:
      fieldRef:
        fieldPath: status.hostIP
  - name: DD_TRACE_AGENT_PORT
    value: "8126"
```

## Troubleshooting

### Pods not starting

```bash
kubectl describe pod <pod-name> -n datadog
kubectl logs <pod-name> -n datadog -c agent
```

### No data in Datadog

1. Verify secret contains correct API key
2. Check network policies allow egress
3. Verify RBAC permissions

## Useful Commands

```bash
kubectl rollout restart daemonset datadog-agent -n datadog
kubectl logs -l app=datadog -n datadog --tail=100
kubectl exec -it <agent-pod> -n datadog -- agent check kubernetes
```
