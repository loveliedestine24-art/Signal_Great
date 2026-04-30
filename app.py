import streamlit as st
import yfinance as yf
import pandas_ta as ta
import pandas as pd
import time

# Konfigirasyon paj pwofesyonèl pou mobil
st.set_page_config(page_title="Pro Real-Market Bot", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #007bff; color: white; font-weight: bold; }
    .signal-call { padding: 25px; border-radius: 15px; background-color: #0b2e13; text-align: center; border: 3px solid #28a745; margin-bottom: 20px; }
    .signal-put { padding: 25px; border-radius: 15px; background-color: #2c0b0e; text-align: center; border: 3px solid #dc3545; margin-bottom: 20px; }
    .status-box { padding: 10px; border-radius: 8px; background-color: #1a1a1a; border: 1px solid #333; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_index=True)

st.title("📈 Real-Market Analyzer Pro")
st.write("Done Live: Forex & Mache Reyèl")

# Paramèt pou itilizatè a
assets = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "JPY=X",
    "AUD/USD": "AUDUSD=X",
    "Gold (Lò)": "GC=F"
}

col1, col2 = st.columns(2)
with col1:
    target = st.selectbox("Pè Lanjan:", list(assets.keys()))
with col2:
    tf = st.selectbox("Timeframe:", ["1m", "5m", "15m"])

def get_pro_data(ticker, interval):
    data = yf.download(ticker, period="1d", interval=interval, progress=False)
    if data.empty: return None
    
    # Kalkil Endikatè Teknik
    data['RSI'] = ta.rsi(data['Close'], length=14)
    data['EMA200'] = ta.ema(data['Close'], length=200)
    data['ATR'] = ta.atr(data['High'], data['Low'], data['Close'], length=14)
    
    # Bollinger Bands
    bbands = ta.bbands(data['Close'], length=20, std=2)
    data = pd.concat([data, bbands], axis=1)
    
    return data

if st.button("EKZEKITE ANALIZ REYÈL"):
    with st.status("Bot la ap analize mache a...", expanded=True) as status:
        df = get_pro_data(assets[target], tf)
        time.sleep(1)
        
        if df is not None:
            last = df.iloc[-1]
            price = last['Close']
            rsi = last['RSI']
            ema = last['EMA200']
            atr = last['ATR']
            lower_b = last['BBL_20_2.0']
            upper_b = last['BBU_20_2.0']
            avg_atr = df['ATR'].mean()
            
            # Detèmine Tandans
            trend = "MOUNTING 📈" if price > ema else "DESANN 📉"
            status.update(label="Analiz Fini ✅", state="complete")

            # --- VIZYÈL DASHBOARD ---
            st.markdown(f"### Pri: `{price:.5f}`")
            
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("RSI", f"{rsi:.1f}")
            col_b.metric("Tandans", trend)
            col_c.metric("Volatilite", "BON" if atr > avg_atr else "FEB")

            # --- LOJIK SIYAL PWISAN ---
            st.divider()
            
            # Siyal CALL (Achte)
            if price <= lower_b and rsi < 35 and price > ema:
                if atr > (avg_atr * 0.8): # Tcheke si gen ase mouvman
                    st.markdown(f"""<div class="signal-call">
                        <h2>🚀 SIYAL ACHTE (CALL)</h2>
                        <p>Asset: {target} | Price: {price:.5f}</p>
                        <p>Konfimasyon: Tandans an favè w + RSI Oversold</p>
                    </div>""", unsafe_allow_index=True)
                    st.balloons()
            
            # Siyal PUT (Vann)
            elif price >= upper_b and rsi > 65 and price < ema:
                if atr > (avg_atr * 0.8):
                    st.markdown(f"""<div class="signal-put">
                        <h2>📉 SIYAL VANN (PUT)</h2>
                        <p>Asset: {target} | Price: {price:.5f}</p>
                        <p>Konfimasyon: Tandans an favè w + RSI Overbought</p>
                    </div>""", unsafe_allow_index=True)
            
            else:
                st.warning("⚠️ PA GEN SIYAL KLÈ. Mache a nan zòn risk oswa volatilite a twò ba.")

            # Grafik la
            st.line_chart(df[['Close', 'EMA200']].tail(40))
            
        else:
            st.error("Mache a fèmen kounye a (Wikenn). Tounen Lendi maten!")

st.sidebar.markdown("### Règ pou siksè:")
st.sidebar.write("1. Sèlman trade si Volatilite a 'BON'.")
st.sidebar.write("2. Pa trade 5 minit anvan gwo nouvèl.")
st.sidebar.write("3. Teste siyal la sou Demo anvan.")

