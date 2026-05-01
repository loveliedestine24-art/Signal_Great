from flask import Flask, render_template
import bot

app = Flask(__name__)

@app.route("/")
def home():
    signals = bot.get_signals()
    return render_template("index.html", signals=signals)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
