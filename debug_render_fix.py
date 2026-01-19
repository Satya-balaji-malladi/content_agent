from moviepy.editor import ImageClip, CompositeVideoClip, TextClip, ColorClip, concatenate_videoclips
import os
from PIL import Image

def test_render():
    img_path = "frame_1.jpg"
    if not os.path.exists(img_path):
        print("Test image not found.")
        return

    # Simulate logic from social_youtube.py
    
    # 1. PIL Pre-resize
    with Image.open(img_path) as pil_img:
        pil_img = pil_img.resize((1188, 2112), Image.LANCZOS)
        left = (1188 - 1080)/2
        top = (2112 - 1920)/2
        pil_img = pil_img.crop((left, top, left+1080, top+1920))
        temp_path = "debug_temp.jpg"
        pil_img.save(temp_path, quality=90)
    
    # 2. MoviePy Clip
    try:
        clip = ImageClip(temp_path)
        clip = clip.set_duration(3)
        clip = clip.resize(lambda t: 1.0 + (0.05 * t / 3))
        clip = clip.set_position('center')
        
        # 3. Text Clip (Caption)
        caption = TextClip("TEST CAPTION", fontsize=85, color='white', font='Arial-Bold', stroke_color='black', stroke_width=4, size=(1080, None))
        caption = caption.set_pos(('center', 0.65), relative=True).set_duration(3)
        
        # 4. Composite
        final = CompositeVideoClip([clip, caption], size=(1080, 1920))
        
        # 5. Render
        final.write_videofile("test_fix.mp4", fps=24, preset="ultrafast")
        
        print("Render complete. Check test_fix.mp4")
        
    finally:
        # DO NOT DELETE TEMP yet
        pass

if __name__ == "__main__":
    test_render()
