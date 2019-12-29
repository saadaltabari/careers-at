import flask_fs as fs


RESUME_STORAGE = fs.Storage("Resumes")


def init_storage(app):
    """
    This function should be called after app
    creation to initialize the file storage
    backend from the application configurations

    :param app: flask app instance
    """
    fs.init_app(app, RESUME_STORAGE)
