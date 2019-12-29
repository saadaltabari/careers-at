import os
import uuid

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_serialize import FlaskSerializeMixin
from werkzeug.utils import secure_filename

from file_storage import RESUME_STORAGE


db = SQLAlchemy()


class Candidate(db.Model, FlaskSerializeMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    years_of_experience = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(7), nullable=False)
    resume = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, nullable=False)

    @classmethod
    def create(cls, full_name, dob, years_of_experience, department, resume):
        """
        A static method for saving new candidates to the database.

        :param full_name: str
            name of candidate
        :param dob: str
            date of birth of the candidate
        :param years_of_experience: int
            years of experience the candidate has
        :param department: str
            the department the candidate is applying for
        :param resume: FileStorage
            the candidate's resume file
        :return:
        """
        candidate = cls(
            full_name=full_name,
            dob=dob,
            years_of_experience=years_of_experience,
            department=department,
            created=datetime.now()
        )

        # rename file and save to storage
        resume_filename = "{}-{}".format(str(uuid.uuid4())[:8], secure_filename(resume.filename))
        RESUME_STORAGE.write(resume_filename, resume.read())

        # save file path to db
        candidate.resume = os.path.join(RESUME_STORAGE.base_url, resume_filename)

        db.session.add(candidate)
        db.session.commit()
        return candidate
