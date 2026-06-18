import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai

# .env file load karne ke liye
load_dotenv()

# Gemini API Key configuration
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is missing!")

genai.configure(api_key=API_KEY)

app = FastAPI()

# Frontend se connect karne ke liye CORS settings
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
    return {"status": "Server is running smoothly!"}

@app.post("/generate-script")
async def generate_script(request: ScriptRequest):
    try:
        # Ek badhiya sa prompt design kiya hai
        prompt = (
            f"Create a high-engaging viral Instagram Reel script.\n"
            f"Topic/Niche: {request.topic}\n"
            f"Duration: {request.duration}\n"
            f"Tone of Voice: {request.tone}\n\n"
            f"Please include visual cues (what to show on screen) and the exact voiceover text."
        )

        # YAHAN BADLAV KIYA HAI: 'models/' hata kar seedha model ka naam likha hai
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        return {"script": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))