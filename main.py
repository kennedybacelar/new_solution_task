from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple
import pandas as pd
from config import load_config
import os

class DataFile:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.dataframe = pd.read_excel(file_path, sheet_name='input_refresh_template', header=None, index_col=None)
        self._validate_data_frame()
        self.sites_df = self._extract_sites_info()
        self.final_df = pd.DataFrame(_get_final_df_dict(), columns=list(_get_final_df_dict().keys()), dtype=str)
        
    def _validate_data_frame(self):
        start_and_end_dates = self.dataframe.iloc[0:2, 0]
        try:
            start_and_end_dates_as_datetime = pd.to_datetime(start_and_end_dates).tolist()
            self.start_date, self.end_date = [date.to_pydatetime() for date in start_and_end_dates_as_datetime]
        except ValueError as error:
            raise ValueError(f"Not able to parse dates correctly from the excel template {error}")
    
    def _extract_sites_info(self) -> pd.DataFrame:
        pattern_identifier = r'site \d+$'
        mask = self.dataframe.iloc[:, 0].str.match(pattern_identifier).fillna(False)
        return self.dataframe[mask]
        
    def process_sites_df(self):
        copy_sites_df = self.sites_df.copy() # To be deleted
        dates, days_of_month = get_date_and_day_of_month_lists(self.start_date, self.end_date)
        number_of_days_in_interval = len(dates)
        metrics = list(_get_final_df_dict().keys())[3:] # Getting the 5 metrics 
        
        
        copy_sites_df.set_index(copy_sites_df.columns[0], inplace=True)
        for idx in copy_sites_df.index:
            temp_df = pd.DataFrame(_get_final_df_dict())
            temp_df["Day of Month"] = days_of_month
            temp_df["Date"] = dates
            temp_df["Site ID"] = idx

            all_metrics_in_single_list = copy_sites_df.loc[idx].to_list()

            for idx_count, idx_slice  in enumerate(range(0, len(all_metrics_in_single_list), number_of_days_in_interval)):
                temp_df[metrics[idx_count]] = all_metrics_in_single_list[idx_slice: idx_slice + number_of_days_in_interval]
            self.final_df = pd.concat([self.final_df, temp_df], axis=0)
    
    def write_output_file(self):
        sheet_name = 'input_refresh_template'
        output_file_path = f"{load_config()['output_path']}/output_{self.file_path.name}"
        self.final_df.to_excel(output_file_path, sheet_name=sheet_name, index=False)        

def get_input_file_paths() -> List[Path]:
    input_path_str = load_config()["input_path"]
    return [Path(os.path.join(input_path_str, file_path_str)) for file_path_str in os.listdir(input_path_str)]

def get_date_and_day_of_month_lists(start_date: datetime, end_date: datetime) -> Tuple[List[datetime], List[int]]:
    dates = []
    days_of_month = []
    for i in range((end_date - start_date).days + 1):
        dates.append((start_date + timedelta(days=i)).date())
        days_of_month.append((start_date + timedelta(days=i)).day)
    return dates, days_of_month

def _get_final_df_dict():
    return {
        "Day of Month": [],
        "Date": [],
        "Site ID": [],
        "Page Views": [],
        "Unique Visitors": [],
        "Total Time Spent": [],
        "Visits": [],
        "Average Time Spent on Site": []
    }

if __name__ == "__main__":
    all_filepaths = get_input_file_paths()
    for filepath in all_filepaths:
        data_obj = DataFile(filepath)
        data_obj.process_sites_df()
        data_obj.write_output_file()