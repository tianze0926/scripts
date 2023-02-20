#!/bin/bash

for container in swag sync wireguard gitea qbittorrent qbittorrentee frps
do
	ufw-docker delete allow $container
	ufw-docker allow $container
done

