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

genai.configure(api_key=API_KEY)

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

        # AGAR RECENT GOOGLE PACKAGES HAIN TOH YEH BINAMODELS/ KE CHALEGA
        # LEKIN SAFETY KE LIYE HUM DIRECT GENERATE_CONTENT USE KAR RAHE HAIN
        response = genai.generate_text(
            model="models/text-bison-001" if "text" in request.topic else "models/gemini-1.5-flash",
            prompt=prompt
        ) if hasattr(genai, 'generate_text') else None

        if not response:
            # Agar purana library configuration hai, toh bina 'models/' ya sirf model string try karte hain
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
        
        return {"script": response.text}

    except Exception as e:
        # AGAR FIR BHI ERROR AAYE TOH DIRECT STRING SE TRY KAREIN
        try:
            # Yeh aakhiri brahmastra hai bina kisi library validation ke
            import requests
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            payload = {"contents": [{"parts":[{"text": prompt}]}]}
            res = requests.post(url, json=payload)
            return {"script": res.json()['candidates'][0]['content']['parts'][0]['text']}
        except:
            raise HTTPException(status_code=500, detail=str(e))