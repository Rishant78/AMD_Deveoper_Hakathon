import os

from backend.fireworks import generate_caption


def caption_frames(folder):

    captions = []

    files = sorted(os.listdir(folder))

    for file in files:

        if file.endswith(".jpg"):

            image_path = os.path.join(folder, file)

            caption = generate_caption(image_path)

            captions.append(caption)

    return captions

def caption_video(folder):

    captions = caption_frames(folder)

    return captions