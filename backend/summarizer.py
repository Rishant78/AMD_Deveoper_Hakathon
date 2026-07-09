import requests

from backend.config import (
    FIREWORKS_API_KEY,
    MODEL_NAME
)

from backend.prompts import VIDEO_SUMMARIZER_PROMPT

URL = "https://api.fireworks.ai/inference/v1/chat/completions"


def summarize_video(captions):

    caption_text = "\n".join(
        f"- {caption}"
        for caption in captions
    )

    headers = {
        "Authorization": f"Bearer {FIREWORKS_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,

        "messages": [
            {
                "role": "system",
                "content": VIDEO_SUMMARIZER_PROMPT
            },
            {
                "role": "user",
                "content": caption_text
            }
        ],

        "reasoning_effort": "none",
        "temperature": 0.2,
        "max_tokens": 80
    }

    response = requests.post(
        URL,
        headers=headers,
        json=payload
    )

    result = response.json()

    if "choices" not in result:
        error_msg = result.get("error", {}).get("message") if isinstance(result.get("error"), dict) else result.get("error", "Unknown API error")
        return f"Error: {error_msg}"

    return result["choices"][0]["message"]["content"]