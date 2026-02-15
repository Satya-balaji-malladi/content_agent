
import logging
import urllib.parse
import time
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_image(prompt, output_path):
    """
    Generates an image using Pollinations AI with retry logic and browser headers.
    """
    try:
        # Encode the prompt
        encoded_prompt = urllib.parse.quote(prompt)
        
        # Exact URL structure as requested
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&model=flux&nologo=true"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        logger.info(f"Testing URL: {url}")
        
        for attempt in range(3):
            try:
                logger.info(f"Attempt {attempt+1}...")
                response = requests.get(url, headers=headers, timeout=30)
                if response.status_code == 200:
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    logger.info(f"Successfully generated image: {output_path}")
                    return True
                else:
                    logger.warning(f"Attempt {attempt+1} failed with status {response.status_code}")
                    logger.warning(f"Response content: {response.text[:200]}") # Print first 200 chars of error
            except Exception as e:
                logger.warning(f"Attempt {attempt+1} error: {e}")
            
            time.sleep(2) # 2-second sleep between failures
            
        logger.error(f"Failed to generate image after 3 attempts.")
        return False
    except Exception as e:
        logger.error(f"Critical error: {e}")
        return False

if __name__ == "__main__":
    prompt = "A futuristic city with neon lights, cinematic lighting, hyper-realistic, 8k"
    generate_image(prompt, "test_image.jpg")
