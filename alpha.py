import requests as req
import pandas as pd
import os
from datetime import datetime as dt

class AlphaVantage:
    def __init__(self, key:str) -> None:
        self.key = key

    def daily(self, ticker:str) -> None:
        # Check if Data in already available on hard disk
        today = dt.today()
        today_string = today.strftime("%Y%m%d")
        dataDirectory = os.getcwd() + 'Data'
        filename = f'{ticker}_DAILY_{today_string}.csv'
        fullPath = os.path.join(dataDirectory, filename)
        fileExists = os.path.exists(fullPath)

        if not fileExists:
            # Make Request
            base_url = f'https://www.alphavantage.co/query'
            params = {
                'function': "TIME_SERIES_DAILY",
                'outputsize': "full",
                'datatype': "json",
                'symbol': ticker,
                'apikey': self.key
            }
            r = req.get(base_url, params=params)
            data = r.json()

            # Unwrap load
            #metaData = data['Meta Data']
            body = data["Time Series (Daily)"]
            dataframe = pd.DataFrame()
            # dataframe = pd.to_datetime(dataframe.index)

            for attribute, values in body.items():
                datetime_obj = dt.strptime(attribute, "%Y-%m-%d")
                newRow = pd.DataFrame(values, index=[datetime_obj])
                dataframe = pd.concat([dataframe, newRow])
            
            col_name_mappings = {
                "1. open": "OPEN",
                "2. high": "HIGH",
                "3. low": "LOW",
                "4. close": "CLOSE",
                "5. volume": "VOLUME"
            }
            
            dataframe.rename(columns=col_name_mappings, inplace=True)
            dataframe.to_csv(fullPath)
            clean_data = pd.read_csv(fullPath, index_col=0)
            return clean_data
            
        else:
            print(f"{filename} data already exists on disk")
            data = pd.read_csv(fullPath, index_col=0)
            return data




