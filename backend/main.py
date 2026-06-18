import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is missing!")

# Yahan humne api_version ko explicit 'v1' set kiya hai taaki v1beta ka lafda khatam ho
genai.configure(api_key=API_KEY, transport='rest')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        prompt = (
            f"Create a high-engaging viral Instagram Reel script.\n"
            f"Topic/Niche: {request.topic}\n"
            f"Duration: {request.duration}\n"
            f"Tone of Voice: {request.tone}\n\n"
            f"Please include visual cues and the exact voiceover text."
        )

        # Direct REST API call (Brahmastra) jo Google ke rules ko bypass karega
        import requests
        # v1beta ki jagah hum direct v1 stable use kar rahe hain jahan gemini-1.5-flash standard hai
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        payload = {"contents": [{"parts":[{"text": prompt}]}]}
        
        res = requests.post(url, json=payload)
        res_data = res.json()

        if "candidates" in res_data:
            script_text = res_data['candidates'][0]['content']['parts'][0]['text']
            return {"script": script_text}
        else:
            # Fallback agar koi dikkat aaye
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return {"script": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))