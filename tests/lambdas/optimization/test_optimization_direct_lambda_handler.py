from pathlib import Path
from typing import TYPE_CHECKING

from fixtures.pdfs.files import FILE_SAMPLES_BY_SIZE  # type: ignore[import-not-found]
from pytest import mark

from arine_pdf_ovt.lambdas.optimize.handlers import optimize_direct_lambda_handler
from arine_pdf_ovt.lambdas.optimize.models import OptimizeDirectRequest, OptimizeDirectResponse

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3ServiceResource


@mark.parametrize(
    ("file_size", "file_path"),
    FILE_SAMPLES_BY_SIZE.items(),
)
def test_optimize_direct_lambda_handler_standard_pdf(
    mock_aws_s3_resource: "S3ServiceResource",
    mock_lambda_context: object,
    file_size: int,
    file_path: Path,
    tmp_path: Path,
):
    mock_aws_s3_bucket = mock_aws_s3_resource.Bucket("test-bucket")
    mock_aws_s3_bucket.create()
    mock_aws_s3_bucket.upload_file(str(file_path), "file.pdf")

    response = OptimizeDirectResponse.model_validate(
        optimize_direct_lambda_handler(
            OptimizeDirectRequest.model_validate(
                {
                    "bucket": "test-bucket",
                    "key": "file.pdf",
                    "dpi": 150,
                }
            ).model_dump(mode="json"),
            mock_lambda_context,
        )
    )

    assert response.message == "Success"

    temp_pdf_file_path = tmp_path / "file.pdf"
    mock_aws_s3_bucket.download_file("file.pdf", str(temp_pdf_file_path))

    assert file_size > temp_pdf_file_path.stat().st_size
