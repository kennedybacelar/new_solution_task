
from pathlib import Path
from typing import List
import pandas as pd
from config import load_config
import os

class DataFile:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.dataframe = pd.read_excel(file_path, sheet_name='input_refresh_template')
        self.validate_data_frame()
        
    def validate_data_frame(self):
        start_and_end_dates = self.dataframe["A"].head(2)
        try:
            start_and_end_dates_as_datetime = pd.to_datetime(start_and_end_dates).tolist()
            self.start_date = start_and_end_dates_as_datetime[0]
            self.end_date = start_and_end_dates_as_datetime[1]
        except ValueError as error:
            raise ValueError(f"Not able to parse dates correctly from the excel template {error}")


def get_input_file_paths() -> List[Path]:
    input_path_str = load_config()["input_path"]
    return [Path(os.path.join(input_path_str, file_path_str)) for file_path_str in os.listdir(input_path_str)]

