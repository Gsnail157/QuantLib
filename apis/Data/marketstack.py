import os
from datetime import datetime as dt

import requests as req
import pandas as pd

class MarketStack:
    base_url = "http://api.marketstack.com/v1/eod"
    def __init__(self, key:str) -> None:
        self.key = key

    def query(self, ticker:str, limit:int, offset:int):
        params = {
            'access_key': self.key,
            'symbols': ticker,
            # 'date_from': date_from,
            # 'date_to': date_to,
            'limit': limit,
            'offset': offset
        }
        res = req.get(self.base_url, params=params, timeout=10)
        return res.json()

    def eod(self, ticker) -> None:
        today = dt.today()
        today_string = today.strftime("%Y%m%d")
        data_directory = os.getcwd() + '\\Data\\MarketStack'
        filename = f'{ticker}_DAILY_{today_string}.csv'
        full_path = os.path.join(data_directory, filename)
        file_exists = os.path.exists(full_path)

        if not file_exists:
            data = self.query(ticker=ticker, limit=1000, offset=0)
            count = data["pagination"]["count"]
            total = data["pagination"]["count"]
            offset = data["pagination"]["count"]

            dataframe = pd.DataFrame()

            for value in data["data"]:
                new_row = pd.DataFrame(value, index=['date'])
                dataframe = pd.concat([dataframe, new_row])

            dataframe.to_csv(full_path)
            return dataframe
        else:
            print(f"{filename} data from MarketData already exists on disk")
            data = pd.read_csv(full_path)
            return data