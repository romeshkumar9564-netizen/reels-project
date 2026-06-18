import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

# .env file load karne ke liye (Local testing ke liye zaroori hai)
load_dotenv()

app = FastAPI(title="AI Reels Script Generator Backend")

# 1. CORS Setup (Yeh sabse important hai taaki aapka Android/iOS app backend se baat kar sake)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production mein aap isko specific domains tak limit kar sakte hain
    allow_credentials=True,
    allow_methods=["*"],  # Sabhi HTTP methods (GET, POST, etc.) allow karne ke liye
    allow_headers=["*"],
)

# 2. Gemini API Configuration
# Render par hum 'GEMINI_API_KEY' naam ka environment variable set karenge
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY nahi mila! Render Environment Variables mein add karein.")
else:
    genai.configure(api_key=GEMINI_API_KEY)

# Frontend se aane waale data ka structure (Schema)
class ScriptRequest(BaseModel):
    topic: str
    duration: str = "30 Seconds"
    tone: str = "Energetic & Aggressive"

# 3. Health Check Route (UptimeRobot/Cron-job isi route ko ping karega server jagane ke liye)
@app.get("/")
def home():
    return {"status": "healthy", "message": "AI Reels Script Generator Backend is Running!"}

# 4. Main Script Generation Route
@app.post("/generate-script")
async def generate_script(request: ScriptRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="API Key configured nahi hai server par.")
    
    try:
        # Prompt engineering: Jo preferences user select karega uske mutabik prompt banega
        prompt = f"Create a highly engaging {request.duration} Instagram Reel script on the topic: '{request.topic}'. The tone should be {request.tone}. The script must be in Hinglish, with clear visual cues and voiceover text formatted nicely."
        
        # Gemini 1.5 Flash model call (Fast aur cost-effective hai)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        return {"script": response.text}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Script generate karne mein dikkat aayi: {str(e)}")

# 5. Render/Production Dynamic Port Handling
if __name__ == "__main__":
    import uvicorn
    # Render automatically ek PORT assign karta hai, agar na mile toh default 8000 use hoga
    port = int(os.environ.get("PORT", 8000))
    # host '0.0.0.0' hona compulsory hai Render par deploy karne ke liye
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)