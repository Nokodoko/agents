# Datadog Infrastructure Questionnaire

**Client Name**: {{CLIENT_NAME}}
**Date**: {{DATE}}
**Engagement Type**: [ ] POC / [ ] Production

---

## 1. Organization Setup

How should the Datadog organization be configured?

- [ ] Create new child organization (recommended for client isolation)
- [ ] Use existing organization
- [ ] Other: _______________

**Organization Name** (if new): _______________

**Parent Organization** (if child org): _______________

---

## 2. Cloud Providers

Which cloud providers does your infrastructure use? (Select all that apply)

- [ ] AWS
- [ ] GCP (Google Cloud Platform)
- [ ] Azure
- [ ] On-premise / Private Data Center
- [ ] Other: _______________

**Primary Cloud Provider** (if multiple): _______________

### AWS Details (if selected)
- [ ] Single AWS Account
- [ ] Multiple AWS Accounts
- Number of accounts: ___

**AWS Regions in use**: _______________

### GCP Details (if selected)
- [ ] Single GCP Project
- [ ] Multiple GCP Projects
- Number of projects: ___

**GCP Regions in use**: _______________

### Azure Details (if selected)
- [ ] Single Azure Subscription
- [ ] Multiple Azure Subscriptions
- Number of subscriptions: ___

**Azure Regions in use**: _______________

---

## 3. Infrastructure Components

### 3.1 Hosts

What types of hosts are in your environment?

- [ ] Linux servers
  - [ ] RHEL/CentOS
  - [ ] Ubuntu/Debian
  - [ ] Amazon Linux
  - [ ] Other Linux: _______________
- [ ] Windows servers
  - [ ] Windows Server 2016+
  - [ ] Windows Server 2012
- [ ] Solaris
- [ ] Other: _______________

**Approximate number of hosts**: _______________

### 3.2 Containers

Do you use container orchestration?

- [ ] Yes
- [ ] No (skip to section 3.3)

**Container Platform** (select all that apply):
- [ ] Kubernetes (self-managed)
- [ ] Amazon EKS
- [ ] Google GKE
- [ ] Azure AKS
- [ ] Amazon ECS
- [ ] Docker Swarm
- [ ] Other: _______________

**Number of Kubernetes clusters** (if applicable): ___

**Approximate number of pods/containers**: _______________

### 3.3 Serverless

Do you use serverless functions?

- [ ] Yes
- [ ] No (skip to section 3.4)

**Serverless Platform** (select all that apply):
- [ ] AWS Lambda
- [ ] Google Cloud Functions
- [ ] Azure Functions
- [ ] AWS Fargate
- [ ] Other: _______________

**Approximate number of functions**: _______________

### 3.4 Databases

Which databases are in your environment?

**AWS Databases**:
- [ ] Amazon RDS
  - [ ] MySQL
  - [ ] PostgreSQL
  - [ ] SQL Server
  - [ ] Oracle
  - [ ] MariaDB
- [ ] Amazon Aurora
- [ ] Amazon DynamoDB
- [ ] Amazon ElastiCache (Redis/Memcached)
- [ ] Amazon DocumentDB

**GCP Databases**:
- [ ] Cloud SQL
  - [ ] MySQL
  - [ ] PostgreSQL
  - [ ] SQL Server
- [ ] Cloud Spanner
- [ ] Firestore
- [ ] Memorystore (Redis)

**Azure Databases**:
- [ ] Azure SQL Database
- [ ] Azure Database for MySQL
- [ ] Azure Database for PostgreSQL
- [ ] Azure Cosmos DB
- [ ] Azure Cache for Redis

**Self-Managed Databases**:
- [ ] MySQL
- [ ] PostgreSQL
- [ ] MongoDB
- [ ] Redis
- [ ] Elasticsearch
- [ ] Other: _______________

---

## 4. Services & Applications

### 4.1 Web Servers

- [ ] nginx
- [ ] Apache HTTP Server
- [ ] IIS
- [ ] Other: _______________

### 4.2 Application Servers / Runtimes

- [ ] Node.js
- [ ] Java (Spring, Tomcat, etc.)
- [ ] Python (Django, Flask, etc.)
- [ ] .NET / .NET Core
- [ ] Go
- [ ] Ruby (Rails, etc.)
- [ ] PHP
- [ ] Other: _______________

### 4.3 Message Queues

- [ ] Amazon SQS
- [ ] Amazon SNS
- [ ] RabbitMQ
- [ ] Apache Kafka
- [ ] Azure Service Bus
- [ ] Google Pub/Sub
- [ ] None
- [ ] Other: _______________

### 4.4 Caching

- [ ] Redis
- [ ] Memcached
- [ ] Varnish
- [ ] CloudFront
- [ ] None
- [ ] Other: _______________

---

## 5. Monitoring Requirements

### 5.1 APM (Application Performance Monitoring)

Do you need application tracing?

- [ ] Yes
- [ ] No

**Languages/Frameworks to instrument** (if yes):
- [ ] Java
- [ ] Python
- [ ] Node.js
- [ ] .NET
- [ ] Go
- [ ] Ruby
- [ ] PHP
- [ ] Other: _______________

### 5.2 RUM (Real User Monitoring)

Do you need frontend/browser monitoring?

- [ ] Yes
- [ ] No

**Frontend Frameworks** (if yes):
- [ ] React
- [ ] Angular
- [ ] Vue.js
- [ ] Plain JavaScript
- [ ] Mobile (iOS/Android)
- [ ] Other: _______________

### 5.3 Synthetic Testing

Do you need synthetic uptime monitoring?

- [ ] Yes
- [ ] No

**Test Types** (if yes):
- [ ] HTTP/API tests
- [ ] Browser tests
- [ ] SSL certificate monitoring
- [ ] DNS checks

**Number of endpoints to monitor**: _______________

### 5.4 Private Locations

Do you need to monitor internal/private endpoints?

- [ ] Yes (requires private location workers)
- [ ] No

**Private Location Details** (if yes):
- Deployment platform: [ ] Kubernetes / [ ] Docker / [ ] VM
- Number of locations needed: ___

---

## 6. Team Structure & Access

### 6.1 User Counts

| Role | Count | Names/Emails |
|------|-------|--------------|
| Admin | ___ | _______________ |
| Standard User | ___ | _______________ |
| Read-Only User | ___ | _______________ |

### 6.2 Role Requirements

Which standard roles do you need?

- [x] Admin (full access) - **Required**
- [x] Standard User (create/edit monitors, dashboards) - **Required**
- [x] Read-Only User (view only) - **Required**
- [ ] Monitor-Only User (manage monitors only)
- [ ] Dashboard-Read-Only (view dashboards only)
- [ ] Dashboard-Write User (create/edit dashboards only)
- [ ] Custom roles: _______________

### 6.3 Teams

List the teams that should receive alerts:

| Team Name | Alert Channel | Members |
|-----------|--------------|---------|
| _______________ | _______________ | _______________ |
| _______________ | _______________ | _______________ |
| _______________ | _______________ | _______________ |

---

## 7. Tagging Strategy

### 7.1 Environment Tags

What environment names do you use?

- [ ] production / staging / development
- [ ] prod / stage / dev
- [ ] prd / stg / dev
- [ ] Custom: _______________

### 7.2 Standard Tags

Which tags should be applied to all resources?

| Tag Key | Description | Example Values |
|---------|-------------|----------------|
| `env` | Environment | prod, staging, dev |
| `application_team` | Owning team | _______________ |
| `platform` | Cloud platform | aws, gcp, azure |
| `managed_by` | Management tool | terraform |
| _______________ | _______________ | _______________ |
| _______________ | _______________ | _______________ |

### 7.3 Service Tags

| Service/Application | Tag Value |
|--------------------|-----------|
| _______________ | _______________ |
| _______________ | _______________ |
| _______________ | _______________ |

---

## 8. Integrations

### 8.1 Alert Integrations

How should alerts be delivered?

- [ ] Email
- [ ] Slack
  - Workspace: _______________
  - Channel(s): _______________
- [ ] Microsoft Teams
  - Team: _______________
  - Channel(s): _______________
- [ ] PagerDuty
  - Service: _______________
- [ ] ServiceNow
  - Instance: _______________
- [ ] Webhook
  - URL: _______________
- [ ] Other: _______________

### 8.2 SSO/Identity Provider

- [ ] SAML
  - Provider: _______________
- [ ] Google Workspace
- [ ] Azure AD / Entra ID
- [ ] Okta
- [ ] None (Datadog native auth)

---

## 9. Additional Requirements

### 9.1 Compliance

- [ ] HIPAA
- [ ] PCI-DSS
- [ ] SOC 2
- [ ] FedRAMP
- [ ] Other: _______________

### 9.2 Data Residency

- [ ] US (default)
- [ ] EU
- [ ] US Government (GovCloud)
- [ ] Other: _______________

### 9.3 Custom Requirements

Please describe any additional monitoring requirements:

```
_______________________________________________________________
_______________________________________________________________
_______________________________________________________________
```

---

## Summary

**Selected Infrastructure**:
- Cloud Providers: _______________
- Containers: [ ] Yes / [ ] No
- Serverless: [ ] Yes / [ ] No
- Databases: _______________

**Selected Monitoring**:
- APM: [ ] Yes / [ ] No
- RUM: [ ] Yes / [ ] No
- Synthetics: [ ] Yes / [ ] No
- Private Locations: [ ] Yes / [ ] No

**Next Steps**:
1. Review and complete all sections above
2. Save this file
3. Run: `/org-generator:apply {{CLIENT_NAME}}`

---

*Questionnaire generated by org-generator plugin*
