
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple
import pandas as pd
from config import load_config
import os

class DataFile:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.dataframe = pd.read_excel(file_path, sheet_name='input_refresh_template', header=None)
        self.validate_data_frame()
        
    def validate_data_frame(self):
        start_and_end_dates = self.dataframe.iloc[0:2, 0]
        try:
            start_and_end_dates_as_datetime = pd.to_datetime(start_and_end_dates).tolist()
            self.start_date, self.end_date = [date.to_pydatetime() for date in start_and_end_dates_as_datetime]
        except ValueError as error:
            raise ValueError(f"Not able to parse dates correctly from the excel template {error}")
        
    def process_dataframe(self):
        pass

def get_input_file_paths() -> List[Path]:
    input_path_str = load_config()["input_path"]
    return [Path(os.path.join(input_path_str, file_path_str)) for file_path_str in os.listdir(input_path_str)]

def get_date_and_day_of_month_lists(start_date: datetime, end_date: datetime) -> Tuple[List[datetime], List[int]]:
    dates = []
    day_of_month = []
    for i in range((end_date - start_date).days + 1):
        dates.append(start_date + timedelta(days=i))
        day_of_month.append((start_date + timedelta(days=i)).day)
    return dates, day_of_month