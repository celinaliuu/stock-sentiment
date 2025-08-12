const API_BASE_URL = "http://127.0.0.1:8000";

async function getSentiment() {
    const symbol = document.getElementById("symbolInput").value.trim();
    if (!symbol) return alert("Please enter a stock symbol.");

    const response = await fetch(`${API_BASE_URL}/sentiment/${symbol}`);
    const data = await response.json();

    const resultsDiv = document.getElementById("sentimentResults");
    resultsDiv.innerHTML = "";

    data.forEach(item => {
        const el = document.createElement("p");
        el.innerText = `Headline: ${item.headline} | Sentiment: ${item.sentiment.label} (Score: ${item.sentiment.score})`;
        resultsDiv.appendChild(el);
    });
}

async function getTrend() {
    const symbol = document.getElementById("symbolInput").value.trim();
    if (!symbol) return alert("Please enter a stock symbol.");

    const response = await fetch(`${API_BASE_URL}/trend/${symbol}`);
    const data = await response.json();

    const trendDiv = document.getElementById("trendResult");
    trendDiv.innerHTML = `Average Sentiment for ${data.symbol}: ${data.average_sentiment}`;
}

