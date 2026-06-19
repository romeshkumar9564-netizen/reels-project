import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_model  # env file load karne ke liye (agar use kar rahe ho)

load_dotenv()

# API Key ko secure tarike se read karna (Render environment variable se)
# Agar local pe check kar rahe ho toh yahan direct apni key string bhi daal sakte ho: "AQ.Ab8RN6...""
API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6Jz2At2SRyPGmbG74QYUXiuNnzFtCAP9jG48HMEvvQJ3A")

# Purane SDK (google-generativeai) ke hisab se configure karein
genai.configure(api_key=API_KEY)

app = FastAPI()

# Frontend connectivity ke liye CORS Middleware
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
        
        # Purane SDK ke tarike se Gemini model initialize karein
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