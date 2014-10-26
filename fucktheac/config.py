import os
import toml

CONFIG_FILE = os.environ.get('CONFIG_FILE', "config.toml")
CONFIG = {}


with open(CONFIG_FILE, 'r') as f:
    CONFIG = toml.loads(f.read())
