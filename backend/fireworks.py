import base64
import requests

from backend.prompts import VIDEO_CAPTION_PROMPT
from backend.config import (
    FIREWORKS_API_KEY,
    MODEL_NAME
)

URL = "https://api.fireworks.ai/inference/v1/chat/completions"


def image_to_base64(image_path):
    with open(image_path, "rb") as image:
        return base64.b64encode(image.read()).decode("utf-8")


def generate_caption(image_path):

    image_base64 = image_to_base64(image_path)

    headers = {
        "Authorization": f"Bearer {FIREWORKS_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an image captioning assistant. "
                    "Return ONLY the final caption. "
                    "Never reveal reasoning, thinking, analysis, or explanations."
                )
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": VIDEO_CAPTION_PROMPT
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        "reasoning_effort": "none",
        "max_tokens": 80,
        "temperature": 0.2
    }

    response = requests.post(
        URL,
        headers=headers,
        json=payload
    )

    result = response.json()

    if "choices" not in result:
        return result

    return result["choices"][0]["message"]["content"]