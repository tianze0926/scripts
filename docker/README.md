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

Install `ufw-docker` script:

```sh
sudo wget -O /usr/local/bin/ufw-docker https://github.com/chaifeng/ufw-docker/raw/master/ufw-docker
sudo chmod +x /usr/local/bin/ufw-docker
```

Then:

```sh
ufw-docker install
```

The allow rules must be set on every docker startup to correctly match each container's IP address. Run `sudo systemctl edit docker` to add an override file:

```conf
[Service]
ExecStartPost=/home/ubuntu/scripts/docker/ufw.sh
```
