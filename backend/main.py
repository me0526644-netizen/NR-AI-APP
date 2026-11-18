import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(title="NR AI API")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-3.8-flash"

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)

@app.get("/api/health")
async def health():
    return {
        "ok": True,
        "gemini_configured": bool(GEMINI_API_KEY)
    }

@app.post("/api/chat")
async def chat(req: ChatRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="Gemini API key belum dikonfigurasi."
        )

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/{GEMINI_MODEL}:generateContent"
    )

    headers = {
        "x-goog-api-key": GEMINI_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "systemInstruction": {
            "parts": [{
                "text": "Kamu adalah NR AI, asisten yang ramah. "
                        "Utamakan bahasa Indonesia."
            }]
        },
        "contents": [{
            "parts": [{"text": req.message}]
        }]
    }

    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                url,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()

        reply = data["candidates"][0]["content"]["parts"][0]["text"]
        return {"reply": reply}

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Gemini mengalami error HTTP {e.response.status_code}."
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="NR AI gagal memproses permintaan."
        )

app.mount("/", StaticFiles(directory="static", html=True), name="static")
