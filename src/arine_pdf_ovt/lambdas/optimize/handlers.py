from pathlib import Path
from tempfile import TemporaryDirectory

from aws_lambda_powertools import Metrics
from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.tracing import Tracer
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.utilities.validation import validator

from arine_pdf_ovt.lambdas.optimize.models import OptimizeDirectRequest, OptimizeDirectResponse
from arine_pdf_ovt.repositories.aws import AwsS3Client, AwsSession
from arine_pdf_ovt.repositories.programs import GhostscriptProgram, ProgramExecutor

logger = Logger()
metrics = Metrics()
tracer = Tracer()


@logger.inject_lambda_context()
@metrics.log_metrics()
@tracer.capture_lambda_handler()
@validator(
    inbound_schema=OptimizeDirectRequest.model_json_schema(), outbound_schema=OptimizeDirectResponse.model_json_schema()
)
def optimize_direct_lambda_handler(event: dict, context: LambdaContext) -> dict:
    request = OptimizeDirectRequest.model_validate(event)
    with (
        AwsSession() as aws_session,
        AwsS3Client(aws_session) as aws_s3_client,
        ProgramExecutor() as program_executor,
        GhostscriptProgram(program_executor) as ghostscript_program,
        TemporaryDirectory() as temp_dir_str,
    ):
        temp_dir_path = Path(temp_dir_str)

        input_pdf_path = temp_dir_path / "input.pdf"
        output_pdf_path = temp_dir_path / "output.pdf"

        aws_s3_client.download_file(request.bucket, request.key, input_pdf_path)
        ghostscript_program.optimize(input_pdf_path, output_pdf_path, dpi=request.dpi)
        aws_s3_client.upload_file(request.bucket, request.key, output_pdf_path)

    return OptimizeDirectResponse(message="Success").model_dump(mode="json")
