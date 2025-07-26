from aws_lambda_powertools import Metrics
from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.tracing import Tracer
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.utilities.validation import validator

from arine_pdf_ovt.s3_direct.models import S3DirectRequest, S3DirectResponse

logger = Logger()
tracer = Tracer()
metrics = Metrics()


@metrics.log_metrics(capture_cold_start_metric=True)
@tracer.capture_lambda_handler(capture_response=False, capture_error=False)
@logger.inject_lambda_context
@validator(inbound_schema=S3DirectRequest.model_json_schema(), outbound_schema=S3DirectResponse.model_json_schema())
def s3_direct_handler(event: dict, context: LambdaContext) -> dict:
    # request = S3DirectRequest.model_validate(event)
    return S3DirectResponse(message="Success").model_dump(mode="json")
