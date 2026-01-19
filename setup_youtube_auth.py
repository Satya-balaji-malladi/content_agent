import os
import logging
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

# Scopes needed for uploading
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def authenticate_youtube():
    """
    Runs a local server flow to let the user log in to Google
    and saves the 'token.json' file for the agent to use later.
    """
    client_secrets_file = "client_secret.json"
    
    if not os.path.exists(client_secrets_file):
        print(f"❌ Error: '{client_secrets_file}' not found.")
        print("Please download your OAuth Client JSON from Google Cloud Console,")
        print("rename it to 'client_secret.json', and place it in this folder.")
        return

    print("🚀 Starting authentication flow...")
    print("Your browser should open shortly. Please log in with your YouTube account.")
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
        creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
        print("✅ Success! 'token.json' has been created.")
        print("You can now run the main agent.")
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")

if __name__ == "__main__":
    authenticate_youtube()
