import os
from datetime import datetime as dt

import requests as req
import pandas as pd

class EODhd:
    base_url = "https://eodhd.com/api/eod/"
    def __init__(self, key:str) -> None:
        self.key = key

    def eod_historical(self, ticker:str, exchange:str) -> None:
        today = dt.today()
        today_string = today.strftime("%Y%m%d")
        data_directory = os.getcwd() + '\\Data\\MarketStack'
        filename = f'{ticker}_DAILY_{today_string}.csv'
        full_path = os.path.join(data_directory, filename)
        file_exists = os.path.exists(full_path)

        if not file_exists:
            url = self.base_url + f"{ticker}.{exchange}"
            params = {
                "api_token": self.key,
                "fmt": "json",
                "period": "m", # d - daily, m - monthly, w - weekly
                "order": "d", # d - descending, a - ascending
                # "from": "2024-08-01",
                # "to": "2020-08-01"
            }

            res = req.get(url, params=params, timeout=10)
            data = res.json()

            dataframe = pd.DataFrame()
            for value in data:
                new_row = pd.DataFrame(value)
                dataframe = pd.concat(dataframe, new_row)
            
            dataframe.to_csv(full_path)
            return dataframe
            
        else:
            print(f"{filename} data from EoDHD already exists on disk")
            data = pd.read_csv(full_path)
            return data

        return data