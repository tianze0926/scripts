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

## Access host service

> `host.docker.internal` is not supported since its DNS resolving is achieved using `/etc/hosts` instead of Docker's DNS server, and Nginx is not looking up `/etc/hosts` for `proxy_pass` directive.

- Configure `ufw` to allow traffic from docker

    ```
    ufw allow from 192.168.32.0/20 comment 'docker'
    ```

    The subnet is of the bridge network to which SWAG's container links.

- Nginx `proxy_pass`: should be `docker0`'s IP