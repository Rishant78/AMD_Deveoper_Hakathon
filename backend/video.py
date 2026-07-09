import cv2
import os
from backend.config import MAX_FRAMES, BLUR_THRESHOLD


def is_blurry(frame, threshold=BLUR_THRESHOLD):
    """
    Returns True if the frame is blurry.
    """

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    variance = cv2.Laplacian(
        gray,
        cv2.CV_64F
    ).var()

    return variance < threshold


def extract_frames(video_path, output_root="outputs"):
    """
    Extract approximately MAX_FRAMES sharp frames from a video.
    """

    video_name = os.path.splitext(
        os.path.basename(video_path)
    )[0]

    output_folder = os.path.join(output_root, video_name)
    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    interval = max(1, total_frames // MAX_FRAMES)

    frame_count = 0
    saved_count = 0
    blurred_frames = 0

    while True:

        success, frame = cap.read()

        if not success:
            break

        if frame_count % interval == 0:

            candidate = frame
            found_sharp = not is_blurry(candidate)

            # Search ahead for a sharp frame
            if not found_sharp:

                blurred_frames += 1

                for _ in range(10):

                    success, next_frame = cap.read()

                    if not success:
                        break

                    frame_count += 1

                    if not is_blurry(next_frame):
                        candidate = next_frame
                        found_sharp = True
                        break

            # Save the frame if we found a sharp one
            if found_sharp:

                frame_path = os.path.join(
                    output_folder,
                    f"frame_{saved_count:04d}.jpg"
                )

                cv2.imwrite(frame_path, candidate)

                saved_count += 1

                if saved_count >= MAX_FRAMES:
                    break

        frame_count += 1

    cap.release()

    return {
        "frames": saved_count,
        "blurred_frames": blurred_frames,
        "folder": output_folder,
        "interval": interval,
        "total_frames": total_frames
    }

def get_video_info(video_path):
    """
    Returns basic metadata about the uploaded video.
    """

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)

    total_frames = int(
        cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    duration = (
        total_frames / fps
        if fps > 0
        else 0
    )

    cap.release()

    return {
        "fps": round(fps, 2),
        "total_frames": total_frames,
        "duration": round(duration, 2)
    }