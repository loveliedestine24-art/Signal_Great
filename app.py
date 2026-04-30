import streamlit as st
import yfinance as yf
import pandas as pd

st.title("Analizè Trading")

symbol = st.selectbox("Chwazi Lajan:", ["EURUSD=X", "GBPUSD=X", "JPY=X"])

if st.button("Analize"):
    df = yf.download(symbol, period="1d", interval="1m")
    if not df.empty:
        st.write(f"Pri Kounye a: {df['Close'].iloc[-1]}")
        st.line_chart(df['Close'].tail(20))
        
        # Lojik senp
        avg = df['Close'].mean()
        if df['Close'].iloc[-1] < avg:
            st.success("Siyal: CALL (Pri a ba)")
        else:
            st.error("Siyal: PUT (Pri a wo)")
