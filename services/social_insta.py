import requests
import logging
from config import settings
from services.imgbb_uploader import upload_image_to_imgbb

logger = logging.getLogger(__name__)

def post_to_instagram(caption: str, image_path: str):
    """
    Posts an image to Instagram Feed via the Graph API.
    Step 1: Uploads local image to ImgBB to get a public URL.
    Step 2: Creates a Media Container on Instagram.
    Step 3: Publishes the Container.
    """
    try:
        # Pre-check Credentials
        if not settings.INSTAGRAM_ACCESS_TOKEN or settings.INSTAGRAM_ACCESS_TOKEN.startswith("your_"):
            logger.info("Instagram Access Token missing or placeholder. Skipping Instagram post.")
            return

        # 1. Upload to Cloud (ImgBB)
        if not settings.IMGBB_API_KEY:
            logger.warning("No IMGBB_API_KEY. Cannot post to Instagram (requires public URL).")
            return

        logger.info("Uploading image to ImgBB...")
        image_url = upload_image_to_imgbb(image_path)
        
        if not image_url:
            logger.error("ImgBB upload failed. Aborting Instagram post.")
            return

        logger.info(f"Image uploaded: {image_url}")

        # 2. Create Media Container
        url_create = f"https://graph.facebook.com/v18.0/{settings.INSTAGRAM_ACCOUNT_ID}/media"
        payload_create = {
            "image_url": image_url,
            "caption": caption,
            "access_token": settings.INSTAGRAM_ACCESS_TOKEN
        }
        
        res_create = requests.post(url_create, data=payload_create)
        if res_create.status_code != 200:
            logger.error(f"Instagram Create Container Failed: {res_create.text}")
            return
            
        creation_id = res_create.json().get("id")
        if not creation_id:
            logger.error("No Creation ID returned from Instagram.")
            return
            
        logger.info(f"Media Container Created: {creation_id}")

        # 3. Publish Container
        url_publish = f"https://graph.facebook.com/v18.0/{settings.INSTAGRAM_ACCOUNT_ID}/media_publish"
        payload_publish = {
            "creation_id": creation_id,
            "access_token": settings.INSTAGRAM_ACCESS_TOKEN
        }
        
        res_publish = requests.post(url_publish, data=payload_publish)
        if res_publish.status_code == 200:
            logger.info(f"Instagram Post Published! ID: {res_publish.json().get('id')}")
        else:
            logger.error(f"Instagram Publish Failed: {res_publish.text}")

    except Exception as e:
        logger.error(f"Instagram Logic Error: {e}")
