import os
from pathlib import Path
from subprocess import check_output  # noqa: S404

PROGRAM_PATH_ENV = ":".join(["/opt/programs/view/bin", *os.environ.get("PATH", "").split(":")])


class ProgramExecutor:
    def __init__(self):
        pass

    def execute(self, command: list[str]) -> str:
        return check_output(  # noqa: S603
            command,
            env={
                "PATH": PROGRAM_PATH_ENV,
            },
        ).decode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class GhostscriptProgram:
    def __init__(self, program_executor: ProgramExecutor):
        self.program_executor = program_executor

    def version(self) -> str:
        return self.program_executor.execute(["gs", "--version"])

    def help(self) -> str:  # noqa: A003
        return self.program_executor.execute(["gs", "--help"])

    def optimize(self, input_pdf_path: Path, output_pdf_path: Path, dpi: int = 600) -> str:
        input_pdf_path = input_pdf_path.resolve()
        output_pdf_path = output_pdf_path.resolve()
        return self.program_executor.execute(
            [
                "gs",
                "-sDEVICE=pdfwrite",
                "-dCompatibilityLevel=1.4",
                "-dPDFSETTINGS=/printer",
                "-dCompressFonts=true",
                "-dSubsetFonts=true",
                "-dDownsampleColorImages=true",
                f"-dColorImageResolution={dpi}",
                "-dColorImageDownsampleType=/Bicubic",
                "-dDownsampleGrayImages=true",
                f"-dGrayImageResolution={dpi}",
                "-dGrayImageDownsampleType=/Bicubic",
                "-dDownsampleMonoImages=true",
                f"-dMonoImageResolution={dpi}",
                "-dMonoImageDownsampleType=/Subsample",
                "-dInterpolationFilter=/Bicubic",
                "-dNOPAUSE",
                "-dBATCH",
                f"-sOutputFile={output_pdf_path}",
                f"{input_pdf_path}",
            ]
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
