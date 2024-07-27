import pandas as pd
import numpy as np
from datetime import datetime as dt
from equity import Equity
from alpha import AlphaVantage
from dotenv import load_dotenv
import os
from preprocessing import data_preprocessing, correlation_table
import itertools
import math

class Portfolio:
    def __init__(self, data) -> None:
        self.user_data = data
        self.expected_return = None
        self.sharpe_ratio = None
        self.variance = None
        self.std = None
        self.securities = {}
        self.tickers = []
        self.start_date = self.user_data["metadata"]["start_date"]
        self.end_date = self.user_data["metadata"]["end_date"]
        self.correlation_table = None
        self.cal_security_data()

    def cal_security_data(self) -> None:
        processed_data = []
        for row in self.user_data["data"]:
            source = row["Source"]
            weight = int(row["Weight"])
            ticker = row["Ticker"]
            raw_data = None
            self.tickers.append(ticker)

            if (source == "Alpha Vantage"):
                load_dotenv()
                key = os.getenv('ALPHAVANTAGE')
                alpha = AlphaVantage(key)
                raw_data = alpha.daily(ticker)
                processed = data_preprocessing(raw_data, self.start_date, self.end_date)
                processed_data.append(processed)
                equity = Equity(processed)
                self.securities[ticker] = {"Weight": weight, "data": equity}
        self.correlation_table = correlation_table(processed_data, self.tickers)
        return

    def sharpeRatio(self) -> float:
        pass

    def report(self) -> None:
        pass

    def cal_std(self) -> None:
        avg_variance = 0
        weighted_std = 2
        correlation_total = 1
        ticker_combinations = list(itertools.combinations(self.correlation_table.columns, 2))
        for ticker1, ticker2 in ticker_combinations:
            correlation_total *= (self.correlation_table.loc[ticker1,ticker2])

        for tick in self.tickers:
            weight = ((self.securities[tick]["Weight"]) / 100)
            var = self.securities[tick]["data"].variance
            std = self.securities[tick]["data"].std
            avg_variance += (weight**2) * var
            weighted_std *= (weight * std)
        port_var = (avg_variance + weighted_std * correlation_total)
        return math.sqrt(port_var)

    def cal_expected_return(self) -> None:
        port_expected_return = 0
        for ticker in self.tickers:
            weight = self.securities[ticker]["Weight"]
            expected_return = (self.securities[ticker]["data"]).avg_expected_return
            port_expected_return += ((weight / 100) * expected_return)

        return port_expected_return

    def target_return(self, target_return:float) -> None:
        ones = np.ones(len(target_return))
        returns = np.array([exp_return.avg_expected_return for exp_return in equities])
        a = np.array([returns, ones])
        b = np.array([target_return, 1])
        weights = np.linalg.solve(a,b)

        if not np.allclose(np.dot(a, x), b):
            return "Something went wrong"
        else:
            return weights

    def target_beta(self, target_beta:float) -> None:
        ones = np.ones(len(target_beta))
        betas = np.array([exp_return.beta for exp_return in equities])
        a = np.array([betas, ones])
        b = np.array([target_beta, 1])
        weights = np.linalg.solve(a,b)

        if not np.allclose(np.dot(a, x), b):
            return "Something went wrong"
        else:
            return weights
    

    
