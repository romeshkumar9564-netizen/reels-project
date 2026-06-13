import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

# 1. FastAPI Initialize karna
app = FastAPI()

# 2. CORS Middleware configure karna (Yeh aapke iPhone ke red error ko theek karega)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Sabhi origins se requests allow karne ke liye
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Gemini API Key set karna (Render Environment variables se uthayega)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    # Agar Render par config nahi kiya, toh yahan apna key backup me rakh sakte hain
    GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

genai.configure(api_key=GEMINI_API_KEY)

# 4. Request Body ke liye Pydantic Model (Jo Frontend se topic aayega)
class TopicRequest(BaseModel):
    topic: str

# 5. Live Generate Endpoint
@app.post("/generate")
async def generate_reels_script(request: TopicRequest):
    try:
        # Prompt ko viral aur engaging banane ke liye design kiya hai
        prompt = (
            f"Write a highly engaging 30-second Instagram Reel/Shorts script about: '{request.topic}'. "
            f"The language must be Hinglish (Hindi written in English alphabets) so it connects easily with the Indian audience. "
            f"Include an eye-catching HOOK at the beginning, an informative BODY in the middle, and a clear Call To Action (CTA) or safety tip at the end."
        )
        
        # Gemini Model call karna
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        
        if not response.text:
            raise HTTPException(status_code=500, detail="Gemini didn't return any text.")
            
        # Frontend ko 'script' key ke andar response bhejna
        return {"script": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 6. Health Check Endpoint (Render ko active rakhne ke liye)
@app.get("/")
def read_root():
    return {"status": "Server is running perfectly Raja Bhai! 🚀"}