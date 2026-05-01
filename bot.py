import yfinance as yf

symbols = ["EURUSD=X", "GBPUSD=X", "BTC-USD", "ETH-USD"]

def get_signal(symbol):
    try:
        data = yf.download(symbol, interval="5m", period="5d", progress=False)

        if data is None or data.empty or len(data) < 50:
            return {"symbol": symbol, "signal": "NO DATA", "price": 0}

        close = data["Close"]

        # Médias móveis
        ema_short = close.ewm(span=10).mean()
        ema_long = close.ewm(span=30).mean()

        # RSI simples (sem biblioteca externa)
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        price = close.iloc[-1]

        trend_up = ema_short.iloc[-1] > ema_long.iloc[-1]
        trend_down = ema_short.iloc[-1] < ema_long.iloc[-1]

        rsi_value = rsi.iloc[-1]

        signal = "NO SIGNAL"

        # FILTRO MAIS SEGURO
        if trend_up and rsi_value > 55:
            signal = "BUY"

        elif trend_down and rsi_value < 45:
            signal = "SELL"

        return {
            "symbol": symbol,
            "price": round(price, 5),
            "signal": signal
        }

    except:
        return {"symbol": symbol, "signal": "ERROR", "price": 0}


def get_signals():
    return [get_signal(s) for s in symbols]
