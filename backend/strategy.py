from candles import get_candles
from liquidity import detect_liquidity_sweep

def generate_signal():
    return {
        "signal": "BUY",
        "score": 85
    }
