from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from generate.generator import Generator


def http(port: int, domain: str, routes: list):
    return {
        'servers': {
            'myserver': {
                'listen': [f':{port}'],
                'listener_wrappers': [
                    {'wrapper': 'http_redirect'},
                    {'wrapper': 'tls'}
                ],
                'routes': [{
                    'match': [{'host': [f'*.{domain}']}],
                    'handle': [{
                        'handler': 'subroute',
                        'routes': routes,
                    }],
                }],
                'logs': {},
            }
        }
    }

def tls(self: Generator, domain: str):
    return {
        'automation': {
            'policies': [{
                'subjects': [f'*.{domain}'],
                'issuers': [{
                    'module': 'zerossl',
                    'challenges': {
                        'dns': {
                            'provider': {
                                'name': 'cloudflare',
                                'api_token': self.config['tls']['cloudflare_token'],
                            }
                        }
                    },
                    'email': self.config['tls']['email'],
                }]
            }]
        }
    }

def logging():
    return {
        'logs': {
            '': {
                'writer': {
                    'output': 'file',
                    'filename': '/app/access.log',
                    'roll_size_mb': 1000,
                },
                'encoder': {
                    'format': 'json',
                },
            },
        },
    }

def gen_config(self: Generator, port: int, domain: str, routes: list):
    return {
        'apps': {
            'http': http(port, domain, routes),
            'tls': tls(self, domain),
        },
        'logging': logging(),
    }
