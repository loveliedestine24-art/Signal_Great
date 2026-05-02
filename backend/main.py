from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "API ONLINE 🚀"}

@app.get("/signal")
def signal():
    return {
        "signal": "BUY",
        "score": 85
    }
