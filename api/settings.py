import json
import os

ENV_FILE = os.environ.get("ENV_FILE", "config.json")

with open(ENV_FILE, encoding='utf-8') as env_file:
    json_file = json.load(env_file)
    # Clean the json from empty values
    config = {k: v for k, v in json_file.items() if v is not ''}

config["UPLOAD_FOLDER"] = config["FILE_STORAGE"].get("PATH", "")

db_settings = config["DATABASE"]
if db_settings["BACKEND"] == 'sqlite':
    config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////db/sqlite.db"
else:
    config["SQLALCHEMY_DATABASE_URI"] = "{}:///{}:{}@{}/db/".format(
        db_settings["BACKEND"],
        db_settings["USER"],
        db_settings["PASSWORD"],
        db_settings["HOST"]
    )
config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

SETTINGS = config.copy()
