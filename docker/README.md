## Enabling IPv6

Create IPv6 bridge:

```shell
docker network create apps --ipv6 --subnet fd00:dead:beef::/48
```

Enable IPv6 at `/etc/docker/daemon.json`:

```json
{
  "ipv6": true,
  "fixed-cidr-v6": "2001:db8:1::/64",
  "experimental": true,
  "ip6tables": true
}
```

## UFW

https://github.com/chaifeng/ufw-docker
