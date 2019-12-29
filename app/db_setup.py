from models import db
from api import app
from settings import SETTINGS


if __name__ == '__main__':
    DB_URL = SETTINGS.get("SQLALCHEMY_DATABASE_URI")

    db.create_engine(DB_URL, {})

    with app.app_context():
        db.create_all(app=app)
        db.session.commit()
