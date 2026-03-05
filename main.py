from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import re

app = FastAPI()

class SentimentRequest(BaseModel):
    sentences: List[str]

positive_words = [
    "love","great","good","amazing","awesome","happy","excellent",
    "fantastic","wonderful","like","best","nice","enjoy"
]

negative_words = [
    "bad","terrible","hate","awful","worst","sad","angry",
    "horrible","disappointed","poor","annoying"
]

def classify(text):
    text_lower = text.lower()

    if any(word in text_lower for word in positive_words):
        return "happy"

    if any(word in text_lower for word in negative_words):
        return "sad"

    return "neutral"


@app.post("/sentiment")
def batch_sentiment(data: SentimentRequest):

    results = []

    for sentence in data.sentences:
        sentiment = classify(sentence)

        results.append({
            "sentence": sentence,
            "sentiment": sentiment
        })

    return {"results": results}
