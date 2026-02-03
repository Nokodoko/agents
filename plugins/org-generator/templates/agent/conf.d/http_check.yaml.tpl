# HTTP Check Configuration Template for {{CLIENT_NAME}}
# Generated: {{DATE}}
#
# Place this file in /etc/datadog-agent/conf.d/http_check.d/conf.yaml
#
# Update the URLs below to match your actual endpoints

init_config:

instances:
  # Example health check endpoint
  - name: app-health
    url: http://localhost:8080/health
    timeout: 10
    http_response_status_code: 200
    tags:
      - service:app
      - client:{{CLIENT_NAME}}

  # Add more endpoints as needed
  # - name: api-health
  #   url: https://api.example.com/health
  #   timeout: 10
  #   http_response_status_code: 200
  #   tls_verify: true
  #   tags:
  #     - service:api
  #     - client:{{CLIENT_NAME}}
