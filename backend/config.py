import os
from dotenv import load_dotenv

load_dotenv()

FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")

MODEL_NAME = os.getenv("MODEL_NAME")

UPLOAD_FOLDER = "uploads"

OUTPUT_FOLDER = "outputs"

FRAME_INTERVAL = 30

BLUR_THRESHOLD = 40

MAX_FRAMES = 10