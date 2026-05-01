import yfinance as yf
import ta

symbols = ["EURUSD=X", "GBPUSD=X", "BTC-USD", "ETH-USD"]

def analyze(symbol):
    data = yf.download(symbol, interval="1m", period="1d")

    if data.empty:
        return {"symbol": symbol, "signal": "NO DATA", "price": 0, "rsi": 0}

    data["ema50"] = ta.trend.ema_indicator(data["Close"], window=50)
    data["ema200"] = ta.trend.ema_indicator(data["Close"], window=200)
    data["rsi"] = ta.momentum.rsi(data["Close"], window=14)

    last = data.iloc[-1]

    trend_up = last["ema50"] > last["ema200"]
    trend_down = last["ema50"] < last["ema200"]

    signal = "NO SIGNAL"

    if trend_up and last["rsi"] > 55:
        signal = "BUY"
    elif trend_down and last["rsi"] < 45:
        signal = "SELL"

    return {
        "symbol": symbol,
        "price": round(last["Close"], 5),
        "signal": signal,
        "rsi": round(last["rsi"], 2)
    }


def get_signals():
    return [analyze(s) for s in symbols]
