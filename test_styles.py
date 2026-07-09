from backend.caption import caption_video
from backend.summarizer import summarize_video
from backend.styles import generate_styles

captions = caption_video(
    "outputs/Untitled video - Made with Clipchamp"
)

summary = summarize_video(captions)

print("\nVIDEO SUMMARY:\n")
print(summary)

print("\nSTYLES:\n")

styles = generate_styles(summary)

print(styles)