import json
import os

ENV_FILE = os.environ.get("ENV_FILE", "config.json")

with open(ENV_FILE, encoding='utf-8') as env_file:
    json_file = json.load(env_file)
    # Clean the json from empty values
    SETTINGS = {k: v for k, v in json_file.items() if v is not ''}
