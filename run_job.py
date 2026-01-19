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
    logger.info("Starting Autonomous Job Runner...")

    # 1. Restore token.json from Environment Variable if missing
    if not os.path.exists("token.json"):
        token_data = os.environ.get("YOUTUBE_TOKEN_JSON")
        if token_data:
            logger.info("Restoring token.json from Environment Variable...")
            with open("token.json", "w") as f:
                f.write(token_data)
        else:
            logger.warning("YOUTUBE_TOKEN_JSON env var not set. YouTube upload might fail if token.json is missing.")

    # 2. Run the Job
    try:
        from scheduler import daily_content_job
        await daily_content_job()
        logger.info("Job Runner Completed Successfully.")
    except Exception as e:
        logger.error(f"Job Runner Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
