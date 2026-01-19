import requests
import logging
from config import settings
import base64

logger = logging.getLogger(__name__)

def upload_image_to_imgbb(image_path: str) -> str:
    """
    Uploads an image to ImgBB and returns the direct display URL.
    Returns None if upload fails.
    """
    if not settings.IMGBB_API_KEY:
        logger.warning("IMGBB_API_KEY not set. Cannot upload image for Instagram.")
        return None

    try:
        url = "https://api.imgbb.com/1/upload"
        
        with open(image_path, "rb") as file:
            payload = {
                "key": settings.IMGBB_API_KEY,
                "image": base64.b64encode(file.read()),
            }
            
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            data = response.json()
            return data['data']['url']
        else:
            logger.error(f"ImgBB Upload Failed: {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"ImgBB Error: {e}")
        return None
