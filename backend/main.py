import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
app = FastAPI(title="NR AI API", version="0.2.0")

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)

@app.get("/api/health")
async def health():
    available = False
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            r = await client.get(f"{OLLAMA_URL}/api/tags")
            available = r.status_code == 200
    except Exception:
        pass
    return {"ok": True, "ollama": available, "model": OLLAMA_MODEL}

@app.post("/api/chat")
async def chat(req: ChatRequest):
    try:
        async with httpx.AsyncClient(timeout=180) as client:
            r = await client.post(
                f"{OLLAMA_URL}/api/chat",
                json={
                    "model": OLLAMA_MODEL,
                    "messages": [
                        {"role": "system", "content": "Kamu adalah NR AI, asisten AI yang ramah. Jawab dalam bahasa yang digunakan pengguna; utamakan bahasa Indonesia."},
                        {"role": "user", "content": req.message}
                    ],
                    "stream": False
                }
            )
            r.raise_for_status()
            data = r.json()
            return {"reply": data.get("message", {}).get("content", "Tidak ada jawaban dari model.")}
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Ollama tidak aktif. Jalankan Ollama dan unduh model terlebih dahulu.")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Ollama mengembalikan status {e.response.status_code}. Pastikan model sudah diunduh.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memproses permintaan: {str(e)}")

@app.get("/")
async def home():
    return FileResponse("static/index.html")

app.mount("/", StaticFiles(directory="static", html=True), name="static")
