from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from generate.generator import Generator


def handle_auth(config):
    return {
        'handler': 'reverse_proxy',
        'upstreams': [{'dial': config["auth"]["dial"]}],
        'rewrite': {
            'method': 'GET',
            'uri': f'/api/verify?rd=https://{config["auth"]["name"]}.{config["domain"]}:{config["port"]}',
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

def caddy_config_route(self: Generator, match, service_route):
    if 'custom_handle' in service_route:
        handles = service_route["custom_handle"]
    else:
        require_auth = True if 'auth' not in service_route else service_route["auth"]
        handle = {
            'handler': 'reverse_proxy',
            'upstreams': [{'dial': service_route["dial"]}],
        }
        handles = [self.caddy_config_handle_auth, handle] if require_auth else [handle]
    
        if 'paths' in service_route:
            caddy_routes = [
                self.caddy_config_route({'type': 'path', 'value': path}, sub_route)
                for path, sub_route in service_route["paths"].items()
            ]
            handles = [{
                'handler': 'subroute',
                'routes': caddy_routes + [{'handle': handles}]
            }]
    
    return {
        'match': [{match["type"]: [match["value"]]}],
        'handle': handles,
    }
