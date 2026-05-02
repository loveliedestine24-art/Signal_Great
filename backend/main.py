from fastapi import FastAPI
from strategy import generate_signal

app = FastAPI()

@app.get("/signal")
def signal():
    return generate_signal()
