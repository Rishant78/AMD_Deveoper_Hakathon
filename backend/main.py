from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.video import get_video_info
from backend.video import extract_frames
from backend.pipeline import process_video
import shutil
import os

app = FastAPI(
    title="AMD Video Captioning API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to specific origins if needed in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Mount outputs folder to serve generated keyframes to the frontend
app.mount("/outputs", StaticFiles(directory=OUTPUT_FOLDER), name="outputs")

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
    video_name = os.path.splitext(os.path.basename(latest_uploaded_video))[0]

    frontend_frames = []
    for f in result["saved_frames"]:
        frontend_frames.append({
            "filename": f["filename"],
            "url": f"/outputs/{video_name}/{f['filename']}",
            "timestamp_seconds": f["timestamp_seconds"],
            "timestamp_formatted": f["timestamp_formatted"]
        })

    return {
        "success": True,
        "video": latest_uploaded_video,
        "frames_extracted": result["frames"],
        "frames": frontend_frames,
        "duration": result["duration"],
        "total_frames": result["total_frames"],
        "fps": result["fps"]
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