from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class SentimentRequest(BaseModel):
    sentences: List[str]

positive = ["love","great","good","amazing","awesome","happy","excellent"]
negative = ["bad","terrible","hate","awful","worst","sad","angry"]

@app.get("/")
def root():
    return {"message": "API is running"}

def classify(text):
    text = text.lower()

    if any(w in text for w in positive):
        return "happy"

    if any(w in text for w in negative):
        return "sad"

    return "neutral"


@app.post("/sentiment")
def sentiment(data: SentimentRequest):

    results = []

    for sentence in data.sentences:
        results.append({
            "sentence": sentence,
            "sentiment": classify(sentence)
        })

    return {"results": results}
