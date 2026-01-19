from services.social_youtube import upload_to_youtube
import os
import sys

video_path = "output_karaoke_test.mp4"

if not os.path.exists(video_path):
    print(f"Error: {video_path} not found. Has the render finished?")
    sys.exit(1)

print(f"Uploading {video_path} to YouTube (Unlisted)...")
try:
    response = upload_to_youtube(
        video_path,
        title="Karaoke Caption Test Build",
        description="Testing the new karaoke highlight system with high-contrast yellow pop.",
        tags=["test", "karaoke"],
        privacy="unlisted"
    )
    if response:
        print(f"Upload Successful! Video ID: {response.get('id')}")
        print(f"Watch here: https://youtu.be/{response.get('id')}")
    else:
        print("Upload failed (no response).")
except Exception as e:
    print(f"Upload failed with error: {e}")
