from typing import TYPE_CHECKING, Iterator

from boto3 import Session
from moto import mock_aws
from pytest import MonkeyPatch, fixture

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client, S3ServiceResource


@fixture
def aws_environment(monkeypatch: MonkeyPatch) -> Iterator[None]:
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "test_access_key")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "test_secret_key")
    yield None


@fixture
def aws_session(aws_environment: MonkeyPatch) -> Iterator[Session]:
    yield Session()


@fixture
def mock_aws_s3_client(aws_session: Session) -> Iterator["S3Client"]:
    with mock_aws():
        yield aws_session.client("s3")


@fixture
def mock_aws_s3_resource(aws_session: Session) -> Iterator["S3ServiceResource"]:
    with mock_aws():
        yield aws_session.resource("s3")


@fixture
def mock_lambda_context() -> Iterator[object]:
    class MockLambdaContext:
        def __init__(self):
            self.function_name = "test_function"
            self.memory_limit_in_mb = 128
            self.aws_request_id = "test_request_id"
            self.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test_function"

        def get_remaining_time_in_millis(self) -> int:
            return 30000

    yield MockLambdaContext()
