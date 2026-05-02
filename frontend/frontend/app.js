const API = "https://SEU-RENDER.onrender.com/market";

async function loadData() {

    const pair = document.getElementById("pair").value;
    const tf = document.getElementById("tf").value;

    const res = await fetch(`${API}?symbol=${pair}&interval=${tf}`);
    const data = await res.json();

    document.getElementById("signal").innerText = data.signal;
    document.getElementById("price").innerText = "Price: " + data.price;
    document.getElementById("score").innerText = "Score: " + data.score;
    document.getElementById("trend").innerText = "Trend: " + data.trend;
}

setInterval(loadData, 5000);
