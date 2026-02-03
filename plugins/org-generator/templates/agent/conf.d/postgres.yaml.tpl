# PostgreSQL Integration Template for {{CLIENT_NAME}}
# Generated: {{DATE}}
#
# Place this file in /etc/datadog-agent/conf.d/postgres.d/conf.yaml
#
# Prerequisites:
# 1. Create Datadog user in PostgreSQL:
#    CREATE USER datadog WITH PASSWORD '<PASSWORD>';
#    GRANT pg_monitor TO datadog;
#    GRANT SELECT ON pg_stat_database TO datadog;

init_config:

instances:
  - host: localhost
    port: 5432
    username: datadog
    password: "<POSTGRES_PASSWORD>"  # Use env var
    dbname: postgres

    # Query metrics
    query_metrics:
      enabled: true

    # Relations to collect
    relations:
      - relation_regex: .*

    tags:
      - client:{{CLIENT_NAME}}
      - service:postgres

logs:
  - type: file
    path: /var/log/postgresql/*.log
    source: postgresql
    service: postgres
