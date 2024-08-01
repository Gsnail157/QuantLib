import requests as req
import pandas as pd
import os
from datetime import datetime as dt

class MarketStack:
    base_url = "http://api.marketstack.com/v1/eod"
    def __init__(self, key:str) -> None:
        self.key = key

    def query(self, ticker:str, date_from:None, date_to:None, limit:int, offset:int):
        params = {
            'access_key': self.key,
            'symbols': ticker,
            'date_from': 'blank',
            'date_to': 'blank',
            'limit': 'blank',
            'offset': 'blank'
        }
        res = req.get(self.base_url, params=params, timeout=10)
        return res.json()

    

    