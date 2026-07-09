VIDEO_CAPTION_PROMPT = """
You are an image captioning model.

Your task is ONLY to describe what is visible.

Rules:
- Return ONLY one sentence.
- Maximum 25 words.
- Do NOT explain your reasoning.
- Do NOT think step by step.
- Do NOT mention what you are doing.
- Do NOT use bullet points.
- Do NOT add introductions.
- Describe only what is visible.

Caption:
"""
STYLE_PROMPT = """
Rewrite the following video caption into FOUR different styles.

Caption:
{caption}

Return EXACTLY in this format:

Formal:
...

Sarcastic:
...

Humorous-Tech:
...

Humorous-NonTech:
...

Rules:
- Keep the meaning the same.
- Don't invent information.
- Maximum 35 words each.
- Return ONLY the four captions.
"""


VIDEO_SUMMARIZER_PROMPT = """
You are an expert video understanding assistant.

The following captions come from key frames extracted from the SAME video.

Your task is to infer the overall content of the video.

Rules:
- Produce ONE coherent caption.
- Do NOT list every frame.
- Do NOT say "a montage".
- Describe the video as a continuous scene.
- Mention only the most important actions.
- Maximum 35 words.
- Return ONLY the final caption.
"""