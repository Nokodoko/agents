# nginx Integration Template for {{CLIENT_NAME}}
# Generated: {{DATE}}
#
# Place this file in /etc/datadog-agent/conf.d/nginx.d/conf.yaml
#
# Prerequisites:
# 1. Enable nginx stub_status module
# 2. Add to nginx.conf:
#    location /nginx_status {
#        stub_status on;
#        allow 127.0.0.1;
#        deny all;
#    }

init_config:

instances:
  - nginx_status_url: http://localhost/nginx_status
    tags:
      - client:{{CLIENT_NAME}}

logs:
  - type: file
    path: /var/log/nginx/access.log
    service: nginx
    source: nginx

  - type: file
    path: /var/log/nginx/error.log
    service: nginx
    source: nginx
