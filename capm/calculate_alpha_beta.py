import pandas as pd
import statsmodels.api as sm
import glob
import os

data_folder = "/Users/liuzongyu18/Nasdaqtrading/cleaned_data/nasdaq"
spx_path = "/Users/liuzongyu18/Nasdaqtrading/cleaned_data/SPX.csv"
returns_out = "/Users/liuzongyu18/Nasdaqtrading/capm/returns"
os.makedirs(returns_out, exist_ok=True)

spx = pd.read_csv(spx_path, parse_dates=['Date'])

def get_returns(df):
    """Calculate percentage returns for each column."""
    return df.pct_change().dropna()

def calculate_alpha_beta(returns):
    """Run OLS regression: nasdaq_Close ~ const + SPX_Close."""
    X = sm.add_constant(returns["SPX_Close"])
    y = returns["nasdaq_Close"]
    model = sm.OLS(y, X).fit()
    beta = model.params["SPX_Close"]
    alpha = model.params["const"]
    return alpha, beta, model

parameters = pd.DataFrame(columns=['Alpha', 'Beta'])

files = glob.glob(data_folder.rstrip("/") + "/*.csv")

for file in files:
    ticker = os.path.basename(file).replace(".csv", "")
    nasdaq = pd.read_csv(file, parse_dates=['Date'])

    if "Close" not in nasdaq.columns:
        print(f"Skipping {ticker}: no Close column")
        continue

    df = pd.DataFrame({
        "nasdaq_Close": nasdaq["Close"],
        "SPX_Close": spx["Close"]
    })

    returns = get_returns(df)

    try:
        alpha, beta, model = calculate_alpha_beta(returns)
    except Exception as e:
        print(f"Error in {ticker}: {e}")
        continue

    returns["Prediction"] = alpha + beta * returns["SPX_Close"]
    returns["Residual"] = returns["nasdaq_Close"] - returns["Prediction"]
    returns["Excess"] = returns["nasdaq_Close"] - beta * returns["SPX_Close"]

    out_path = f"{returns_out}/{ticker}.csv"
    returns.to_csv(out_path, index=False)
    print(f"Saved returns for {ticker}: {out_path}")

    parameters.loc[ticker] = [alpha, beta]

parameters.to_csv("/Users/liuzongyu18/Nasdaqtrading/capm/parameters.csv")
print(f"\nSaved parameters summary to {returns_out}/parameters.csv")
