import os
import uuid
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# =========================================================
#   🚀 Multi Video Downloader API
#   👑 Powered by @CAPTAINPAPAJI
# =========================================================

app = FastAPI(
    title="𝘾𝘼𝙋𝙏𝘼𝙄𝙉 𝙈𝙐𝙇𝙏𝙄 𝙑𝙄𝘿𝙀𝙊 𝘿𝙊𝙒𝙉𝙇𝙊𝘼𝘿𝙀𝙍 𝘼𝙋𝙄",
    description="YouTube | Facebook | Instagram | Twitter | Snapchat\nCredit: @CAPTAINPAPAJI",
    version="1.0.0"
)

DOWNLOAD_DIR = "/tmp"

class DownloadRequest(BaseModel):
    url: str
    quality: str = "best"

@app.get("/")
def home():
    return {
        "status": "API Running",
        "credit": "@CAPTAINPAPAJI",
        "supported": ["YT", "FB", "IG", "TWITTER", "SNAPCHAT"]
    }

@app.post("/download")
def download_video(data: DownloadRequest):
    video_id = str(uuid.uuid4())
    output = f"{DOWNLOAD_DIR}/{video_id}.%(ext)s"

    command = ["yt-dlp", "-f", data.quality, "-o", output, data.url]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=400, detail="Download failed")

    for file in os.listdir(DOWNLOAD_DIR):
        if video_id in file:
            return {
                "status": "success",
                "file": file,
                "credit": "@CAPTAINPAPAJI"
            }

    raise HTTPException(status_code=500, detail="File not found")
