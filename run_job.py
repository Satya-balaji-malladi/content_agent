import asyncio
import logging
import os
import sys
import json
from PIL import Image

# Monkeypatch ANTIALIAS for Pillow 10+ compatibility with MoviePy
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure we are in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

async def main():
    logger.info("Starting Autonomous Job Runner...")

    # Helper Functions for File Management
    import shutil
    
    def ensure_temp_dir():
        if not os.path.exists("temp"):
            os.makedirs("temp")
            logger.info("Created 'temp/' directory.")

    def cleanup_temp():
        # Deletes all files in temp/ but keeps the folder
        if os.path.exists("temp"):
            for filename in os.listdir("temp"):
                file_path = os.path.join("temp", filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    logger.warning(f"Failed to delete {file_path}: {e}")
            logger.info("Cleaned up 'temp/' directory.")

    # 1. Restore token.json from Environment Variable if missing
    if not os.path.exists("token.json"):
        token_data = os.environ.get("YOUTUBE_TOKEN_JSON")
        if token_data:
            logger.info("Restoring token.json from Environment Variable...")
            with open("token.json", "w") as f:
                f.write(token_data)
        else:
            logger.warning("YOUTUBE_TOKEN_JSON env var not set. YouTube upload might fail if token.json is missing.")

    # 2. Run the Job with Cleanup
    ensure_temp_dir()
    cleanup_temp() # Clean start
    
    try:
        from scheduler import daily_content_job
        await daily_content_job()
        logger.info("Job Runner Completed Successfully.")
    except Exception as e:
        logger.error(f"Job Runner Failed: {e}")
        sys.exit(1)
    finally:
        cleanup_temp() # Clean exit (optional, maybe keep for debugging if failed?)
        # For now, following user instruction to clean at end.

if __name__ == "__main__":
    asyncio.run(main())
