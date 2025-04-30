from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tempfile
import os
from utils import align_audio_with_text

app = FastAPI()

# Allow frontend (e.g. Streamlit) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/align")
async def align(audio: UploadFile, transcript: str = Form(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
        tmp_audio.write(await audio.read())
        audio_path = tmp_audio.name

    segments = align_audio_with_text(audio_path, transcript)
    os.remove(audio_path)

    return JSONResponse(content={"segments": segments})
