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
        dataDirectory = os.getcwd() + '\\Data'
        filename = f'{ticker}_DAILY_{today_string}.csv'
        fullPath = os.path.join(dataDirectory, filename)
        fileExists = os.path.exists(fullPath)

        if not fileExists:
            # Make Request
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&datatype=json&symbol={ticker}&apikey={self.key}'
            r = req.get(url)
            data = r.json()

            # Unwrap load
            metaData = data['Meta Data']
            body = data["Time Series (Daily)"]
            dataframe = pd.DataFrame()

            for attribute, values in body.items():
                datetime_obj = dt.strptime(attribute, "%Y-%m-%d")
                newRow = pd.DataFrame(values, index=[datetime_obj])
                dataframe = pd.concat([dataframe, newRow])

            dataframe.to_csv(fullPath)
            return dataframe
            
        else:
            print(f"{filename} data already exists on disk")
            data = pd.read_csv(fullPath)
            return data




