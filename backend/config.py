import os
from dotenv import load_dotenv

load_dotenv()

FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")

MODEL_NAME = os.getenv("MODEL_NAME")

UPLOAD_FOLDER = "uploads"

OUTPUT_FOLDER = "outputs"

# Threshold for duplicate frame detection (grayscale absolute difference on 0-255 scale)
DUP_THRESHOLD = 15.0