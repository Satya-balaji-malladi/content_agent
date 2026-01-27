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
        - Optimal Duration: 35 seconds (Range 30-40s).
        - Word Count: 90-110 words.
        - Hook: Strict 5-8 seconds. 
        - Climax: Must occur at the 25-second mark.
        - Loop Logic: The final sentence must flow seamlessly back into the hook for infinite viewing.
        
        Output Format (JSON):
        {
            "topic": "The Cinematic Title",
            "narrative": "The full story (90-110 words).",
            "hook_prompts": ["3 cinematic noir prompts for the first 8 seconds."],
            "story_prompts": ["12 sequential cinematic noir prompts for the rest."],
            "youtube_title": "The Secret of the Night... 😱 | Balaji Bytes",
            "youtube_description": "A mysterious figure emerges in the darkness...",
            "youtube_tags": ["AI Storytelling", "Cinematic AI", "Mystery", "Balaji Bytes"]
        }
        """ # This was the line causing the error!

        for attempt in range(3):
            try:
                response_text = None
                try:
                    gemini_resp = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
                    response_text = gemini_resp.text
                except (exceptions.ResourceExhausted, Exception) as gemini_e:
                    logger.warning(f"Gemini Issue: {gemini_e}. Attempting Failover to Groq...")
                    try:
                        from groq import Groq
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
                            logger.info("FAILOVER SUCCESS: Content generated via Groq.")
                        else:
                            logger.error("No GROQ_API_KEY found.")
                    except Exception as groq_e:
                        logger.error(f"Groq Failover Failed: {groq_e}")

                if response_text:
                    data = json.loads(response_text)
                    break 
                    
            except Exception as e:
                 wait_time = 20 * (attempt + 1)
                 logger.warning(f"Sleeping for {wait_time}s... Error: {e}")
                 time.sleep(wait_time)
        
        if not data:
             raise Exception("Content Generation Failed.")
        
        logger.info(f"Generated Cinematic Story: {data['topic']}")
        
        all_prompts = data.get('hook_prompts', []) + data.get('story_prompts', [])
        image_paths = []

        for i, p_text in enumerate(all_prompts):
            path = f"frame_{i+1}.jpg"
            clean_prompt = p_text.replace('"', '').replace("'", "")
            encoded_prompt = urllib.parse.quote(clean_prompt[:400])
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
                except Exception as e:
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
        logger.error(f"Final Execution Error: {e}")
        raise e
            path = f"frame_{i+1}.jpg"
            clean_prompt = p_text.replace('"', '').replace("'", "")
            encoded_prompt = urllib.parse.quote(clean_prompt[:400])
            
            # Vertical 9:16 Resolution
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
                except Exception as e:
                    logger.warning(f"Frame {i+1} attempt {img_attempt+1} failed: {e}")
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
        logger.error(f"Final Execution Error: {e}")
        raise e
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
        
        # 2. Generate Images (Pollinations.ai) - Fast & Story Montage
        all_prompts = data['hook_prompts'] + data['story_prompts']
        image_paths = []
        
        # 2. Generate Images (Pollinations.ai)
        all_prompts = data['hook_prompts'] + data['story_prompts']
        image_paths = []
        
        try:
            import urllib.parse
            import urllib.request
            import time
            import os

            logger.info(f"Starting Pollinations.ai Generation for {len(all_prompts)} frames...")
            
            for i, prompt in enumerate(all_prompts):
                path = f"frame_{i+1}.jpg"
                
                # Cleanup Prompt
                clean_prompt = prompt.replace('"', '').replace("'", "")
                encoded_prompt = urllib.parse.quote(clean_prompt[:400]) # Limit length
                
                # Pollinations URL (Flux Model, No Logo, 720p for Speed/Stability)
                # CHANGED TO VERTICAL RESOLUTION: 720x1280
                url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=720&height=1280&model=flux&nologo=true&seed={i*123}"
                
                for attempt in range(5): # Increased to 5 retries
                    try:
                        # Random seed update on retry to avoid stuck cache
                        if attempt > 0: url = f"{url}&seed={i*123 + attempt}"
                        
                        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        # Increased timeout to 120s for busy periods
                        with urllib.request.urlopen(req, timeout=120) as response:
                            with open(path, 'wb') as f:
                                f.write(response.read())
                        
                        # Verify file
                        if os.path.exists(path) and os.path.getsize(path) > 1000:
                            logger.info(f"Generated Frame {i+1} (Pollinations/Flux)")
                            image_paths.append(path)
                            # Polite delay to avoid rate limits
                            time.sleep(5) 
                            break
                        else:
                            raise Exception("Empty file downloaded")
                            
                    except Exception as e:
                        logger.warning(f"Frame {i+1} attempt {attempt+1} failed: {e}")
                        time.sleep(10) # 10s cooling off on failure
                        if attempt == 4: logger.error(f"Failed to generate Frame {i+1} after 5 attempts")

        except Exception as e:
             logger.error(f"Pollinations Generation Failed: {e}")

        
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
