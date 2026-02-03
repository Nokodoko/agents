# Process Monitoring Template for {{CLIENT_NAME}}
# Generated: {{DATE}}
#
# Place this file in /etc/datadog-agent/conf.d/process.d/conf.yaml

init_config:

instances:
  {{#if NGINX_ENABLED}}
  - name: nginx
    search_string:
      - nginx
    exact_match: false
  {{/if}}

  {{#if APACHE_ENABLED}}
  - name: apache
    search_string:
      - apache2
      - httpd
    exact_match: false
  {{/if}}

  {{#if JAVA_ENABLED}}
  - name: java
    search_string:
      - java
    exact_match: false
  {{/if}}

  {{#if NODEJS_ENABLED}}
  - name: nodejs
    search_string:
      - node
    exact_match: false
  {{/if}}

  {{#if PYTHON_ENABLED}}
  - name: python
    search_string:
      - python
      - gunicorn
      - uwsgi
    exact_match: false
  {{/if}}

  {{#if REDIS_ENABLED}}
  - name: redis
    search_string:
      - redis-server
    exact_match: false
  {{/if}}

  {{#if RABBITMQ_ENABLED}}
  - name: rabbitmq
    search_string:
      - rabbitmq
      - beam.smp
    exact_match: false
  {{/if}}

  {{#if KAFKA_ENABLED}}
  - name: kafka
    search_string:
      - kafka
    exact_match: false
  {{/if}}

  # Always monitor datadog-agent
  - name: datadog-agent
    search_string:
      - datadog-agent
    exact_match: false
