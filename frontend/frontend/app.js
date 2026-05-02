fetch("https://SEU-LINK.onrender.com/signal")
.then(res => res.json())
.then(data => {
  document.getElementById("signal").innerText =
    data.signal + " - " + data.score;
});
