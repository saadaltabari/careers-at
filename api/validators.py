from werkzeug.datastructures import FileStorage
from datetime import datetime

from settings import SETTINGS


class RequestValidator:
    input_fields = None
    required_fields = None

    def __init__(self, request):
        self.data = {**request.data, **request.files}
        self.errors = {}

    def get_input_fields(self):
        assert self.input_fields is not None
        return self.input_fields

    def get_required_fields(self):
        assert self.required_fields is not None
        return self.input_fields if self.required_fields == "__all__" else self.required_fields

    def validate(self):
        for field in self.get_required_fields():
            if field not in self.data or self.data[field] in [None, '']:
                self.errors[field] = ["This field is required."]

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
    input_fields = ("full_name", "dob", "years_of_experience", "department", "resume")
    required_fields = "__all__"

    def validate_dob(self, value):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise Exception("Use YYYY-MM-DD for date format")

    def validate_resume(self, value):
        accepted_resume_file_types = SETTINGS.get("ACCEPTED_RESUME_TYPES_MIME", {})
        assert isinstance(value, FileStorage)\
            and value.mimetype in accepted_resume_file_types.values(),\
            "resume should be a file of the following types {}".format(list(accepted_resume_file_types.keys()))
        return value

    def validate_department(self, value):
        valid_departments = SETTINGS.get("ACCEPTED_CANDIDATE_DEPARTMENTS", [])
        assert value.upper() in valid_departments,\
            "Department should be one of the following {}".format(valid_departments)
        return value.upper()
