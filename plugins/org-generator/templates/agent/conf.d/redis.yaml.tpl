# Redis Integration Template for {{CLIENT_NAME}}
# Generated: {{DATE}}
#
# Place this file in /etc/datadog-agent/conf.d/redisdb.d/conf.yaml

init_config:

instances:
  - host: localhost
    port: 6379
    # password: "<REDIS_PASSWORD>"  # Uncomment if auth required

    # Keys to monitor (patterns)
    # keys:
    #   - key_pattern

    # Slow log
    slowlog-max-len: 128

    tags:
      - client:{{CLIENT_NAME}}
      - service:redis

logs:
  - type: file
    path: /var/log/redis/redis-server.log
    source: redis
    service: redis
