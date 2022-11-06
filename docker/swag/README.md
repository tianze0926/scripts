# SWAG

This handles the web portal as well as automatic certificate.

## Make Nginx Ignore Upstream When Unreachable

https://serverfault.com/questions/700894/make-nginx-ignore-site-config-when-its-upstream-cannot-be-reached

```
server {
    server_name clash.*;
    include /config/nginx/ssl.conf;
    include /config/nginx/authelia-server.conf;
    location / {
        include /config/nginx/proxy.conf;
        include /config/nginx/authelia-location.conf;
        set $target http://clash:8080;
        proxy_pass $target;
    }
}
```

so that the upstream domain will be evaluated at run time instead of startup time.