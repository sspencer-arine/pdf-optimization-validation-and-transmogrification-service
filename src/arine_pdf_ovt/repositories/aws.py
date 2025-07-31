from pathlib import Path
from typing import TYPE_CHECKING, Literal, overload

import boto3

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client, S3ServiceResource


class AwsSession:
    def __init__(self, profile_name: str | None = None, region_name: str | None = None):
        self.session = boto3.Session(profile_name=profile_name, region_name=region_name)

    @overload
    def create_client(self, service_name: Literal["s3"]) -> "S3Client": ...

    @overload
    def create_client(self, service_name: Literal["s3", "dynamodb"]): ...

    def create_client(self, service_name: Literal["s3", "dynamodb"]):
        return self.session.client(service_name)

    @overload
    def create_resource(self, service_name: Literal["s3"]) -> "S3ServiceResource": ...

    @overload
    def create_resource(self, service_name: Literal["s3", "dynamodb"]):
        return self.session.resource(service_name)

    def create_resource(self, service_name: Literal["s3", "dynamodb"]):
        return self.session.resource(service_name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class AwsS3Client:
    def __init__(self, aws_session: AwsSession):
        self.aws_session = aws_session
        self.aws_s3_client = aws_session.create_client("s3")

    def download_file(self, bucket: str, key: str, pdf_path: Path):
        self.aws_s3_client.download_file(bucket, key, str(pdf_path))

    def upload_file(self, bucket: str, key: str, pdf_path: Path):
        self.aws_s3_client.upload_file(str(pdf_path), bucket, key)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class AwsS3Resource:
    def __init__(self, aws_session: AwsSession):
        self.aws_session = aws_session
        self.aws_s3_resource = aws_session.create_resource("s3")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
