
import requests
import json
import os
import random
import time
from services.gemini_gen import generate_cinematic_story

def fix_images():
    # We'll just run the full generation again to get fresh visuals with the turbo model
    # This is safer than trying to surgically replace frames.
    print("!!! RE-GENERATING ALL CINEMATIC FRAMES (TURBO ENGINE) !!!")
    content = generate_cinematic_story()
    print(f"New frames ready for: {content['topic']}")
    
    # Save the narrative so finalize_render can use it
    with open("temp_narrative.txt", "w") as f:
        f.write(content['narrative'])
        
    print("!!! ASSETS REFRESHED. READY FOR MASTER RENDER. !!!")

if __name__ == "__main__":
    fix_images()
