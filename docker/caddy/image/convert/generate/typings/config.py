from typing import Any, TypedDict, NotRequired

class Tls(TypedDict):
    cloudflare_token: str
    email: str

class Auth(TypedDict):
    name: str
    dial: str

class ServiceRegular(TypedDict):
    dial: str
    paths: NotRequired[dict[str, 'Service']]
    auth: NotRequired[bool]

class ServiceCustom(TypedDict):
    custom_handle: list[dict]

Service = ServiceRegular | ServiceCustom

class Config(TypedDict):
    port: int
    domain: str
    tls: Tls
    auth: Auth
    services: dict[str, Service]

SensitiveConfig = dict[str, Any]

