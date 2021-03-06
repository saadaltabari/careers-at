from flask import request, redirect
from flask_api import FlaskAPI

from decorators import authorize_admin_users_only
from file_storage import init_storage, RESUME_STORAGE
from models import db, Candidate
from settings import SETTINGS
from validators import CreateCandidateRequestValidator


# Initialize the application
app = FlaskAPI(__name__)
app.config.from_mapping(SETTINGS)
db.init_app(app)
init_storage(app)


@app.route('/api/candidates', methods=['GET'])
@authorize_admin_users_only
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


@app.route('/api/candidate-resume/<int:candidate_id>', methods=['GET'])
@authorize_admin_users_only
def get_candidate_resume(candidate_id):
    """
    Download candidate resume endpoint.
    Endpoint for administrators to install candidate resume files

    :param candidate_id: int
    :return: PDF or DOCX file
    """
    candidate = Candidate.query.get_or_404(candidate_id)
    return redirect(candidate.resume)


if __name__ == '__main__':
    app.run()
