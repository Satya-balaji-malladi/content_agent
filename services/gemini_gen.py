import google.generativeai as genai
import logging
import json
import time
import os
import urllib.parse
import urllib.request
from google.api_core import exceptions
from config import settings

# Configure API
genai.configure(api_key=settings.GOOGLE_API_KEY)

# Logger
logger = logging.getLogger(__name__)

def generate_cinematic_story():
    data = None 
    try:
        model_name = "gemini-2.0-flash" 
        model = genai.GenerativeModel(model_name)
        
        prompt = """
        You are a cinematic director and expert in "Short Form Retention". Generate a "Cinematic Story" (Vertical 9:16) with an "Infinite Loop" ending.
        
        Constraints:
        - Optimal Duration: 35 seconds.
        - Loop Logic: The final sentence must flow back into the hook.
        
        Output Format (JSON):
        {
            "topic": "Title",
            "narrative": "Story (90-110 words)",
            "hook_prompts": ["3 prompts"],
            "story_prompts": ["12 prompts"],
            "youtube_title": "Title | Balaji Bytes",
            "youtube_description": "Description",
            "youtube_tags": ["tags"]
        }
        """

        for attempt in range(3):
            try:
                response_text = None
                try:
                    gemini_resp = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
                    response_text = gemini_resp.text
                except (exceptions.ResourceExhausted, Exception) as gemini_e:
                    logger.warning(f"Gemini Issue: {gemini_e}. Trying Groq...")
                    try:
                        from groq import Groq
                        if settings.GROQ_API_KEY:
                            client = Groq(api_key=settings.GROQ_API_KEY)
                            chat_completion = client.chat.completions.create(
                                messages=[
                                    {"role": "system", "content": "You are a JSON API."},
                                    {"role": "user", "content": prompt}
                                ],
                                model="llama-3.3-70b-versatile",
                                response_format={"type": "json_object"}
                            )
                            response_text = chat_completion.choices[0].message.content
                        else:
                            logger.error("No GROQ_API_KEY")
                    except Exception as groq_e:
                        logger.error(f"Groq Failed: {groq_e}")

                if response_text:
                    data = json.loads(response_text)
                    break 
                    
            except Exception as e:
                wait_time = 20 * (attempt + 1)
                time.sleep(wait_time)
        
        if not data:
            raise Exception("Generation Failed")
        
        all_prompts = data.get('hook_prompts', []) + data.get('story_prompts', [])
        image_paths = []

        for i, p_text in enumerate(all_prompts):
            path = f"frame_{i+1}.jpg"
            encoded_prompt = urllib.parse.quote(p_text.replace('"', '')[:400])
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=720&height=1280&model=flux&nologo=true&seed={i*123}"
            
            for img_attempt in range(3):
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=60) as response:
                        with open(path, 'wb') as f:
                            f.write(response.read())
                    if os.path.exists(path) and os.path.getsize(path) > 1000:
                        image_paths.append(path)
                        time.sleep(2) 
                        break
                except:
                    time.sleep(5)

        return {
            "narrative": data['narrative'],
            "topic": data['topic'],
            "image_paths": image_paths,
            "youtube_title": data['youtube_title'],
            "youtube_description": data['youtube_description'],
            "youtube_tags": data['youtube_tags'],
            "hook_count": len(data.get('hook_prompts', []))
        }

    except Exception as e:
        logger.error(f"Error: {e}")
        raise e
