from uuid import uuid1

from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from arine_pdf_ovt.repositories.aws import AwsS3Client, AwsSession
from arine_pdf_ovt.repositories.environment import Environment
from arine_pdf_ovt.repositories.programs import GhostscriptProgram, ProgramExecutor

logger = Logger()
instance_id = str(uuid1())


@logger.inject_lambda_context
def health_check_direct_lambda_handler(event: dict, context: LambdaContext) -> dict:

    with (
        AwsSession() as aws_session,
        AwsS3Client(aws_session) as aws_s3_client,
        ProgramExecutor() as program_executor,
        GhostscriptProgram(program_executor) as ghostscript_program,
        Environment() as environment,
    ):
        aws_s3_bucket_names = environment.aws_s3_bucket_names()
        aws_s3_bucket_health_checks = {}

        for aws_s3_bucket in aws_s3_bucket_names:
            try:
                aws_s3_client.aws_s3_client.head_bucket(Bucket=aws_s3_bucket)
                aws_s3_bucket_health_checks[aws_s3_bucket] = "Healthy"
            except Exception as e:
                logger.error(f"Failed to access S3 bucket {aws_s3_bucket}: {e}")
                aws_s3_bucket_health_checks[aws_s3_bucket] = "Unhealthy"

        return {
            "instance_id": instance_id,
            "programs": {
                "ghostscript": {
                    "version": ghostscript_program.version(),
                    "help": ghostscript_program.help(),
                },
            },
            "environment": {
                "aws_s3_buckets": aws_s3_bucket_names,
            },
            "aws_s3_bucket_health_checks": aws_s3_bucket_health_checks,
        }
