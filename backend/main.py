import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv  # Yeh ekdum sahi line hai!

# .env file se variables load karne ke liye
load_dotenv()

# API Key ko Render environment variable se read karna
API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6Jz2At2SRyPGmbG74QYUXiuNnzFtCAP9jG48HMEvvQJ3A")

# Gemini SDK ko configure karein
genai.configure(api_key=API_KEY)

app = FastAPI()

# Android App aur Website dono se connect karne ke liye CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend se aane wale data ka structure
class ScriptRequest(BaseModel):
    topic: str
    duration: str
    tone: str

@app.get("/")
def home():
    return {"status": "Server is running smoothly on Render!"}

@app.post("/generate-script")
async def generate_script(request: ScriptRequest):
    try:
        # Prompt taiyar karein
        prompt = (
            f"Write a short video/reel script on the topic: '{request.topic}'. "
            f"The duration should be around {request.duration} and the tone of the "
            f"script should be {request.tone}. Make it engaging and ready for social media."
        )
        
        # Gemini model initialize karein
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        if not response.text:
            raise HTTPException(status_code=500, detail="Failed to generate content from Gemini.")
            
        return {
            "success": True,
            "topic": request.topic,
            "script": response.text
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))