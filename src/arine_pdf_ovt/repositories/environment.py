import os


class Environment:
    def __init__(self):
        pass

    def aws_s3_bucket_names(self) -> list[str]:
        return os.getenv("AWS_S3_BUCKET_NAMES", "").split(",")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
