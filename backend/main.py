import os
import json
import urllib.request
import ssl
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

    # Google Gemini 1.5 Flash - Nayi Key ke liye v1beta endpoint mandatory hai
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = f"Write a highly engaging 30-second Instagram Reel script about the topic: '{request.topic}'. Language: Hinglish. Format it with clearly marked HOOK, BODY, and CTA."

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    data = json.dumps(payload).encode("utf-8")
    
    # SSL Bypass aur Cloud Environment standard headers
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(
        url, 
        data=data, 
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }, 
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            script_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
            return {"script": script_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google API Error: {str(e)}")