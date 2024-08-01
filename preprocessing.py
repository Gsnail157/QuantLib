import pandas as pd

def data_preprocessing(data, start, end):
    data["PERCENT_CHANGE_CLOSE"] = data["CLOSE"].pct_change(periods=-1)*100
    select = data.loc[end:start]
    return select

def correlation_table(securities:list=None):
    '''
    Creates a correlation table for each security provided

    Return Type: Pandas DataFrame
    '''
    aggerated = {}
    for security in securities:
        df = security.raw_data
        aggerated[security.ticker] = df["PERCENT_CHANGE_CLOSE"]
    combined_df = pd.DataFrame(aggerated)
    return combined_df.corr()

            