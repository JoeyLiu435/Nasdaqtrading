import yfinance as yf
import pandas as pd


#get all tickers from nasdaqlisted.txt
tickers = []

with open('nasdaqlisted.txt', 'r') as file:
    for line in file:
        ticker = line.split('|')[0].strip()
        tickers.append(ticker)

tickers.remove('Symbol')

start_date = '2010-01-01'
end_date = '2025-07-01'

#download data and save as csv files
for ticker in tickers:
    try:
        data = yf.download(ticker,start_date,end_date)
        data.to_csv(f'./nasdaq/{ticker}.csv')
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")