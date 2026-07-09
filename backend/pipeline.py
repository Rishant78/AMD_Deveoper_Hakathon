import os
from backend.video import extract_frames
from backend.caption import caption_video
from backend.summarizer import summarize_video
from backend.styles import generate_styles


def process_video(video_path):
    # Step 1: Extract Frames
    extracted = extract_frames(video_path)

    saved_frames = extracted["saved_frames"]

    # Step 2: Caption Each Frame
    captioned_frames = caption_video(saved_frames)

    # Extract text captions for the summarization model
    captions = [f["caption"] for f in captioned_frames]

    # Step 3: Generate Overall Summary
    summary = summarize_video(captions)

    # Step 4: Generate Caption Styles
    styles = generate_styles(summary)

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    
    # Format and map frame metadata to frontend URL layout
    frontend_frames = []
    for f in captioned_frames:
        frontend_frames.append({
            "filename": f["filename"],
            "url": f"/outputs/{video_name}/{f['filename']}",
            "timestamp_seconds": f["timestamp_seconds"],
            "timestamp_formatted": f["timestamp_formatted"],
            "caption": f["caption"]
        })

    return {
        "success": True,
        "video_info": {
            "filename": os.path.basename(video_path),
            "duration": extracted["duration"],
            "fps": extracted["fps"],
            "total_frames": extracted["total_frames"]
        },
        "frames_used": extracted["frames"],
        "frames": frontend_frames,
        "video_caption": summary,
        "styles": styles
    }