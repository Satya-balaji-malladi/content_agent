import asyncio
import logging
import os
import sys
import json

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure we are in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

async def main():
    logger.info("Starting Autonomous Job Runner (YouTube Focus)...")

    # 1. Restore YouTube token.json from Environment Variable if missing
    if not os.path.exists("token.json"):
        token_data = os.environ.get("YOUTUBE_TOKEN_JSON")
        if token_data:
            logger.info("Restoring token.json from Environment Variable...")
            with open("token.json", "w") as f:
                f.write(token_data)
        else:
            logger.warning("YOUTUBE_TOKEN_JSON env var not set. YouTube upload might fail.")

    # 2. Run the Job
    try:
        # Import local modules
        # scheduler.py lo nuvvu content generation logic rasi untavu
        from scheduler import daily_content_job
        
        logger.info("Executing daily_content_job...")
        
        # Manam ikkada kevalam YouTube upload mathrame jarigela logic run chesthunnam
        # Instagram logic scheduler lopala unte, andulo 'upload_to_instagram' ni comment chesi unchali
        await daily_content_job()
        
        logger.info("Job Runner Completed Successfully (Only YouTube Focus).")
        
    except Exception as e:
        logger.error(f"Job Runner Failed: {e}")
        # Instagram keys (null) valla error vasthe code break avvakunda ikkada handle chesthunnam
        sys.exit(1)

if __name__ == "__main__":
    # Script automatic ga run avvadaniki
    asyncio.run(main())

# --- SCHEDULER LOGIC REMINDER ---
# Nee scheduler.py lo upload logic ila undali:
#
# async def daily_content_job():
#     video = await generate_content()
#
#     # 1. YouTube Upload (Active)
#     await upload_to_youtube(video)
#
#     # 2. Instagram Upload (Commented out to avoid 'null' errors)
#     # logger.info("Instagram upload is disabled.")
#     # await upload_to_instagram(video)
