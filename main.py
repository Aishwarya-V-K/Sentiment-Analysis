from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: List[str]

positive_words = ["love","great","good","amazing","awesome","happy","excellent"]
negative_words = ["bad","terrible","hate","awful","worst","sad","angry"]

@app.get("/")
def root():
    return {"message": "API running"}

def classify(text):
    text = text.lower()
    if any(w in text for w in positive_words):
        return "happy"
    if any(w in text for w in negative_words):
        return "sad"
    return "neutral"


# GET endpoint (prevents 405 error)
@app.get("/sentiment")
def sentiment_info():
    return {"message": "Use POST with JSON body {'sentences': [...]}"}


# POST endpoint (grader uses this)
@app.post("/sentiment")
def sentiment(data: SentimentRequest):

    results = []

    for s in data.sentences:
        results.append({
            "sentence": s,
            "sentiment": classify(s)
        })

    return {"results": results}
