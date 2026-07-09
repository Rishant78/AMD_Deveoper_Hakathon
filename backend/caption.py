import os
from backend.fireworks import generate_caption


def caption_video(saved_frames):
    """
    Generate captions for each saved frame in the list of frame dicts.
    Modifies the dictionaries in-place by adding a 'caption' key.
    """
    for frame_info in saved_frames:
        image_path = frame_info["frame_path"]
        
        # Call Fireworks to get the caption
        caption = generate_caption(image_path)
        frame_info["caption"] = caption

    return saved_frames