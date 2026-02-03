# MySQL Integration Template for {{CLIENT_NAME}}
# Generated: {{DATE}}
#
# Place this file in /etc/datadog-agent/conf.d/mysql.d/conf.yaml
#
# Prerequisites:
# 1. Create Datadog user in MySQL:
#    CREATE USER 'datadog'@'localhost' IDENTIFIED BY '<PASSWORD>';
#    GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost';
#    GRANT PROCESS ON *.* TO 'datadog'@'localhost';
#    GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';

init_config:

instances:
  - host: localhost
    port: 3306
    username: datadog
    password: "<MYSQL_PASSWORD>"  # Use env var: ENC[datadog_user_password]

    options:
      replication: true
      galera_cluster: false
      extra_status_metrics: true
      extra_innodb_metrics: true
      schema_size_metrics: true
      disable_innodb_metrics: false

    tags:
      - client:{{CLIENT_NAME}}
      - service:mysql

logs:
  - type: file
    path: /var/log/mysql/error.log
    source: mysql
    service: mysql

  - type: file
    path: /var/log/mysql/mysql-slow.log
    source: mysql
    service: mysql
