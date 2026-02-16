from fastapi import FastAPI
import yfinance as yf
import pandas_ta as ta

app = FastAPI()

def analyze_pair(pair):
    df = yf.download(pair, interval="15m", period="5d")

    df["EMA200"] = ta.ema(df["Close"], length=200)
    df["RSI"] = ta.rsi(df["Close"], length=14)

    last = df.iloc[-1]

    score = 0
    max_score = 4

    if last["Close"] > last["EMA200"]:
        score += 2

    if last["RSI"] > 50:
        score += 2

    confidence = (score / max_score) * 100

    return {
        "pair": pair,
        "confidence": round(confidence, 2)
    }

@app.get("/analyze/{pair}")
def analyze(pair: str):
    return analyze_pair(pair)
