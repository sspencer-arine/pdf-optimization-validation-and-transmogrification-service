import os
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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
