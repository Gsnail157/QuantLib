from dotenv import load_dotenv
import os
from alpha import AlphaVantage
from equity import Equity
from preprocessing import data_preprocessing

def main():
    # LOAD API KEYS
    load_dotenv()
    key = os.getenv('ALPHAVANTAGE')

    alpha = AlphaVantage(key)
    ibm_data = alpha.daily("IBM")
    tsla_data = alpha.daily("TSLA")
    aapl_data = alpha.daily("AAPL")

    data = [ibm_data, tsla_data, aapl_data]
    equities = []

    for ticker in data:
        processed = data_preprocessing(ticker)
        equity = Equity(processed)
        equities.append(equity)
    
    weights = [50, 25, 25]

    for stock in equities:
        print(stock.std)


    return

if __name__ == '__main__':
    main()