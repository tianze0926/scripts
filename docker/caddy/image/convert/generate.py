import re
import yaml
import json
from pathlib import Path

from tap import Tap
from typeguard import check_type

from generate.generator import Generator
from generate.typings.config import Config, SensitiveConfig


class ArgumentParser(Tap):
    input_config: str
    input_sensitive_config: str | None
    output_caddy_config: str

if __name__ == '__main__':
    args = ArgumentParser().parse_args()

    with open(args.input_config, 'r') as f:
        config: Config = yaml.safe_load(f)
    check_type(config, Config)

    generator = Generator(config)
    json_str = json.dumps(generator.caddy_config, indent=2)

    def replace_placeholders(s: str):
        if args.input_sensitive_config is None:
            return
        p = Path(args.input_sensitive_config)
        if not p.is_file():
            return
        with open(p, 'r') as f:
            sensitive_config: SensitiveConfig = yaml.safe_load(f)
        check_type(sensitive_config, SensitiveConfig)
        for match in re.findall(r'\$\{(.*?)\}', s):
            s = s.replace(
                f'${{{match}}}',
                sensitive_config[match]
            )
    replace_placeholders(json_str)

    with open(args.output_caddy_config, 'w') as f:
        f.write(json_str)

