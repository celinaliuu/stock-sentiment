from fastapi import FastAPI
from textblob import TextBlob
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FINNHUB_API_KEY")

app = FastAPI()



def fetch_headlines():
    url = f"https://finnhub.io/api/v1/news?category=general&token={API_KEY}"
    response = requests.get(url)
    news_data = response.json()
    return [item["headline"] for item in news_data[:5]]


headlines = fetch_headlines()

def analyze_sentiment(text):
    sentiment = TextBlob(text)
    score = sentiment.sentiment.polarity
    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    else:
        return "neutral"
    
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


