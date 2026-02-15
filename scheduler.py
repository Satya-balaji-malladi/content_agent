from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from services.gemini_gen import generate_cinematic_story
from services.social_insta import post_to_instagram
from services.social_youtube import create_premium_reel, upload_to_youtube
import asyncio
import os

logger = logging.getLogger(__name__)

async def daily_content_job():
    logger.info("Starting Daily Premium Reel Job...")
    try:
        # 1. Generate Cinematic Script & Assets (Non-Blocking)
        logger.info("Generating content asynchronously...")
        content = await asyncio.to_thread(generate_cinematic_story)
        logger.info(f"Generated Cinematic Story: {content['topic']}")

        video_path = None
        if content['image_paths']:
            # 2. Render Video (Heavy Blocking Task moved to thread)
            logger.info("Rendering video asynchronously...")
            video_path = await asyncio.to_thread(
                create_premium_reel,
                content['image_paths'], 
                content['hook_count'],
                content['topic'], 
                content['narrative'],
                "output_premium.mp4",
                True # Autonomous
            )
        else:
            logger.warning("No images generated due to service outage. Skipping video creation.")
        
        if video_path and video_path != "PREVIEW_GENERATED":
             # 3. Upload to YouTube (Network Blocking Task moved to thread)
             logger.info("Uploading to YouTube asynchronously...")
             await asyncio.to_thread(
                 upload_to_youtube,
                 video_path, 
                 title=content['youtube_title'], 
                 description=content['youtube_description'],
                 tags=content['youtube_tags'],
                 privacy="public"
             )
        
        # 4. Instagram Complementary Post (Network Blocking Task moved to thread)
        if content['image_paths']:
            logger.info("Posting to Instagram asynchronously...")
            await asyncio.to_thread(post_to_instagram, content['narrative'], content['image_paths'][0])
        else:
            logger.info("Skipping Instagram Post (No images generated).")
        
        # Cleanup
        if os.path.exists("is_final_approved.txt"): os.remove("is_final_approved.txt")
        logger.info("Daily Content Job Completed.")
        
    except Exception as e:
        if os.path.exists("is_final_approved.txt"): os.remove("is_final_approved.txt")
        logger.error(f"Job Failed: {e}")
        raise e

def start_scheduler():
    scheduler = AsyncIOScheduler()
    # Dual Posting Schedule
    scheduler.add_job(daily_content_job, CronTrigger(hour=9, minute=0), id="morning_post")
    scheduler.add_job(daily_content_job, CronTrigger(hour=19, minute=30), id="evening_post")
    
    scheduler.start()
    logger.info("Scheduler started. Jobs set for 09:00 and 19:30 daily.")
    return scheduler
