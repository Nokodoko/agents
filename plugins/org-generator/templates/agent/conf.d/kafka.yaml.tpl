# Kafka Integration Template for {{CLIENT_NAME}}
# Generated: {{DATE}}
#
# Place this file in /etc/datadog-agent/conf.d/kafka.d/conf.yaml
#
# Prerequisites:
# 1. Enable JMX for Kafka brokers
# 2. Set KAFKA_JMX_OPTS environment variable

init_config:
  is_jmx: true
  collect_default_metrics: true

instances:
  - host: localhost
    port: 9999  # JMX port

    tags:
      - client:{{CLIENT_NAME}}
      - service:kafka

logs:
  - type: file
    path: /var/log/kafka/*.log
    source: kafka
    service: kafka
