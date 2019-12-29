import os

SETTINGS = {
    "SQLALCHEMY_DATABASE_URI":  "{}://{}:{}@{}:{}/{}".format(
        os.environ.get("DB_BACKEND"),
        os.environ.get("DB_USER"),
        os.environ.get("DB_PASSWORD"),
        os.environ.get("DB_HOST"),
        os.environ.get("DB_PORT"),
        os.environ.get("DB_NAME")
    ),
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "FS_ROOT": "/uploads",
    "FS_BACKEND": "local", # s3

    # Set the FS_Backend to s3 and
    # configure the following settings
    # to use AWS S3 Storage backend.

    # "FS_S3_ACCESS_KEY": "",
    # "FS_S3_SECRET_KEY": "",
    # "FS_S3_ENDPOINT": "https://BUCKET_NAME.s3.amazonaws.com/",
    # "FS_S3_REGION": "",
    "ACCEPTED_RESUME_TYPES_MIME": {
        "pdf":  "application/pdf",
        "docx":  "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    },
    "ACCEPTED_CANDIDATE_DEPARTMENTS": ["HR", "IT", "FINANCE"]
}
