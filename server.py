from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import Response
from portfolio import Portfolio
import math
import os
from dotenv import load_dotenv
from fred import FredAPI
from alpha import AlphaVantage
from equity import Equity
from preprocessing import data_preprocessing
#import psycopg2

load_dotenv()
app = Flask(__name__)


valid_data_source = ["Alpha Vantage"]

# KEYS
db_url = os.getenv("RENDER_POSTGRES_URL")
FREDAPI_KEY = os.getenv("FRED")
ALPHAVANTAGE_KEY = os.getenv("ALPHAVANTAGE")

# Create API Instances
# db_url = os.getenv("RENDER_POSTGRES_URL")
# db = psycopg2.connect(db_url)

# if db:
#     print("Connection is Established")
# else:
#     print("No Connection Made")

fred = FredAPI(FREDAPI_KEY)
alphaVantage = AlphaVantage(ALPHAVANTAGE_KEY)

@app.route('/')
def main():
    return render_template("dashboard/dashboard.html")

@app.get("/calculate")
def calculate():
    data = request.get_json()
    save = data["metadata"]["save"]
    end_date = data["metadata"]["end_date"]
    start_date = data["metadata"]["start_date"]
    tickers = []
    securities = []
    total_weights = 0

    for row in data["data"]:
        ticker = row["Ticker"]
        weight = float(row["Weight"])
        source = row["Source"]

        # Check if ticker value is valid
        if ticker:
            pass

        # Check if Data Source can be supported
        if source not in valid_data_source:
            return Response("{'error':'Data Source not supported'}", status=400, mimetype='application/json')

        total_weights += weight
        tickers.append(ticker)

        raw_security_data = alphaVantage.daily(ticker)
        equity_data = data_preprocessing(raw_security_data, start_date, end_date)

        info = {
            "raw_data": equity_data,
            "ticker": ticker,
        }

        securities.append(Equity(info))

    # Check total Weight of portfolio
    if total_weights != 100:
        return Response("{'error':'Weights do not total to 100%'}", status=400, mimetype='application/json')
    

    port = Portfolio(securities)
    daily_expected_return = port.cal_expected_return()
    monthly_expexted_return = daily_expected_return * 21
    quarterly_expected_return = daily_expected_return * 63
    yearly_expected_return = daily_expected_return * 252

    port_std = port.cal_std()
    print(port_std * math.sqrt(252))
    
    new_weights = port.target_return(12)
    port.set_weights(new_weights)

    res = {
        "daily": daily_expected_return,
        "monthly": monthly_expexted_return,
        "quarterly": quarterly_expected_return,
        "yearly": yearly_expected_return,
        "weights": new_weights
    }

    return Response(f"{res}", status=200, mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True)