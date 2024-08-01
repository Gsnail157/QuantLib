import numpy as np

class Security:
    def __init__(self) -> None:
        self.cusip = str
        self.isin = str
        self.asset_class = str

class Equity(Security):
    def __init__(self, data:None) -> None:
        self.raw_data = data["raw_data"]
        self.data_source = str
        self.ticker = data["ticker"]
        self.full_name = str
        self.description = str
        self.sector = str
        self.industry = str
        self.country = str
    
    def expected_return(self) -> float:
        percent_change_close = np.array(self.raw_data["PERCENT_CHANGE_CLOSE"])
        return float(percent_change_close.mean())

    def variance(self) -> float:
        percent_change_close = np.array(self.raw_data["PERCENT_CHANGE_CLOSE"])
        return float(percent_change_close.var())

    def std(self) -> float:
        percent_change_close = np.array(self.raw_data["PERCENT_CHANGE_CLOSE"])
        return float(percent_change_close.std())