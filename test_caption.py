from backend.caption import caption_video

captions = caption_video("outputs/Untitled video - Made with Clipchamp")

for i, caption in enumerate(captions):

    print(f"{i+1}. {caption}")