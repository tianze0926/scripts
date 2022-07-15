from typing import Callable, Dict, TypedDict

Config = Dict[str, str]

class Location(TypedDict, total=False):
    port: int
    custom: Config

class Domain(Location, total=False):
    # / as default location, not requiring explicit declaration
    locations: Dict[str, Location] # locations other than /

SSL_CONFIG: Config = {
    'ssl_protocols': 'TLSv1 TLSv1.1 TLSv1.2 TLSv1.3', # Dropping SSLv3, ref: POODLE
    'ssl_prefer_server_ciphers': 'on',
    'ssl_ciphers': '"EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH+aRSA+RC4 EECDH EDH+aRSA RC4 !aNULL !eNULL !LOW !3DES !MD5 !EXP !PSK !SRP !DSS +RC4 RC4"',
    'ssl_session_cache':    'shared:SSL:10m',
    'ssl_session_timeout':  '10m',
}

SSL_CERTS: Dict[str, Config] = {
    'tianze.xyz': {
        'ssl_certificate': '/etc/letsencrypt/live/tianze.xyz/fullchain.pem',
        'ssl_certificate_key': '/etc/letsencrypt/live/tianze.xyz/privkey.pem'
    },
    'tianze.me': {
        'ssl_certificate': '/etc/letsencrypt/live/tianze.me/fullchain.pem',
        'ssl_certificate_key': '/etc/letsencrypt/live/tianze.me/privkey.pem'
    }
}

PORT = 1111

domain_qbittorrent: Callable[[int], Domain] = lambda port : {
    'port': port,
    # https://github.com/qbittorrent/qBittorrent/wiki/NGINX-Reverse-Proxy-for-Web-UI
    'custom': {
        'proxy_http_version':   '1.1',
        'proxy_set_header Host':             f'127.0.0.1:{port}',
        'proxy_set_header X-Forwarded-Host': '$http_host',
        'proxy_set_header X-Forwarded-For':  '$remote_addr',
        'proxy_cookie_path':    '/           "/; Secure"',
        'client_max_body_size': '100M',
    }
}

SUBDOMAINS: Dict[str, Domain] = {
    'status': {
        'port': 61208,
    },
    'file': {
        'port': 49149,
        'custom': {
            'client_max_body_size': '50G'
        }
    },
    'bt': domain_qbittorrent(8112),
    'bte': domain_qbittorrent(8113),
    'sub': {
        'port': 9305,
        'custom': {
            'proxy_set_header X-Real-IP': '$remote_addr',
            'proxy_set_header X-Forwarded-For': '$proxy_add_x_forwarded_for',
        }
    },
    'aria': {
        'custom': {
            'root': '/home/ubuntu/ariaNg'
        },
        'locations': {
            'jsonrpc': {
                'port': 6800
            }
        }
    },
    'rss': {
        'port': 18111,
        'custom': {
            'gzip': 'on',
            'proxy_redirect': 'off',
            'proxy_set_header  Host':                '$http_host',
            'proxy_set_header  X-Real-IP':           '$remote_addr',
            'proxy_set_header  X-Forwarded-Ssl':     'on',
            'proxy_set_header  X-Forwarded-For':     '$proxy_add_x_forwarded_for',
            'proxy_set_header  X-Forwarded-Proto':   '$scheme',
            'proxy_set_header  X-Frame-Options':     'SAMEORIGIN',
            'client_max_body_size':        '100m',
            'client_body_buffer_size':     '128k',
            'proxy_buffer_size':           '4k',
            'proxy_buffers':               '4 32k',
            'proxy_busy_buffers_size':     '64k',
            'proxy_temp_file_write_size':  '64k',
        }
    },
    'clash': {
        'port': 17890
    },
    'docker': {
        'custom': {
            'proxy_pass': 'https://localhost:9443',
        }
    },
}

def config_format(c: Config):
    return [
        f'{k} {v};' for k, v in c.items()
    ]

def location_format(l: Location):
    items = []
    if 'port' in l:
        items.append(f'proxy_pass http://localhost:{l["port"]};')
    if 'custom' in l:
        items.extend(config_format(l['custom']))
    return items

s = ''

NEWLINE = '\n'
for domain, cert_config in SSL_CERTS.items():
    ssl_config = {**SSL_CONFIG, **cert_config}
    for subdomain, sub_config in SUBDOMAINS.items():
        s += f'''server {{
    listen {PORT} ssl;
    server_name {subdomain}.{domain};
    error_page 497 301 =307 https://$host:$server_port$request_uri;
    
    {f'{NEWLINE}    '.join(config_format(ssl_config))}
    
    location / {{
        {f'{NEWLINE}        '.join(location_format(sub_config))}
    }}
    {NEWLINE.join([f"""location /{location} {{
        {f'{NEWLINE}        '.join(location_format(config))}
    }}""" for location, config in sub_config["locations"].items()])
    if "locations" in sub_config else ''}
}}

'''

with open('subdomain.conf', 'w') as f:
    f.write(s)
