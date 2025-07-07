import yfinance as yf
import pandas as pd

def get_data(ticker, start_date, end_date):
    """
    Fetch historical stock data from Yahoo Finance.

    Parameters:
    ticker (str): Stock ticker symbol.
    start_date (str): Start date in 'YYYY-MM-DD' format.
    end_date (str): End date in 'YYYY-MM-DD' format.

    Returns:
    pd.DataFrame: DataFrame containing the stock data.
    """
    df = yf.download(ticker, start=start_date, end=end_date)
    df.reset_index(inplace=True)
    return df