import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# retrieve data
sp500 = yf.download("^GSPC", start = "2020-01-01", end = "2025-01-01")
# calculate MA
sp500["MA4"] = sp500["Close"].rolling(4).mean()
sp500["MA9"] = sp500["Close"].rolling(9).mean()
sp500["MA18"] = sp500["Close"].rolling(18).mean()
# signal
sp500["Signal"] = 0
sp500.loc[(sp500["MA4"] > sp500["MA9"]) & (sp500["MA9"] > sp500["MA18"]), "Signal"] = 1
sp500.loc[(sp500["MA4"] < sp500["MA9"]) & (sp500["MA9"] < sp500["MA18"]), "Signal"] = -1
# position
sp500["Position"] = sp500["Signal"].shift(1)
# calculate daily return
sp500["Return"] = sp500["Close"].pct_change()
sp500["MA_Return"] = sp500["Position"]*sp500["Return"]
# calculate cumulative return
sp500["CumReturn"] = (1 + sp500["Return"]).cumprod()
sp500["MA_CumReturn"] = (1 + sp500["MA_Return"]).cumprod()
# plot: Long run period
plt.plot(sp500.index, sp500["CumReturn"], label = "Buy & Hold", color = "red")
plt.plot(sp500.index, sp500["MA_CumReturn"], label = "4-9-18 Strategy", color = "blue")
plt.title("4-9-18 MA Strategy v.s. Buy & Hold")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.show()


# Short run period
SR_period = sp500.loc["2022-01-01":"2023-01-01"].copy()
SR_period["CumReturn"] = (1 + SR_period["Return"]).cumprod()
SR_period["MA_CumReturn"] = (1 + SR_period["MA_Return"]).cumprod()
plt.plot(SR_period.index, SR_period["CumReturn"], label = "Buy & Hold(SR)")
plt.plot(SR_period.index, SR_period["MA_CumReturn"], label = "4-9-18 Strategy(SR)")
plt.title("SR Performance")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.show()
