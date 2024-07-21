import pandas as pd

def data_preprocessing(data, start, end):
    data["PERCENT_CHANGE_CLOSE"] = data["CLOSE"].pct_change(periods=-1)*100
    select = data.loc[end:start]
    return select

def correlation_table(data, tickers):
    aggerated = {}
    for i in range(len(data)):
        df = data[i]
        aggerated[tickers[i]] = df["PERCENT_CHANGE_CLOSE"]
    combined_df = pd.DataFrame(aggerated)
    return combined_df.corr()



            