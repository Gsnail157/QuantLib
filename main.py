from dotenv import load_dotenv
import os
from alpha import AlphaVantage
import matplotlib.pyplot as plt

def main():
    # LOAD API KEYS
    load_dotenv()
    key = os.getenv('ALPHAVANTAGE')

    alpha = AlphaVantage(key)
    data = alpha.daily("IBM")
    print(data)
    return

if __name__ == '__main__':
    main()