import os
import uuid
import time
import threading
import subprocess
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import FileResponse
from pydantic import BaseModel

# ================= CONFIG ================= #

API_KEY = os.getenv("API_KEY")

DOWNLOAD_DIR = "/tmp"
DELETE_AFTER_SECONDS = 900  # 15 minutes

# ========================================== #

app = FastAPI(
    title="CAPTAIN Multi Video Downloader API",
    description="Public Video Downloader API | Credit: @CAPTAINPAPAJI",
    version="1.0.0"
)

class DownloadRequest(BaseModel):
    url: str
    quality: str = "best"

# ---------- Auto delete file ---------- #
def auto_delete(path: str):
    time.sleep(DELETE_AFTER_SECONDS)
    if os.path.exists(path):
        os.remove(path)

# ---------- Download endpoint ---------- #
@app.post("/download")
def download_video(
    data: DownloadRequest,
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    file_id = str(uuid.uuid4())
    output_template = f"{DOWNLOAD_DIR}/{file_id}.%(ext)s"

    cmd = [
        "yt-dlp",
        "--js-runtime", "deno",
        "-f", data.quality,
        "-o", output_template,
        data.url
    ]

    try:
        subprocess.run(cmd, check=True)
    except Exception:
        raise HTTPException(status_code=400, detail="Download failed")

    filename = next(
        (f for f in os.listdir(DOWNLOAD_DIR) if file_id in f),
        None
    )

    if not filename:
        raise HTTPException(status_code=500, detail="File not found")

    file_path = f"{DOWNLOAD_DIR}/{filename}"

    threading.Thread(
        target=auto_delete,
        args=(file_path,),
        daemon=True
    ).start()

    return {
        "status": "success",
        "file": filename,
        "file_url": f"https://YOUR_API_DOMAIN/file/{filename}",
        "credit": "@CAPTAINPAPAJI"
    }

# ---------- File serve endpoint ---------- #
@app.get("/file/{filename}")
def serve_file(filename: str):
    path = f"{DOWNLOAD_DIR}/{filename}"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File expired or not found")

    return FileResponse(
        path,
        media_type="video/mp4",
        filename=filename
    )

