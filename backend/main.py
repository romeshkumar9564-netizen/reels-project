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
        # Naya model initialization aur generate format
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Write a highly engaging 30-second Instagram Reel script about the topic: "{request.topic}".
        The content must be purely educational, focusing on tech awareness and best practices.
        Language: Hinglish (Hindi written in Roman English alphabet).
        Format the response exactly like this:
        - **HOOK**: (First 3 seconds to grab attention)
        - **BODY**: (Main valuable tips or info)
        - **CTA**: (Ask users to like and follow)
        """
        
        response = model.generate_content(prompt)
        return {"script": response.text}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))