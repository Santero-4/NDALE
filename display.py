"""Handles play/pause/export and displays the animations"""

#Get graph walk from logic

#Send filenames to loader

#Wait for first received frame from bgthread, then scale and autoplay

#Display menu bar always, just dedicate some window space to it. Can also use it to display loading/errors

#On export click, tell logic to do export

#On back to editor click, stop playing video, kill the bg thread, and return to the editor screen


from PIL import Image, ImageTk, ImageSequence

def open_and_resize(image):
    img = Image.open(image)
    frames = []
    for frame in ImageSequence.Iterator(img):
        cp = frame.copy()
        d = frame.info.get("duration", 100)
        if d < 20: d = 20
        cp = cp.resize((img.width * 8, img.height * 8), Image.NEAREST)
        frames.append((cp, d))
    return frames