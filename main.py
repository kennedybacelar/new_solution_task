
from pathlib import Path
from typing import List
import pandas as pd
from config import load_config
import os

class DataFile:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.dataframe = pd.read_excel(file_path)


def get_input_file_paths() -> List[Path]:
    input_path_str = load_config()["input_path"]
    return [Path(os.path.join(input_path_str, file_path_str)) for file_path_str in os.listdir(input_path_str)]

