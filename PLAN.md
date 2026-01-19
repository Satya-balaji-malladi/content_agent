# Headless Content Automation Agent: Implementation Plan

- **Goal**: Daily at 8:00 AM, generate a "Tech Tip" and post to **Instagram** and **YouTube Shorts**.
- **Tech Stack Updates**:
    - **YouTube**: Use `moviepy` + `ffmpeg` to convert the generated image into a 15-second vertical video (Short).
    - **Auth**: YouTube Data API v3 (OAuth2).
- **Language**: Python 3.11+
- **Web Framework**: FastAPI (for health check/dashboard)
- **Scheduler**: APScheduler (AsyncIOScheduler)
- **AI**: Google Generative AI (`google-generativeai`)
- **Socials**: 
    - `google-api-python-client` (YouTube Data API)
    - `requests` (Instagram Graph API)
- **Video Processing**: `moviepy`, `ffmpeg` (installed in Docker)
- **Hosting**: Dockerized for Cloud Run / Railway

## File Structure
```
/content_agent
├── main.py              # Entry point: FastAPI app + Scheduler startup
├── config.py            # Environment variables & Configuration
├── scheduler.py         # Job definitions
├── services/
│   ├── __init__.py
│   ├── gemini_gen.py    # Generates text & image
│   ├── social_youtube.py # Converts Image->Video & Uploads to YouTube
│   └── social_insta.py  # Instagram posting logic
├── templates/
│   └── index.html       # Simple dashboard
├── Dockerfile           # Deployment container
└── requirements.txt     # Dependencies
```

## Workflow
1. **Clock**: Scheduler hits 8:00 AM.
2. **Generate**:
    - Call Gemini: "Give me a tech tip about [topic] with an image prompt."
    - Call Gemini (Imagen): Generate image from prompt.
3. **Post**:
    - **Instagram**: Upload Image Container -> Publish.
    - **YouTube**: Convert Image to 60fps Video -> Upload as YouTube Short.
4. **Log**: Store result in memory/log for Dashboard.

## Next Steps
1. Update requirements (add moviepy, google-auth).
2. Update Dockerfile (add ffmpeg).
3. Create generic Video Generator service.
4. Implement YouTube Upload logic.
