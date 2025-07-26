from subprocess import check_output  # noqa: S404

from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext


def lambda_handler(event: dict, context: LambdaContext) -> dict:

    ghostscript_version = check_output(["/opt/programs/view/bin/gs", "--version"]).decode("utf-8")  # noqa: S603, S607
    ghostscript_help = check_output(["/opt/programs/view/bin/gs", "--help"]).decode("utf-8")  # noqa: S603, S607
    qpdf_version = check_output(["/opt/programs/view/bin/qpdf", "--version"]).decode("utf-8")  # noqa: S603, S607
    qpdf_help = check_output(["/opt/programs/view/bin/qpdf", "--help"]).decode("utf-8")  # noqa: S603, S607
    tar_version = check_output(["/opt/programs/view/bin/tar", "--version"]).decode("utf-8")  # noqa: S603, S607
    tar_help = check_output(["/opt/programs/view/bin/tar", "--help"]).decode("utf-8")  # noqa: S603, S607
    zip_version = check_output(["/opt/programs/view/bin/zip", "--version"]).decode("utf-8")  # noqa: S603, S607
    zip_help = check_output(["/opt/programs/view/bin/zip", "--help"]).decode("utf-8")  # noqa: S603, S607

    return {
        "ghostscript": {
            "version": ghostscript_version,
            "help": ghostscript_help,
        },
        "qpdf": {
            "version": qpdf_version,
            "help": qpdf_help,
        },
        "tar": {
            "version": tar_version,
            "help": tar_help,
        },
        "zip": {
            "version": zip_version,
            "help": zip_help,
        },
    }
