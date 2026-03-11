# YouTube Authentication Setup Guide

Follow these step-by-step instructions to authenticate your YouTube application:

## Step 1: Create a Project on Google Cloud
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click on **Select a project** at the top of the page.
3. Click on **New Project**.
4. Enter a name for your project and click **Create**.

## Step 2: Enable the YouTube Data API
1. In your Google Cloud project, navigate to **APIs & Services** > **Library**.
2. Search for **YouTube Data API v3**.
3. Click on it, then click on the **Enable** button.

## Step 3: Create Credentials
1. Go to **APIs & Services** > **Credentials**.
2. Click on **Create Credentials**, then select **OAuth client ID**.
3. Configure the consent screen by providing the necessary information, then click **Save**.
4. Select **Web application** as the application type.
5. Set the authorized redirect URIs (e.g., `http://localhost:3000/oauth2callback`).
6. Click **Create**. You will receive a client ID and client secret.

## Step 4: Implementing Authentication in Your Code
1. Use the client ID and client secret in your application code.
2. Implement the OAuth 2.0 flow by redirecting users to the authorization URL and handling the callback with authorization code.

## Step 5: Testing Authentication
1. Run your application and navigate to the authentication endpoint.
2. Follow the prompts to log in to your Google account and allow access to your application.
3. After successful authentication, you should receive an access token to interact with the YouTube Data API.