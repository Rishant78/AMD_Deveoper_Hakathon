from backend.video import extract_frames
from backend.caption import caption_video
from backend.summarizer import summarize_video
from backend.styles import generate_styles


def process_video(video_path):

    # Step 1: Extract Frames
    extracted = extract_frames(video_path)

    folder = extracted["folder"]

    # Step 2: Caption Each Frame
    frame_captions = caption_video(folder)

    # Step 3: Generate Overall Summary
    summary = summarize_video(frame_captions)

    # Step 4: Generate Caption Styles
    styles = generate_styles(summary)

    return {
        "frames_used": extracted["frames"],
        "frame_captions": frame_captions,
        "video_caption": summary,
        "styles": styles
    }