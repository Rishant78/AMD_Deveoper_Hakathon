import requests

from backend.config import (
    FIREWORKS_API_KEY,
    MODEL_NAME
)

from backend.prompts import STYLE_PROMPT

URL = "https://api.fireworks.ai/inference/v1/chat/completions"
def parse_styles(text):

    # Convert literal "\n" into actual newlines
    text = text.replace("\\n", "\n")

    styles = {}
    current = None

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("Formal:"):
            current = "formal"
            styles[current] = line.replace("Formal:", "").strip()

        elif line.startswith("Sarcastic:"):
            current = "sarcastic"
            styles[current] = line.replace("Sarcastic:", "").strip()

        elif line.startswith("Humorous-Tech:"):
            current = "humorous_tech"
            styles[current] = line.replace("Humorous-Tech:", "").strip()

        elif line.startswith("Humorous-NonTech:"):
            current = "humorous_nontech"
            styles[current] = line.replace("Humorous-NonTech:", "").strip()

        elif current:
            styles[current] += " " + line

    return styles

def generate_styles(caption):

    headers = {
        "Authorization": f"Bearer {FIREWORKS_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,

        "messages": [
            {
                "role": "system",
                "content": "You rewrite captions."
            },
            {
                "role": "user",
                "content": STYLE_PROMPT.format(
                    caption=caption
                )
            }
        ],

        "reasoning_effort": "none",
        "temperature": 0.6,
        "max_tokens": 250
    }

    response = requests.post(
        URL,
        headers=headers,
        json=payload
    )

    result = response.json()

    if "choices" not in result:
        return result

    styles_text = result["choices"][0]["message"]["content"]
    return parse_styles(styles_text)