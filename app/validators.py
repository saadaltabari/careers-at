from werkzeug.datastructures import FileStorage
from datetime import datetime

from settings import SETTINGS


class RequestValidator:
    """
    A base class used to validate input from HTTP requests

    Attributes
    ----------
    INPUT_FIELDS : list
        a list of strings representing the input fields that
        are to be passed with the request. Subclasses must
        override this field.
    REQUIRED_FIELDS : list
        a list of strings representing the input fields that
        must be passed with the request. Subclasses must
        override this field. if the value __all__ is given
        then all INPUT_FIELDS must be passed with the request.
    request: flask.request
        the http request to validate.

    Methods
    -------
    validate()
        validates data passed with the request object and
        saves errors in the error dictionary object.
    """
    INPUT_FIELDS = None
    REQUIRED_FIELDS = None

    def __init__(self, request):
        """
        :param request: flask.request object representing the HTTP
         request to validate.
        """
        self.data = {**request.data, **request.files}
        self.errors = {}

    def get_input_fields(self):
        assert self.INPUT_FIELDS is not None,\
            "Subclasses of RequestValidator should override INPUT_FIELDS"
        return self.INPUT_FIELDS

    def get_required_fields(self):
        assert self.REQUIRED_FIELDS is not None,\
            "Subclasses of RequestValidator should override REQUIRED_FIELDS"
        return self.INPUT_FIELDS if self.REQUIRED_FIELDS == "__all__" else self.REQUIRED_FIELDS

    def validate(self):
        """
        validates data passed with the request object.
            - checks for required input
            - runs all subclass implemented validation methods
            ( methods starting with validate_ )
            - saves errors in the error dictionary object

        :return: True if the request object is valid. False otherwise.
        """

        # Check for required input fields
        for field in self.get_required_fields():
            if field not in self.data or self.data[field] in [None, '']:
                self.errors[field] = ["This field is required."]

        # Run input field specific validation methods
        for field in self.get_input_fields():
            if field in self.data and hasattr(self, "validate_{}".format(field)):
                validate_field = getattr(self, "validate_{}".format(field))
                try:
                    self.data[field] = validate_field(self.data[field])
                except Exception as e:
                    self.errors[field] = self.errors.get(field, [])
                    self.errors[field].append(str(e))

        return self.errors.__len__() == 0


class CreateCandidateRequestValidator(RequestValidator):
    """
    A class for validating create candidate HTTP requests
    """
    INPUT_FIELDS = ("full_name", "dob", "years_of_experience", "department", "resume")
    REQUIRED_FIELDS = "__all__"

    def validate_dob(self, value):
        """
        validate date of birth format is YYY-MM-DD

        :param value: str representing date of birth
        :return: datetime.date object representing date of birth
        :raises ValueError if date of birth string format is incorrect
        """
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Use YYYY-MM-DD for date format")

    def validate_resume(self, value):
        """
        validate uploaded resume file type is acceptable.

        :param value: FileStorage for the candidate uploaded resume
        :return: FileStorage for the candidate uploaded resume
        :raises: AssertionError if file format is unacceptable.
        """
        accepted_resume_file_types = SETTINGS.get("ACCEPTED_RESUME_TYPES_MIME", {})
        assert isinstance(value, FileStorage)\
            and value.mimetype in accepted_resume_file_types.values(),\
            "resume should be a file of the following types {}".format(list(accepted_resume_file_types.keys()))
        return value

    def validate_department(self, value):
        """
        validate selected department is acceptable.

        :param value: str representing the department name.
        :return: str representing the department name.
        :raises: AssertionError if selected department is unacceptable.
        """
        valid_departments = SETTINGS.get("ACCEPTED_CANDIDATE_DEPARTMENTS", [])
        assert value.upper() in valid_departments,\
            "Department should be one of the following {}".format(valid_departments)
        return value.upper()
