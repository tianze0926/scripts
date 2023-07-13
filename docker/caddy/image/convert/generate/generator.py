from .proxy import handle_auth
from .typings.config import Config

class Generator:
    from .proxy import caddy_config_route
    from .template import gen_config
    def __init__(self, config: Config):
        self.config = config
        self.caddy_config_handle_auth = handle_auth(config)

        self.caddy_config = self.generate()

    def generate(self):
        caddy_config_routes_services = [
            self.caddy_config_route({
                'type': 'host',
                'value': f'{name}.{self.config["domain"]}'
            }, route)
            for name, route in {
                self.config["auth"]["name"]: {
                    'dial': self.config["auth"]["dial"],
                    'auth': False,
                },
                **self.config["services"]
            }.items()
        ] + [{
            'handle': [{
                "abort": True,
                "handler": "static_response"
            }],
            'terminal': True,
        }]
        return self.gen_config(
            self.config["port"],
            self.config["domain"],
            caddy_config_routes_services
        )

