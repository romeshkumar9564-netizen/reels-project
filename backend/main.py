import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types

# API key system environment se uthayi jaati hai taaki chori na ho
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

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
    prompt = f"""
    Write a highly engaging 30-second Instagram Reel script about the topic: "{request.topic}".
    The content must be purely educational, focusing on tech awareness and best practices.
    Language: Hinglish (Hindi written in Roman English alphabet).
    Format the response exactly like this:
    - **HOOK**: (First 3 seconds to grab attention)
    - **BODY**: (Main valuable tips or info)
    - **CTA**: (Ask users to like and follow)
    """
    try:
        safety = [
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_NONE,
            ),
        ]
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(safety_settings=safety)
        )
        return {"script": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))