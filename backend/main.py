import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

# API key config
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

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
    return {"status": "AI Reels Backend is Running Safely!"}

@app.post("/make-script")
async def make_script(request: TopicRequest):
    try:
        # Kuch system me 'gemini-1.5-flash' direct v1beta me error deta hai, 
        # isliye hum pure standard string formatting backup use kar rahe hain.
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Write a highly engaging 30-second Instagram Reel script about the topic: '{request.topic}'. Language: Hinglish."
            response = model.generate_content(prompt)
            return {"script": response.text}
        except Exception:
            # Alternate model name format agar pehla fail ho jaye
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"Write a highly engaging 30-second Instagram Reel script about the topic: '{request.topic}'. Language: Hinglish."
            response = model.generate_content(prompt)
            return {"script": response.text}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))