def clean_data(df):
    df = df.reset_index()
    df = df[['Date', 'Open', 'Close', 'High', 'Low', 'Volume']]
    return df