import google.generativeai as genai
import logging
import urllib.parse
import random
import time
import requests
from config import settings

# Configure API
genai.configure(api_key=settings.GOOGLE_API_KEY)

# Logger
logger = logging.getLogger(__name__)

def generate_image_with_fallback(prompt, output_path):
    """
    Generates an image using Pollinations AI (Flux) with robust fallback mechanisms.
    If Pollinations fails (Error 530/500/Connection), it falls back to a placeholder image 
    so the pipeline does not crash.
    """
    import requests
    import urllib.parse
    import time
    
    # Attempt 1: Pollinations AI (Flux)
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&model=flux&nologo=true"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        # Short retry loop for primary provider
        for attempt in range(2):
            try:
                response = requests.get(url, headers=headers, timeout=20)
                if response.status_code == 200 and len(response.content) > 1000:
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    logger.info(f"SUCCESS: Image generated via Pollinations (Flux).")
                    return True
                else:
                    logger.warning(f"Pollinations attempt {attempt+1} failed: {response.status_code}")
                    if response.status_code in [530, 403, 500, 502]:
                        break # Fail fast on server errors
            except Exception as e:
                logger.warning(f"Pollinations connection error: {e}")
            time.sleep(1)
            
        logger.warning("⚠️ Pollinations Service Down or Unreachable. Using Fallback Provider.")

    except Exception as e:
        logger.error(f"Critical error in Pollinations request: {e}")

    # Attempt 2: Picsum (Fallback Placeholder)
    # Using 'picsum.photos' for reliable random abstract/nature vertical images
    try:
        params = urllib.parse.quote(prompt[:20]) # Seed with prompt prefix for consistency
        fallback_url = f"https://picsum.photos/seed/{params}/1080/1920" # Vertical High Res
        
        logger.info(f"Attempting Fallback: {fallback_url}")
        response = requests.get(fallback_url, timeout=15)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            logger.warning(f"⚠️ Generated PLACEHOLDER image via Picsum (Service Outage Fallback).")
            return True
        else:
            logger.error(f"Fallback Provider also failed: {response.status_code}")
            return False

    except Exception as e:
        logger.error(f"Fallback generation failed: {e}")
        return False

def generate_cinematic_story():
    """
    Generates a daily tech tip (text) and an image prompt, 
    then generates the image (if supported by the specific model version available).
    
    Returns:
        dict: {
            "caption": str,
            "image_path": str (local path to saved image),
            "topic": str
        }
    """
    try:
        # 1. Generate Text Content (Tip + Image Prompt)
        # Using a model alias that represents the user's request. 
        # Fallback to 'gemini-1.5-flash' if 'gemini-3.0-flash' is not yet available publicly.
        model_name = "gemini-2.0-flash" 
        model = genai.GenerativeModel(model_name)
        
        prompt = """
        You are a cinematic director and expert in "Short Form Retention". Generate a "Cinematic Story" (Vertical 9:16) with an "Infinite Loop" ending.
        
        Constraints:
        - Optimal Duration: 35 seconds (Range 30-40s).
        - Word Count: 90-110 words.
        - Hook: Strict 5-8 seconds. 
        - Climax: Must occur at the 25-second mark.
        - Loop Logic: The final sentence must flow seamlessly back into the hook for infinite viewing.
        
        Output Format (JSON):
        {
            "topic": "The Cinematic Title",
            "narrative": "The full story (90-110 words).",
            "hook_prompts": [
                "3 cinematic noir prompts for the first 8 seconds."
            ],
            "story_prompts": [
                "12 sequential cinematic noir prompts for the rest."
            ],
            "youtube_title": "The Secret of the Night... 😱 | Balaji Bytes",
            "youtube_description": "A mysterious figure emerges in the darkness... but what is he looking for? A cinematic AI story.\\n\\nTimestamps:\\n0:00 - The Setup\\n0:25 - The Twist\\n\\nFollow Balaji Bytes for more AI Stories! #AIStory #Storytelling #BalajiBytes",
            "youtube_tags": ["AI Storytelling", "Cinematic AI", "Mystery", "Balaji Bytes", "Satya Balaji", "Shorts", "Moral Stories"]
        }
        
        SEO INSTRUCTIONS (MYSTERY/STORYTELLING NICHE):
        1. Title Pattern: "[Mystery/Hook] + [Subject]... 😱 | Balaji Bytes". (e.g. "What happened to the Code? | Balaji Bytes")
        2. Description: Start with a Story Hook (First 125 chars). Add timestamps (0:00 Intro, 0:25 The Twist).
        3. Tags: "AI Storytelling", "Cinematic AI video", "Mystery Narratives", "Balaji Bytes", "Satya Balaji".
        4. Hashtags: #AIStory #Storytelling #BalajiBytes #TrendingShorts
        """
        
        
        # Implement Backoff for Gemini
        response = None
        import time
        from google.api_core import exceptions
        
        for attempt in range(3):
            try:
                response_text = None
                
                # Primary: Gemini
                try:
                    gemini_resp = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
                    response_text = gemini_resp.text
                except exceptions.ResourceExhausted:
                    logger.warning("Gemini Quota Exceeded. Attempting Failover to Groq...")
                    
                    # Secondary: Groq
                    try:
                        from groq import Groq
                        import os
                        # Hardcoded key as per user request (simulated - normally use env)
                        if settings.GROQ_API_KEY:
                            client = Groq(api_key=settings.GROQ_API_KEY)
                            chat_completion = client.chat.completions.create(
                                messages=[
                                    {"role": "system", "content": "You are a JSON-only API. Return valid JSON matching the schema."},
                                    {"role": "user", "content": prompt}
                                ],
                                model="llama-3.3-70b-versatile",
                                response_format={"type": "json_object"}
                            )
                            response_text = chat_completion.choices[0].message.content
                            logger.info("FAILOVER SUCCESS: Content generated via Groq (Llama-3.3).")
                        else:
                            raise Exception("No GROQ_API_KEY available for failover.")
                    except Exception as groq_e:
                        logger.error(f"Groq Failover Failed: {groq_e}")
                        raise exceptions.ResourceExhausted("Both Primary and Secondary failed.")

                if response_text:
                    import json
                    # Validation
                    data = json.loads(response_text)
                    break
                    
            except exceptions.ResourceExhausted:
                 wait_time = 20 * (attempt + 1)
                 logger.warning(f"All Providers Exhausted. Sleeping for {wait_time}s...")
                 time.sleep(wait_time)
            except Exception as e:
                 logger.error(f"Generation Error: {e}")
                 raise e
        
        if not data:
             raise Exception("Content Generation Failed after retries.")
        
        # data is already loaded in the loop above
        # import json
        # data = json.loads(response.text)
        
        logger.info(f"Generated Cinematic Story: {data['topic']}")
        
        # 2. Generate Images (Pollinations.ai)
        all_prompts = data['hook_prompts'] + data['story_prompts']
        image_paths = []
        
        # Ensure temp dir exists using relative path assumes calling context handled it
        # But good to be safe here if run independently
        import os
        if not os.path.exists("temp"): os.makedirs("temp")
        
        logger.info(f"Starting Pollinations.ai Generation for {len(all_prompts)} frames...")
        
        for i, prompt in enumerate(all_prompts):
            # Save to temp directory
            filename = f"frame_{i+1}.jpg"
            path = os.path.join("temp", filename)
            
            if generate_image_with_fallback(prompt, path):
                image_paths.append(path)
            else:
                logger.error(f"Failed to generate Frame {i+1} even with fallback.")

        
        # (Orphaned except blocks removed)


        return {
            "narrative": data['narrative'],
            "topic": data['topic'],
            "image_paths": image_paths,
            "youtube_title": data['youtube_title'],
            "youtube_description": data['youtube_description'],
            "youtube_tags": data['youtube_tags'],
            "hook_count": len(data['hook_prompts'])
        }

    except Exception as e:
        logger.error(f"Error generating content: {e}")
        raise e
