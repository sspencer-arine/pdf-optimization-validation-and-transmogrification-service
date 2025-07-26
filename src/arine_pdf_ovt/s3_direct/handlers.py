from aws_lambda_powertools import Metrics
from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.tracing import Tracer
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.utilities.validation import validator

from arine_pdf_ovt.repositories.aws import AwsS3Client, AwsSession
from arine_pdf_ovt.repositories.programs import GhostscriptProgram, ProgramExecutor
from arine_pdf_ovt.s3_direct.models import S3DirectRequest, S3DirectResponse

logger = Logger()
metrics = Metrics()
tracer = Tracer()


@logger.inject_lambda_context()
@metrics.log_metrics()
@tracer.capture_lambda_handler()
@validator(inbound_schema=S3DirectRequest.model_json_schema(), outbound_schema=S3DirectResponse.model_json_schema())
def s3_direct_handler(event: dict, context: LambdaContext) -> dict:

    with (
        AwsSession() as aws_session,
        AwsS3Client(aws_session) as aws_s3_client,
        ProgramExecutor() as program_executor,
        GhostscriptProgram(program_executor) as ghostscript_program,
    ):
        print(ghostscript_program.version(), aws_s3_client)  # noqa: T201

    # request = S3DirectRequest.model_validate(event)
    return S3DirectResponse(message="Success").model_dump(mode="json")
