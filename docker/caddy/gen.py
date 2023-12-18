import json

from sensitive import config
class dotdict(dict): # https://stackoverflow.com/a/23689767
    __getattr__ = dict.get
sensitive_config = dotdict(config)

class Caddy:
  def __init__(s):
    s.port = 1111
    s.domain = 'tianze.me'
    s.auth_name = 'auth'
    s.auth_dial = 'authelia:9091'
    s.routes = [
      s.r(s.auth_name, s.auth_dial, False),
      s.r('status', 'glances:61208'),
      s.r('media', 'jellyfin:8096', False),
      s.r('bt', 'qbittorrent:8080'),
      s.r('bte', 'qbittorrentee:8080'),
      s.r('bitwarden', 'bitwarden:80', False),
      s.r('file', 'filebrowser:80'),
      s.r('swap', 'filebrowser-swap:80', False),
      s.r('sub', 'qzyq-water-sub:8080'),
      s.h('aria', [{
        'handler': 'subroute',
        'routes': [
          {
            'match': [{'path': ['/jsonrpc']}],
            'handle': [s.reverse_handler('aria:6800')],
          },
          {
            'handle': [
              s.auth_handler(),
              s.reverse_handler('aria-ng:6880'),
            ],
          },
        ],
      }]),
      s.r('frp', 'frps:80'),
      s.r('sync', 'sync:8384'),
      s.r('ntfy', 'ntfy:80', auth=False),
      s.r('mail', 'roundcube:80', auth=False),
      s.r('cloud', 'owncloud:9200', False),
      s.h('fs', [{
        'handler': 'subroute',
        'routes': [
          {
            'match': [{'path': [f'/{token}/*']}],
            'handle': [
              {
                'handler': 'rewrite',
                'strip_path_prefix': f'/{token}',
              },
              {
                'handler': 'file_server',
                'root': root,
                'browse': {},
              },
            ],
          }
          for token, root in sensitive_config.file_server_access
        ],
      }]),
      {
        'handle': [{
          'abort': True,
          'handler': 'static_response',
        }],
        'terminal': True,
      }
    ]
  def r(s, name, dial, auth=True):
    # route
    if auth:
      return s.h(name, [s.auth_handler(), s.reverse_handler(dial)])
    else:
      return s.h(name, [s.reverse_handler(dial)])
  def h(s, name, handles):
    # route from handles
    return {
      'match': [{'host': [f'{name}.{s.domain}']}],
      'handle': handles,
    }
  def reverse_handler(s, dial):
    return {
      'handler': 'reverse_proxy',
      'upstreams': [{'dial': dial}],
      'headers': {'response': {'set': {
        'Strict-Transport-Security': ['max-age=31536000;'],
        'X-Frame-Options': ['SAMEORIGIN'],
        'Content-Security-Policy': ["frame-ancestors 'self'"],
        'X-Content-Type-Options': ['nosniff'],
        'X-XSS-Protection': ['1; mode=block'],
      }}},
    }
  def auth_handler(s):
    return {
      **s.reverse_handler(s.auth_dial),
      'rewrite': {
        'method': 'GET',
        'uri': f'/api/verify?rd=https://{s.auth_name}.{s.domain}:{s.port}',
      },
      'headers': {'request': {'set': {
        'X-Forwarded-Method': ['{http.request.method}'],
        'X-Forwarded-Uri': ['{http.request.uri}'],
      }}},
      'handle_response': [{
        'match': {'status_code': [2]},
        'routes': [{'handle': [{
          'handler': 'headers',
          'request': {'set': {
            'Remote-Email': ['{http.reverse_proxy.header.Remote-Email}'],
            'Remote-Groups': ['{http.reverse_proxy.header.Remote-Groups}'],
            'Remote-Name': ['{http.reverse_proxy.header.Remote-Name}'],
            'Remote-User': ['{http.reverse_proxy.header.Remote-User}'],
          }},
        }]}],
      }],
    }

s = Caddy()

caddy_config = {
  'apps': {
    'http': {
      'servers': {
        'myserver': {
          'listen': [f':{s.port}'],
          'listener_wrappers': [
            {'wrapper': 'http_redirect'},
            {'wrapper': 'tls'},
          ],
          'routes': [{
            'match': [{'host': [f'*.{s.domain}']}],
            'handle': [{
              'handler': 'subroute',
              'routes': s.routes,
            }],
          }],
          'logs': {},
        },
      },
    },
    'tls': {
        'automation': {
            'policies': [{
                'subjects': [f'*.{s.domain}'],
                'issuers': [{
                    'module': 'zerossl',
                    'challenges': {
                        'dns': {
                            'provider': {
                                'name': 'cloudflare',
                                'api_token': sensitive_config.cloudflare_token,
                            }
                        }
                    },
                    'email': sensitive_config.tls_email,
                }]
            }]
        }
    },
    'dynamic_dns': {
      'domains': {s.domain: ['*']},
      'dns_provider': {
        'name': 'cloudflare',
        'api_token': sensitive_config.cloudflare_token,
      },
      'versions': {
        'ipv4': False,
        'ipv6': True,
      },
      'check_interval': '5m',
    },
  },
  'logging': {
      'logs': {
          '': {
              'writer': {
                  'output': 'file',
                  'filename': '/app/data/caddy/access.log',
                  'roll_size_mb': 1000,
              },
              'encoder': {
                  'format': 'json',
              },
          },
      },
  },
}

if __name__ == "__main__":
  with open('caddy.json', 'w') as f:
    json.dump(caddy_config, f, indent=2)

# vim: ts=2:sw=2
