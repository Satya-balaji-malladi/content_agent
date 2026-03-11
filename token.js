// token.js

// OAuth 2.0 token management functions for YouTube API authentication

const { google } = require('googleapis');
const TOKEN_PATH = 'token.json';

// Load client secrets from a local file.
function loadCredentials() {
    return new Promise((resolve, reject) => {
        fs.readFile('credentials.json', (err, content) => {
            if (err) return reject('Error loading client secret file:' + err);
            resolve(JSON.parse(content));
        });
    });
}

// Authorize a client with credentials, then call the YouTube API.
async function authorize() {
    const credentials = await loadCredentials();
    const { client_secret, client_id, redirect_uris } = credentials.installed;
    const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);

    // Check if we have previously stored a token.
    try {
        const token = fs.readFileSync(TOKEN_PATH);
        oAuth2Client.setCredentials(JSON.parse(token));
    } catch (err) {
        return getAccessToken(oAuth2Client);
    }
    return oAuth2Client;
}

// Get and store new token after prompting for user authorization.
function getAccessToken(oAuth2Client) {
    const authUrl = oAuth2Client.generateAuthUrl({
        access_type: 'offline',
        scope: ['https://www.googleapis.com/auth/youtube.readonly'],
    });
    console.log('Authorize this app by visiting this url:', authUrl);
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });
    rl.question('Enter the code from that page here: ', async (code) => {
        rl.close();
        const { tokens } = await oAuth2Client.getToken(code);
        oAuth2Client.setCredentials(tokens);
        // Store the token to disk for later program executions
        fs.writeFileSync(TOKEN_PATH, JSON.stringify(tokens));
        console.log('Token stored to', TOKEN_PATH);
    });
}

module.exports = { authorize };