
import logging
import os
import sys

# Setup basic logging
logging.basicConfig(level=logging.INFO)

# Import the upload function
# We need to make sure the app directory is in path or we run from root
sys.path.append(os.getcwd())

from services.social_youtube import upload_to_youtube

def run_test_upload():
    video_file = "output_cinematic.mp4"
    
    if not os.path.exists(video_file):
        print(f"Error: {video_file} not found. Cannot test upload.")
        return

    print(f"Starting test upload for {video_file}...")
    print("Privacy: PRIVATE (Safe for testing)")
    
    response = upload_to_youtube(
        video_path=video_file,
        title="Agent Verification Test Upload",
        description="This is a test upload to verify the authenticated YouTube API connection.",
        tags=["test", "agent", "api"],
        privacy="private" # FORCE PRIVATE FOR TEST
    )
    
    if response:
        print("\nSUCCESS: Video uploaded successfully!")
        print(f"Video ID: {response.get('id')}")
        print(f"View at: https://youtu.be/{response.get('id')}")
    else:
        print("\nFAILURE: Upload returned no response (likely auth error).")

if __name__ == "__main__":
    run_test_upload()
