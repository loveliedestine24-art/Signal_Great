from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from candles import get_candles
from liquidity import detect_liquidity_sweep

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/market")
def market(symbol: str = "BTCUSDT", interval: str = "1m"):

    candles = get_candles(symbol, interval)
    liquidity = detect_liquidity_sweep(candles)

    price = candles[-1]["close"]

    if liquidity["sweep_low"]:
        signal = "BUY 🔵"
        score = 90
        trend = "BULLISH"
    elif liquidity["sweep_high"]:
        signal = "SELL 🔴"
        score = 88
        trend = "BEARISH"
    else:
        signal = "NO TRADE ⚪"
        score = 40
        trend = "RANGE"

    return {
        "symbol": symbol,
        "price": price,
        "signal": signal,
        "score": score,
        "trend": trend
    }
