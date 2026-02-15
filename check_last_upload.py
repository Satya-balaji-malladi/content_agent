from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
import datetime

def check_last_upload():
    try:
        if not os.path.exists('token.json'):
            print("No token.json found.")
            return

        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/youtube.upload'])
        youtube = build('youtube', 'v3', credentials=creds)

        # Get Channel Uploads Playlist
        print("Checking channel details...")
        request = youtube.channels().list(mine=True, part='contentDetails')
        response = request.execute()
        
        if not response['items']:
            print("No channel found.")
            return
            
        uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        # Get Last Upload
        print("Checking recent uploads...")
        request = youtube.playlistItems().list(playlistId=uploads_playlist_id, part='snippet', maxResults=1)
        response = request.execute()
        
        if response['items']:
            video = response['items'][0]['snippet']
            print(f"✅ Latest Video Found:")
            print(f"   Title: {video['title']}")
            print(f"   Uploaded At: {video['publishedAt']}")
            print(f"   Video ID: {video['resourceId']['videoId']}")
            print(f"   Link: https://youtu.be/{video['resourceId']['videoId']}")
        else:
            print("No videos found on this channel.")

    except Exception as e:
        print(f"❌ Could not verify upload: {e}")
        print("Please check YouTube Studio manually.")

if __name__ == "__main__":
    check_last_upload()
