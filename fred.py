import requests

class FredAPI:
    base_url = "https://api.stlouisfed.org/fred/"
    def __init__(self, key:str) -> None:
        self.key = key

    def time_series(self, series_id:str, limit:int=1000, sort_order:str="asc", file_type:str="json") -> None:
        url = self.base_url + "series/observations"
        params = {
            "api_key": self.key,
            "series_id": series_id,
            "limit": limit,
            "sort_order": sort_order,
            "file_type": file_type
        }

        res = requests.get(url, params=params)
        data = res.json()
        return data

    def get_risk_free_rate(self) -> float:
        series_id = "DGS10"
        limit = 1
        sort_order = "desc"
        file_type = 'json'
        data = self.time_series(series_id=series_id,limit=limit,sort_order=sort_order, file_type=file_type)
        return float(data['observations'][0]['value'])

