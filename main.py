from fastapi import FastAPI
from textblob import TextBlob
import requests
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FINNHUB_API_KEY")


app = FastAPI()



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

@app.get("/health")
def health_check():
    return {"status": "ok"}

