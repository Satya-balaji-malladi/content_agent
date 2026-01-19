import asyncio
import logging
import sys
from scheduler import daily_content_job

# Configure logging to see output
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])

async def main():
    print("--- MANUALLY TRIGGERING MORNING SLOT (Recovering Missed 09:00 Job) ---")
    try:
        await daily_content_job()
        print("--- Morning Job Completed Successfully ---")
    except Exception as e:
        print(f"--- Morning Job Failed: {e} ---")

if __name__ == "__main__":
    asyncio.run(main())
