from fastapi import FastAPI
from textblob import TextBlob

app = FastAPI()

headlines = [
    "Apple stock hits all-time high",
    "Amazon announces new AI strategy",
    "Tesla faces production delays in China"
]

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











