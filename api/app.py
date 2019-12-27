from flask import request
from flask_api import FlaskAPI

from settings import SETTINGS
from models import db, Candidate
from validators import CreateCandidateRequestValidator


app = FlaskAPI(__name__)

app.config.from_mapping(SETTINGS)

db.init_app(app)


@app.route('/api/candidates', methods=['GET'])
def list_candidates():
    """
    List Candidates endpoint.
    Get the list of candidates who uploaded their resumes.

    responses:
        200:
            :return: json list of all candidates.
        403:
            Permission to view list of candidates denied.
    """
    return Candidate.json_list(Candidate.query.order_by(db.desc(Candidate.created)).all())


@app.route('/api/candidates', methods=['POST'])
def create_candidate():
    """
    Create new candidate endpoint.
    Endpoint for candidates to submit their information

    responses:
        200:
            :return json candidate object
            description: Foo object to be returned.
        400:
            ":return json errors object
            Candidate data is missing or incorrect.
    """
    validator = CreateCandidateRequestValidator(request)

    if validator.validate():
        candidate = Candidate.create(**validator.data)
        return candidate.as_json, 201

    return validator.errors, 400


if __name__ == '__main__':
    app.run()
