from models import db
from app import app
from settings import SETTINGS


if __name__ == '__main__':
    DB_URL = SETTINGS.get("SQLALCHEMY_DATABASE_URI")

    engine = db.create_engine(DB_URL, {})

    DB_NAME = SETTINGS["DATABASE"]["NAME"]
    if DB_NAME:
        engine.execute("CREATE DATABASE IF NOT EXISTS %s ;" % DB_NAME)
        engine.execute("USE %s;" % DB_NAME)

    with app.app_context():
        db.create_all(app=app)
        db.session.commit()
