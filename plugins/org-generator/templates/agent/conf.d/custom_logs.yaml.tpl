# Custom Log Collection Template for {{CLIENT_NAME}}
# Generated: {{DATE}}
#
# Place this file in /etc/datadog-agent/conf.d/custom_logs.d/conf.yaml
#
# This template is processed by lib/agent-generator.py to include
# log paths based on selected web servers and application servers.

logs:
  # nginx logs (if nginx selected)
  {{#if NGINX_ENABLED}}
  - type: file
    path: /var/log/nginx/access.log
    service: nginx
    source: nginx
    sourcecategory: http_web_access

  - type: file
    path: /var/log/nginx/error.log
    service: nginx
    source: nginx
    sourcecategory: http_web_error
  {{/if}}

  # Apache logs (if apache selected)
  {{#if APACHE_ENABLED}}
  - type: file
    path: /var/log/apache2/access.log
    service: apache
    source: apache
    sourcecategory: http_web_access

  - type: file
    path: /var/log/apache2/error.log
    service: apache
    source: apache
    sourcecategory: http_web_error
  {{/if}}

  # Java application logs (if Java selected)
  {{#if JAVA_ENABLED}}
  - type: file
    path: /var/log/app/*.log
    service: java-app
    source: java
  {{/if}}

  # Node.js application logs (if Node.js selected)
  {{#if NODEJS_ENABLED}}
  - type: file
    path: /var/log/node/*.log
    service: node-app
    source: nodejs
  {{/if}}

  # Python application logs (if Python selected)
  {{#if PYTHON_ENABLED}}
  - type: file
    path: /var/log/python/*.log
    service: python-app
    source: python
  {{/if}}

  # System logs (always included)
  - type: file
    path: /var/log/syslog
    service: system
    source: syslog

  - type: file
    path: /var/log/messages
    service: system
    source: syslog

  - type: file
    path: /var/log/auth.log
    service: system
    source: auth
