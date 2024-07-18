import pandas as pd
import numpy as np

class Equity:
    def __init__(self, data:None) -> None:
        self.data = data
        self.avg_expected_return = None
        self.variance = None
        self.std = None
        self.calculate()
        
    def calculate(self) -> None:
        daily_return_array = np.array(self.data["PERCENT_CHANGE_CLOSE"])
        self.avg_expected_return = daily_return_array.mean()
        self.variance = daily_return_array.var()
        self.std = daily_return_array.std()
        return None
