from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
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


# POST endpoint (main one)
@app.post("/sentiment")
def sentiment_post(data: SentimentRequest):

    results = []

    for sentence in data.sentences:
        results.append({
            "sentence": sentence,
            "sentiment": classify(sentence)
        })

    return {"results": results}


# GET endpoint to prevent 405 error
@app.get("/sentiment")
def sentiment_get():
    return {"message": "Use POST with sentences array"}
