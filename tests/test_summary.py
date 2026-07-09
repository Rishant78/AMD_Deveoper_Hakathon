from backend.caption import caption_video
from backend.summarizer import summarize_video

captions = caption_video(
    "outputs/Untitled video - Made with Clipchamp"
)

print("Frame Captions:\n")

for caption in captions:
    print("-", caption)

print("\nFinal Video Caption:\n")

summary = summarize_video(captions)

print(summary)