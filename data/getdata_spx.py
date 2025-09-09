import yfinance as yf

spx = yf.download('^GSPC', start='2010-01-01', end='2025-07-01')

spx.to_csv('./data/SPX.csv')