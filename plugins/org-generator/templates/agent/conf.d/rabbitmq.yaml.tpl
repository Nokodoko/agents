# RabbitMQ Integration Template for {{CLIENT_NAME}}
# Generated: {{DATE}}
#
# Place this file in /etc/datadog-agent/conf.d/rabbitmq.d/conf.yaml
#
# Prerequisites:
# 1. Enable RabbitMQ management plugin:
#    rabbitmq-plugins enable rabbitmq_management
# 2. Create monitoring user or use existing credentials

init_config:

instances:
  - rabbitmq_api_url: http://localhost:15672/api/
    username: guest
    password: guest  # Update with actual credentials

    # Queue filtering
    # queues:
    #   - queue_name_1
    #   - queue_name_2

    # Queue regex filtering
    # queues_regexes:
    #   - "prefix-.*"

    tags:
      - client:{{CLIENT_NAME}}
      - service:rabbitmq

logs:
  - type: file
    path: /var/log/rabbitmq/*.log
    source: rabbitmq
    service: rabbitmq
