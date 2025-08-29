from fastapi import FastAPI, HTTPException
from textblob import TextBlob
import requests
import os
import datetime
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

API_KEY = os.getenv("FINNHUB_API_KEY")


app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev, you can specify specific domains later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def fetch_company_headlines(symbol):
    try:
        today = datetime.date.today().isoformat()
        url = f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from={today}&to={today}&token={API_KEY}"
        response = requests.get(url)
        news_data = response.json()
        return [item["headline"] for item in news_data[:5]]
    except requests.RequestException as e:
        logging.error(f"Error fetching news: {e}")
        return []

    




def analyze_sentiment(text):
    sentiment = TextBlob(text)
    score = sentiment.sentiment.polarity
    if score > 0:
        label = "positive"
    elif score < 0:
        label = "negative"
    else:
        label = "neutral"
    return {"label": label, "score": round(score, 3)}
    
"""
@app.get("/sentiment")
def sentiment():
    results = []
    for h in headlines:
        sentiment_result = analyze_sentiment(h)
        results.append({
            "headline": h,
            "sentiment": sentiment_result
        })
    return results
"""

@app.get("/sentiment/{symbol}")
def company_sentiment(symbol: str):
    headlines = fetch_company_headlines(symbol.upper())
    results = []
    for h in headlines:
        sentiment = analyze_sentiment(h)
        results.append({
            "headline": h,
            "sentiment": sentiment,
        })
    return results

@app.get("/trend/{symbol}")
def get_trend(symbol: str):
    
    symbol = symbol.upper()
    headlines = fetch_company_headlines(symbol)

    if not headlines:
        raise HTTPException(status_code=404, detail="Company not found")
    
    scores = []
    for headline in headlines:
        sentiment_result = analyze_sentiment(headline)
        if "score" in sentiment_result:
            scores.append(sentiment_result["score"])
            
    avg_sentiment = sum(scores) / len(scores)
    return {
        "symbol": symbol,
        "average_sentiment": round(avg_sentiment, 3)
    }

tracked_symbols = ["AAPL", "TSLA", "MSFT"]
cached_results = {}

@app.post("/update-all")
def update_all():
    results = {}

    for symbol in tracked_symbols:
        headlines = fetch_company_headlines(symbol)
        sentiments = []

        for h in headlines:
            sentiments.append(analyze_sentiment(h))

        if sentiments:
            avg_sentiment = round(
                sum(s["score"] for s in sentiments) / len(sentiments), 3
            )
        else:
            avg_sentiment = None

        results[symbol] = {
            "headlines": headlines,
            "average_sentiment": avg_sentiment
        }

    global cached_results
    cached_results = results
    print("Cache updated at", datetime.datetime.now())


@app.get("/update-all")
def manual_update_all():
    update_all()
    return cached_results

@app.get("/health")
def health_check():
    return {"status": "ok"}

scheduler = BackgroundScheduler()
scheduler.add_job(update_all, "interval", minutes=5)
scheduler.start()