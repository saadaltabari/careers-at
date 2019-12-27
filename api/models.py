import os
import uuid

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_serialize import FlaskSerializeMixin
from werkzeug.utils import secure_filename

from settings import SETTINGS


db = SQLAlchemy()


class Candidate(db.Model, FlaskSerializeMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    years_of_experience = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(7), nullable=False)
    resume = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, nullable=False)

    @classmethod
    def create(cls, **kwargs):
        candidate = cls(
            full_name=kwargs["full_name"],
            dob=kwargs["dob"],
            years_of_experience=kwargs["years_of_experience"],
            department=kwargs["department"],
            created=datetime.now()
        )

        resume = kwargs['resume']

        secure_filename(resume.filename)
        resume_filename = "{}-{}".format(str(uuid.uuid4())[:8], secure_filename(resume.filename))
        resume.save(os.path.join(SETTINGS['UPLOAD_FOLDER'], resume_filename))

        candidate.resume = resume_filename

        db.session.add(candidate)
        db.session.commit()
        return candidate
