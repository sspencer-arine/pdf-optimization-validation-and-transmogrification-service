from pathlib import Path

FILE_SAMPLES_PATH = Path(__file__).parent.resolve()

FILE_SAMPLES_BY_SIZE = {
    142786: FILE_SAMPLES_PATH / "file-sample-140k.pdf",
    469513: FILE_SAMPLES_PATH / "file-sample-460k.pdf",
    1042157: FILE_SAMPLES_PATH / "file-sample-1020k.pdf",
}
