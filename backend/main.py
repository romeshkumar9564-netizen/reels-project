import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types

app = FastAPI()

# CORS configuration for stable frontend communication
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

    try:
        # Initializing the official production client
        client = genai.Client(api_key=api_key)
        
        prompt = f"Write a 30-second Instagram Reel script about the topic: '{request.topic}'. Language: Hinglish."
        
        # Using the official standard model call
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
        )
        
        if response.text:
            return {"script": response.text}
        else:
            raise HTTPException(status_code=500, detail="Google returned an empty response.")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google API Official Error: {str(e)}")