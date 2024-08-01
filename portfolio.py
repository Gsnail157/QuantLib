import math
import numpy as np
from preprocessing import correlation_table
import itertools

class Portfolio:
    '''
    Portfolio Class 
    '''
    def __init__(self, securities:list=None, weights:list=None) -> None:
        self.securities = securities
        self.weights = weights
        self.correlation_table = correlation_table(securities)
        self.weights = weights

    def set_weights(self, weights:list=None) -> None:
        '''
        Sets the weight of security in the portfolio. ORDER MATTERS
        '''
        self.weights = weights

    def std(self) -> float:
        '''
        Calculates and returns the standard deviation of the portfolio

        Return Type: Float
        '''
        return np.sqrt(self.variance())
    
    def expected_return(self) -> float:
        '''
        Calculates and return the expected return of the portfolio
        '''
        expected_return = 0
        for security, weight in zip(self.securities, self.weights):
            total += security.expected_return * weight
        return expected_return
    
    def variance(self) -> float:
        '''
        Calculates and returns the variance of the portfolio

        Return Type: Float
        '''
        avg_variance = 0
        weighted_std = 2
        correlation_total = 1
        ticker_combinations = list(itertools.combinations(self.correlation_table.columns, 2))
        for ticker1, ticker2 in ticker_combinations:
            correlation_total *= (self.correlation_table.loc[ticker1,ticker2])

        for weight, security in zip(self.weights, self.securities):
            var = security.variance()
            std = security.std()
            avg_variance += (math.pow(weight, 2) * var)
            weighted_std *= (weight * std)
        
        return (avg_variance + weighted_std * correlation_total)
    
    def sharpeRatio(self, risk_free_rate:float=0) -> float:
        '''
        Calculates and returns the sharpe ratio of the portfolio given the risk free rate

        Return Type: List
        '''
        return (self.expected_return - risk_free_rate) / self.std

    def target_return(self, target_return:float=0) -> list:
        '''
        Returns the weight of each security given a target return for the portfolio

        Return Type: List
        '''
        ones = np.ones(len(target_return))
        returns = np.array([security.expected_return() for security in self.securities])
        a = np.array([returns, ones])
        b = np.array([target_return, 1.0])
        weights = np.linalg.solve(a,b)

        if not np.allclose(np.dot(a, weights), b):
            return "Something went wrong"
        return weights

    def target_beta(self, target_beta:float=0) -> list:
        '''
        Returns the weight of each security given a target return for the portfolio

        Return Type: List
        '''
        ones = np.ones(len(target_beta))
        betas = np.array([security.beta for security in self.securities])
        a = np.array([betas, ones])
        b = np.array([target_beta, 1])
        weights = np.linalg.solve(a,b)

        if not np.allclose(np.dot(a, weights), b):
            return "Something went wrong"
        return weights

    def security_info(self) -> dict:
        info = {}
        for security in self.securities:
            info[security.ticker] = {
                "Expected Return": security.expected_return(),
                "Variance": security.variance(),
                "Standard Deviation": security.std()
            }
        return info