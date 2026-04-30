import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Konfigirasyon paj
st.set_page_config(page_title="Trading Analyzer", layout="centered")

# Ranje erè 'unsafe_allow_html' la isit la
st.markdown("""<style>.stApp { background-color: #050505; color: white; } .signal-call { padding: 20px; border-radius: 10px; background-color: #0b2e13; border: 2px solid #28a745; text-align: center; font-weight: bold; } .signal-put { padding: 20px; border-radius: 10px; background-color: #2c0b0e; border: 2px solid #dc3545; text-align: center; font-weight: bold; }</style>""", unsafe_allow_html=True)

st.title("📈 Analizè Mache Live")

assets = {"EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "USD/JPY": "JPY=X", "Gold": "GC=F"}
target = st.selectbox("Pè Lanjan:", list(assets.keys()))
tf = st.selectbox("Timeframe:", ["1m", "5m", "15m"])

def calculate_indicators(df):
    # RSI Manyèl
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Bollinger Manyèl
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['STD'] = df['Close'].rolling(window=20).std()
    df['Upper'] = df['MA20'] + (df['STD'] * 2)
    df['Lower'] = df['MA20'] - (df['STD'] * 2)
    
    # EMA 200
    df['EMA200'] = df['Close'].ewm(span=200, adjust=False).mean()
    return df

if st.button("EKZEKITE ANALIZ"):
    with st.spinner("Analiz an kous..."):
        data = yf.download(assets[target], period="1d", interval=tf, progress=False)
        if not data.empty:
            df = calculate_indicators(data)
            last = df.iloc[-1]
            
            st.metric("Pri Live", f"{last['Close']:.5f}")
            
            # Lojik Siyal
            if last['Close'] <= last['Lower'] and last['RSI'] < 35 and last['Close'] > last['EMA200']:
                st.markdown('<div class="signal-call">🚀 SIYAL ACHTE (CALL)</div>', unsafe_allow_html=True)
            elif last['Close'] >= last['Upper'] and last['RSI'] > 65 and last['Close'] < last['EMA200']:
                st.markdown('<div class="signal-put">📉 SIYAL VANN (PUT)</div>', unsafe_allow_html=True)
            else:
                st.warning("Pa gen siyal solid kounye a.")
                
            st.line_chart(df[['Close', 'EMA200']].tail(50))
        else:
            st.error("Done pa disponib. Tcheke si mache a ouvè.")
