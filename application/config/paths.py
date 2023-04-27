from pathlib import Path
from typing import Final

ROOT_PATH: Final[Path] = Path(__file__).parents[2]
OUTPUT_FILES_PATH: Final[Path] = ROOT_PATH.joinpath("files_output")
OUTPUT_DATA_PATH: Final[Path] = OUTPUT_FILES_PATH.joinpath("output_data.txt")
