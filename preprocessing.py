def data_preprocessing(data):
    data["PERCENT_CHANGE_CLOSE"] = data["CLOSE"].pct_change(periods=-1)*100
    select = data.loc['2024-07-15':'2023-07-15']
    return select