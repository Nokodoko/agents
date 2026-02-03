# Questionnaire Skill

This skill helps users interactively fill out the client questionnaire with intelligent suggestions and validation.

## Detection Patterns

This skill activates when:

- User is viewing or editing a questionnaire.md file
- User asks for help filling out the questionnaire
- User mentions specific infrastructure they want to monitor
- User is unsure about questionnaire options

## Behavior

### Interactive Mode

When helping fill out a questionnaire, this skill:

1. **Reads current questionnaire state**
   - Identifies which sections are complete
   - Highlights required sections

2. **Asks clarifying questions**
   - Cloud providers in use
   - Infrastructure components
   - Monitoring requirements
   - Team structure

3. **Provides recommendations**
   - Suggests common configurations
   - Explains trade-offs
   - Recommends best practices

4. **Validates responses**
   - Ensures required fields are filled
   - Checks for conflicting selections
   - Warns about missing dependencies

### Section-by-Section Assistance

#### Organization Setup

**Questions asked**:
- Is this a new Datadog organization or existing?
- Will this be a child organization under a parent?
- What's the organization name?

**Recommendations**:
- Child organizations recommended for client isolation
- Parent org credentials needed for child org creation

#### Cloud Providers

**Questions asked**:
- Which cloud providers are in use?
- Are workloads spread across multiple providers?
- Is there a primary cloud provider?

**Recommendations**:
- Start with primary provider, add others later
- Multi-cloud requires additional integration setup

#### Infrastructure Components

**Questions asked**:
- What types of hosts? (Linux, Windows, Solaris)
- Container orchestration? (Kubernetes, ECS, Docker Swarm)
- Serverless functions? (Lambda, Cloud Functions)
- Databases? (RDS, Cloud SQL, Azure SQL)

**Recommendations**:
- Enable host monitoring first
- Kubernetes requires cluster agent deployment
- Database monitoring may need additional permissions

#### Services & Applications

**Questions asked**:
- Web servers? (nginx, Apache, IIS)
- Application servers? (Node, Java, Python)
- Message queues? (RabbitMQ, Kafka, SQS)
- Caching? (Redis, Memcached)

**Recommendations**:
- APM provides deeper service visibility
- Integration setup varies by service

#### Monitoring Requirements

**Questions asked**:
- APM for application tracing?
- RUM for frontend monitoring?
- Synthetic tests for uptime?
- Private locations for internal endpoints?

**Recommendations**:
- APM recommended for microservices
- RUM requires frontend code instrumentation
- Private locations need dedicated workers

#### Team Structure

**Questions asked**:
- How many admin users?
- How many standard users?
- Any read-only stakeholders?
- Role-based access requirements?

**Recommendations**:
- Limit admin access
- Create role-specific permissions
- Use teams for alert routing

#### Tagging Strategy

**Questions asked**:
- Environment naming? (dev, staging, prod)
- Team identifiers?
- Application names?
- Custom tags needed?

**Recommendations**:
- Consistent tagging is critical
- Use `managed_by:terraform` for all resources
- Environment tags enable filtering

## Example Interaction

**User**: "Help me fill out the questionnaire for acme-corp"

**Skill**:
```
Let me help you complete the questionnaire for acme-corp.

Section 1: Organization Setup
-----------------------------
Is this a new Datadog organization or will you use an existing one?

Options:
- [ ] Create new child organization (recommended for client isolation)
- [ ] Use existing organization
- [ ] Other

What would you like to select?
```

**User**: "New child organization"

**Skill**:
```
Great choice for client isolation.

Section 2: Cloud Providers
--------------------------
Which cloud providers does acme-corp use? (Select all that apply)

- [ ] AWS
- [ ] GCP
- [ ] Azure
- [ ] On-premise / VDC

Which ones should I select?
```

## Validation Rules

The skill validates:

| Rule | Validation |
|------|------------|
| Required sections | Organization, Cloud Providers, Team Structure |
| Dependency checks | Private locations requires Synthetics |
| Conflict detection | Cannot have both "no containers" and "Kubernetes" |
| Completeness | All selected sections must have sub-selections |

## Output

When complete, the skill:
1. Writes the filled questionnaire to disk
2. Provides a summary of selections
3. Instructs user to run `/org-generator:apply`
