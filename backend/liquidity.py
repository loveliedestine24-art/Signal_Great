def detect_liquidity_sweep(candles):

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    last_close = candles[-1]["close"]

    recent_high = max(highs[:-1])
    recent_low = min(lows[:-1])

    return {
        "sweep_high": last_close > recent_high,
        "sweep_low": last_close < recent_low
    }
