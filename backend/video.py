import cv2
import os
from backend.config import DUP_THRESHOLD


def is_duplicate(frame1, frame2, threshold=DUP_THRESHOLD):
    """
    Returns True if the average absolute pixel difference between frame1 and frame2 is below the threshold.
    """
    if frame1 is None or frame2 is None:
        return False

    # Convert to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Resize to small dimensions to capture global structural similarity
    gray1_resized = cv2.resize(gray1, (64, 64))
    gray2_resized = cv2.resize(gray2, (64, 64))

    # Compute absolute difference
    diff = cv2.absdiff(gray1_resized, gray2_resized)
    mean_diff = diff.mean()

    return mean_diff < threshold


def get_target_frames(duration):
    """
    Returns the target number of frames based on video duration:
    - Video <= 30 sec -> 8 frames
    - 30 sec to 2 min -> 15 frames
    - 2 to 5 min -> 20 frames
    - 5+ min -> 30 frames
    """
    if duration <= 30:
        return 8
    elif duration <= 120:
        return 15
    elif duration <= 300:
        return 20
    else:
        return 30


def format_timestamp(seconds):
    """
    Format seconds into MM:SS or HH:MM:SS format.
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def extract_frames(video_path, output_root="outputs"):
    """
    Extract representative sharp keyframes from a video using duration-based adaptive sampling and duplicate removal.
    """
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_folder = os.path.join(output_root, video_name)
    os.makedirs(output_folder, exist_ok=True)

    # Clean existing frames in output directory to prevent stale data
    for file in os.listdir(output_folder):
        if file.endswith(".jpg"):
            try:
                os.remove(os.path.join(output_folder, file))
            except Exception:
                pass

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps > 0:
        duration = total_frames / fps
    else:
        duration = 0

    if total_frames <= 0 or fps <= 0:
        cap.release()
        return {
            "frames": 0,
            "folder": output_folder,
            "saved_frames": [],
            "total_frames": total_frames,
            "duration": round(duration, 2),
            "fps": round(fps, 2)
        }

    target_frames = get_target_frames(duration)

    # If the video has fewer frames than target, adjust the target
    if total_frames < target_frames:
        target_frames = total_frames

    # Calculate uniform sampling frame indices
    if target_frames > 1:
        sample_indices = [
            int(i * (total_frames - 1) / (target_frames - 1))
            for i in range(target_frames)
        ]
    else:
        sample_indices = [0]

    # Ensure unique and sorted indices
    sample_indices = sorted(list(set(sample_indices)))

    saved_frames = []
    last_saved_frame = None
    saved_count = 0

    for idx in sample_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        success, frame = cap.read()
        if not success:
            continue

        # Skip duplicate frames
        if last_saved_frame is not None:
            if is_duplicate(frame, last_saved_frame):
                continue

        # Save non-duplicate frame
        frame_filename = f"frame_{saved_count:04d}.jpg"
        frame_path = os.path.join(output_folder, frame_filename)
        cv2.imwrite(frame_path, frame)

        # Calculate time metadata
        timestamp_seconds = idx / fps
        timestamp_formatted = format_timestamp(timestamp_seconds)

        saved_frames.append({
            "filename": frame_filename,
            "frame_path": frame_path,
            "timestamp_seconds": round(timestamp_seconds, 2),
            "timestamp_formatted": timestamp_formatted
        })

        last_saved_frame = frame.copy()
        saved_count += 1

    cap.release()

    return {
        "frames": saved_count,
        "folder": output_folder,
        "saved_frames": saved_frames,
        "total_frames": total_frames,
        "duration": round(duration, 2),
        "fps": round(fps, 2)
    }


def get_video_info(video_path):
    """
    Returns basic metadata about the uploaded video.
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if fps > 0:
        duration = total_frames / fps
    else:
        duration = 0

    cap.release()

    return {
        "fps": round(fps, 2),
        "total_frames": total_frames,
        "duration": round(duration, 2)
    }