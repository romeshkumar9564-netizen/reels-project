import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# Public deployment ke liye CORS open rakhna zaroori hai
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TopicRequest(BaseModel):
    topic: str

@app.get("/")
def home():
    return {"status": "AI Reels Backend is Running Safely via REST API!"}

@app.post("/make-script")
async def make_script(request: TopicRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is missing in environment variables!")

    # Direct Google Gemini REST API Endpoint (v1beta ko bypass karke v1 stable use kar rahe hain)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Write a highly engaging 30-second Instagram Reel script about the topic: "{request.topic}".
    The content must be purely educational, focusing on tech awareness and best practices.
    Language: Hinglish (Hindi written in Roman English alphabet).
    Format the response exactly like this:
    - **HOOK**: (First 3 seconds to grab attention)
    - **BODY**: (Main valuable tips or info)
    - **CTA**: (Ask users to like and follow)
    """

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response_data.get("error", {}).get("message", "API Error"))

        # Gemini REST API se text response nikalna
        script_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
        return {"script": script_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))