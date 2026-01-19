
import asyncio
import logging
from scheduler import daily_content_job
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("autonomy_mission.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("AutonomousMission")

async def run_mission():
    logger.info("!!! MISSION START: Cinema_Auto_Post_Zero_Interaction !!!")
    
    # Ensure a clean slate
    if os.path.exists("is_final_approved.txt"):
        os.remove("is_final_approved.txt")
    
    try:
        await daily_content_job()
        logger.info("!!! MISSION COMPLETE: Job deployed to YouTube (Public) and Instagram !!!")
    except Exception as e:
        logger.error(f"!!! MISSION FAILED: {e} !!!")

if __name__ == "__main__":
    asyncio.run(run_mission())
