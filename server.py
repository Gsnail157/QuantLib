from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import Response
from portfolio import Portfolio
import math

app = Flask(__name__)

valid_data_source = ["Alpha Vantage"]

@app.route('/')
def main():
    return render_template("dashboard/dashboard.html")

@app.get("/calculate")
def calculate():
    data = request.get_json()
    save = data["metadata"]["save"]

    total_weights = 0

    for row in data["data"]:
        ticker = row["Ticker"]
        weight = row["Weight"]
        source = row["Source"]

        # Check if ticker value is valid
        if ticker:
            pass

        # Check if Data Source can be supported
        if source not in valid_data_source:
            return Response("{'error':'Data Source not supported'}", status=400, mimetype='application/json')

        total_weights += weight

    # Check total Weight of portfolio
    if total_weights != 100:
        return Response("{'error':'Weights do not total to 100%'}", status=400, mimetype='application/json')
        
    info = Portfolio(data)
    daily_expected_return = info.cal_expected_return()
    monthly_expexted_return = daily_expected_return * 21
    quarterly_expected_return = daily_expected_return * 63
    yearly_expected_return = daily_expected_return * 252

    port_std = info.cal_std()
    print(port_std * math.sqrt(252))

    res = {
        "daily": daily_expected_return,
        "monthly": monthly_expexted_return,
        "quarterly": quarterly_expected_return,
        "yearly": yearly_expected_return
    }

    return Response(f"{res}", status=200, mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True)