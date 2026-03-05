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

positive_words = [
    "love","great","good","amazing","awesome","happy","excellent",
    "fantastic","wonderful","like","best","nice","enjoy"
]

negative_words = [
    "bad","terrible","hate","awful","worst","sad","angry",
    "horrible","disappointed","poor","annoying"
]

@app.get("/")
def root():
    return {"message": "API is running"}

def classify(text):
    text = text.lower()

    if any(word in text for word in positive_words):
        return "happy"

    if any(word in text for word in negative_words):
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
