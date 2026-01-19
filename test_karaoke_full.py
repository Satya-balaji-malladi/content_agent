
import asyncio
import os
import json
import logging
from services.social_youtube import create_premium_reel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_karaoke_render():
    # 1. Setup local assets
    # Search for existing frames
    image_paths = []
    for i in range(1, 40):
        fname = f"frame_{i}.jpg"
        if os.path.exists(fname):
            image_paths.append(fname)
            
    if not image_paths:
        print("No frame_*.jpg images found. Cannot render.")
        return

    # Use existing narrative or default
    narrative = "The shadows lengthened as he walked. Every step was a memory. Every breath, a regret."
    if os.path.exists("temp_narrative.txt"):
        with open("temp_narrative.txt", "r", encoding="utf-8") as f:
            narrative = f.read()
    
    topic = "The Shadow's Edge" 
    
    print(f"Starting test render with {len(image_paths)} images...")
    
    # 2. Execute Render
    output_path = "output_karaoke_test.mp4"
    
    try:
        video_path = create_premium_reel(
            image_paths, 
            hook_count=5, # irrelevant for this test
            text_overlay=topic, 
            full_narrative=narrative,
            output_path=output_path,
            autonomous=True # Skip preview
        )
        
        if video_path and os.path.exists(video_path):
            print(f"!!! SUCCESS: Video rendered to {video_path} !!!")
        else:
            print("!!! FAILURE: Video path returned but file missing or None !!!")
            
    except Exception as e:
        print(f"Render crashed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_karaoke_render())
