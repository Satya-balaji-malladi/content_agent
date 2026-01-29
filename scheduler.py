from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from services.gemini_gen import generate_cinematic_story
# Instagram service ni comment chestunnamu
# from services.social_insta import post_to_instagram 
from services.social_youtube import create_premium_reel, upload_to_youtube
import asyncio
import os

logger = logging.getLogger(__name__)

async def daily_content_job():
    logger.info("Starting Daily Premium Reel Job...")
    try:
        # 1. Generate Cinematic Script & Assets
        # Gemini quota lekunte, idi automatic ga Groq use chestundi
        content = generate_cinematic_story() 
        logger.info(f"Generated Cinematic Story: {content['topic']}")

        video_path = create_premium_reel(
            content['image_paths'], 
            hook_count=content['hook_count'],
            text_overlay=content['topic'], 
            full_narrative=content['narrative'],
            autonomous=True # Bypasses Hook Preview Pause
        )
        
        # 2. YouTube Upload (Idhi panichestundi)
        if video_path and video_path != "PREVIEW_GENERATED":
             upload_to_youtube(
                 video_path, 
                 title=content['youtube_title'], 
                 description=content['youtube_description'],
                 tags=content['youtube_tags'],
                 privacy="public" # Mission requirement
             )
        
        # 3. Instagram Complementary Post (COMMENTED OUT)
        # Ippudu Instagram keys lekapoyina ee script break avvadu
        # if content['image_paths']:
        #     post_to_instagram(content['narrative'], content['image_paths'][0])
        # else:
        #     logger.info("Skipping Instagram Post (No images generated).")
        
        logger.info("Skipping Instagram post as per user request.")
        
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
