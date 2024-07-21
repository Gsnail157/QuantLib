from dotenv import load_dotenv
import os
from alpha import AlphaVantage
from equity import Equity
from preprocessing import data_preprocessing, correlation_table
import itertools

def main():
    # LOAD API KEYS
    load_dotenv()
    key = os.getenv('ALPHAVANTAGE')

    alpha = AlphaVantage(key)
    ibm_data = alpha.daily("IBM")
    tsla_data = alpha.daily("TSLA")
    aapl_data = alpha.daily("AAPL")
    tickers = ["IBM", "TSLA", "AAPL"]
    data = [ibm_data, tsla_data, aapl_data]
    processed_data = []
    equities = []
    start_date = "2020-07-19"
    end_date = "2024-07-19"

    for ticker in data:
        processed = data_preprocessing(ticker, start_date, end_date)
        processed_data.append(processed)
        equity = Equity(processed)
        equities.append(equity)
    
    table = correlation_table(processed_data, tickers)
    print(table)
    print(table.values.flatten().prod())
    ticker_combinations = list(itertools.combinations(table.columns, 2))
    print(ticker_combinations)
    weights = [50, 25, 25]

    for stock in equities:
        print(stock.avg_expected_return)


    return

if __name__ == '__main__':
    main()