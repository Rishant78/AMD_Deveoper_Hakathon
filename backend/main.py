from fastapi import FastAPI, UploadFile, File
from backend.video import get_video_info
from backend.video import extract_frames
from backend.pipeline import process_video
import shutil
import os

app = FastAPI(
    title="AMD Video Captioning API",
    version="1.0.0"
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Stores the most recently uploaded video
latest_uploaded_video = None


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "AMD Video Captioning API 🚀"
    }


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    global latest_uploaded_video

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    latest_uploaded_video = file_path

    return {
        "filename": file.filename,
        "saved_to": file_path,
        "message": "Video uploaded successfully!"
    }


@app.post("/extract")
async def extract():

    global latest_uploaded_video

    if latest_uploaded_video is None:
        return {
            "error": "No video uploaded yet."
        }

    result = extract_frames(latest_uploaded_video)

    return {
        "video": latest_uploaded_video,
        "frames_extracted": result["frames"],
        "blurred_frames": result["blurred_frames"],
        "output_folder": result["folder"]
    }
@app.get("/video-info")
async def video_info():

    global latest_uploaded_video

    if latest_uploaded_video is None:
        return {"error": "No video uploaded."}

    return get_video_info(latest_uploaded_video)

@app.post("/caption")
async def caption():

    global latest_uploaded_video

    if latest_uploaded_video is None:
        return {
            "error": "No video uploaded."
        }

    result = process_video(
        latest_uploaded_video
    )

    return result