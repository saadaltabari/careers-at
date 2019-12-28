import json
import os

ENV_FILE = os.environ.get("ENV_FILE", "config.json")

with open(ENV_FILE, encoding='utf-8') as env_file:
    json_file = json.load(env_file)
    # Clean the json from empty values
    config = {k: v for k, v in json_file.items() if v is not ''}

db_settings = config["DATABASE"]
config["SQLALCHEMY_DATABASE_URI"] = "{}://{}:{}@{}:3306/{}".format(
    db_settings["BACKEND"],
    db_settings["USER"],
    db_settings["PASSWORD"],
    db_settings["HOST"],
    db_settings["NAME"],
)
config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

SETTINGS = config.copy()
