import os
from google_auth_oauthlib.flow import InstalledAppFlow

def authenticate_youtube():
    # Define the required scopes
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    # Check for client_secrets.json or client_secret.json
    secret_file = None
    if os.path.exists('client_secrets.json'):
        secret_file = 'client_secrets.json'
    elif os.path.exists('client_secret.json'):
        secret_file = 'client_secret.json'
    
    if not secret_file:
        print("❌ client_secrets.json is missing! Please download it from Google Cloud Console.")
        return

    try:
        print(f"Using secret file: {secret_file}")
        # Create the flow
        flow = InstalledAppFlow.from_client_secrets_file(
            secret_file, SCOPES)
        
        # Run the local server to let the user login
        print("Opening browser for authentication...")
        creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
        print("✅ Login Successful! token.json created. You can now run the main bot.")
        
    except Exception as e:
        print(f"❌ An error occurred during authentication: {e}")

if __name__ == "__main__":
    authenticate_youtube()
