import os
import json
import subprocess
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

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
    return {"status": "Backend is active"}

@app.post("/make-script")
async def make_script(request: TopicRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API Key missing on Render!")

    prompt = f"Write a highly engaging 30-second Instagram Reel script about the topic: '{request.topic}'. Language: Hinglish. Format with clear HOOK, BODY, and CTA."

    # Google AI Studio Custom Command Line Safe Payload
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    # Direct System Bypass Request (Official cURL implementation via Python)
    command = [
        "curl",
        "-X", "POST",
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload)
    ]

    try:
        # Executing direct secure shell command on Render
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        res_data = json.loads(result.stdout)
        
        script_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
        return {"script": script_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google Gateway Network Error: {str(e)}")