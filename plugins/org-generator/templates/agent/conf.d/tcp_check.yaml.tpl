# TCP Check Configuration Template for {{CLIENT_NAME}}
# Generated: {{DATE}}
#
# Place this file in /etc/datadog-agent/conf.d/tcp_check.d/conf.yaml

init_config:

instances:
  {{#if MYSQL_ENABLED}}
  # MySQL
  - name: mysql
    host: localhost
    port: 3306
    timeout: 5
    tags:
      - service:mysql
  {{/if}}

  {{#if POSTGRES_ENABLED}}
  # PostgreSQL
  - name: postgres
    host: localhost
    port: 5432
    timeout: 5
    tags:
      - service:postgres
  {{/if}}

  {{#if MONGODB_ENABLED}}
  # MongoDB
  - name: mongodb
    host: localhost
    port: 27017
    timeout: 5
    tags:
      - service:mongodb
  {{/if}}

  {{#if REDIS_ENABLED}}
  # Redis
  - name: redis
    host: localhost
    port: 6379
    timeout: 5
    tags:
      - service:redis
  {{/if}}

  {{#if RABBITMQ_ENABLED}}
  # RabbitMQ
  - name: rabbitmq
    host: localhost
    port: 5672
    timeout: 5
    tags:
      - service:rabbitmq

  - name: rabbitmq-management
    host: localhost
    port: 15672
    timeout: 5
    tags:
      - service:rabbitmq
  {{/if}}

  {{#if KAFKA_ENABLED}}
  # Kafka
  - name: kafka
    host: localhost
    port: 9092
    timeout: 5
    tags:
      - service:kafka
  {{/if}}

  {{#if ELASTICSEARCH_ENABLED}}
  # Elasticsearch
  - name: elasticsearch
    host: localhost
    port: 9200
    timeout: 5
    tags:
      - service:elasticsearch
  {{/if}}
