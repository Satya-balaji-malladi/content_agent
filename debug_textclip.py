from moviepy.editor import TextClip
import sys

try:
    print("Attempting to create TextClip...")
    # Try a simple TextClip
    txt = TextClip("TEST CAPTION", fontsize=70, color='white')
    print("TextClip created successfully.")
    txt.save_frame("test_text.png", t=0)
    print("Frame saved.")
except Exception as e:
    print(f"FAILED to create TextClip. Error: {e}")
    # Check for ImageMagick configuration
    from moviepy.config import get_setting
    try:
        binary = get_setting("IMAGEMAGICK_BINARY")
        print(f"ImageMagick Binary Path: {binary}")
    except:
        print("Could not retrieve ImageMagick binary path.")
