import json
from pathlib import Path
from typing import Dict

CONFIG_DIR = Path(__file__).resolve().parent.parent / 'agent_config_settings'


def load_agent_configs() -> Dict[str, Dict]:
    """Load all JSON files from agent_config_settings and return a mapping name->config dict.

    - Skips files that don't end with .json
    - Returns parsed JSON content as Python dicts
    - Does not resolve secrets; configs may contain references to secret stores
    """
    configs = {}
    if not CONFIG_DIR.exists():
        return configs

    for p in CONFIG_DIR.glob('*.json'):
        try:
            with p.open('r', encoding='utf-8') as fh:
                cfg = json.load(fh)
                configs[p.stem] = cfg
        except Exception as e:
            # keep loading other files; surface an error in the dict for diagnostics
            configs[p.stem] = {"_error": str(e)}
    return configs


if __name__ == '__main__':
    import pprint
    print('Loading agent configs from', CONFIG_DIR)
    pprint.pprint(load_agent_configs())
