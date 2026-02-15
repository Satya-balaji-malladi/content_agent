import requests
import time

def check(name, url, desc):
    print(f"Checking {name}...", end="", flush=True)
    try:
        # Default python requests UA
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200 and len(resp.content) > 100:
            print(f" SUCCESS! ({len(resp.content)} bytes)")
            return True
        else:
            print(f" FAILED ({resp.status_code})")
    except Exception as e:
        print(f" ERROR: {e}")
    return False

print("--- DIAGNOSTIC START ---")
# 1. Google (Internet Check)
check("Internet", "https://www.google.com", "Connectivity")

# 2. Pollinations Root (Service Check)
check("Pollinations Root", "https://image.pollinations.ai/", "Service Up?")

# 3. Flux (High Res)
check("Flux (1080p)", "https://image.pollinations.ai/prompt/test?width=1080&height=1920&model=flux&nologo=true", "User Config")

# 4. Turbo (High Res)
check("Turbo (1080p)", "https://image.pollinations.ai/prompt/test?width=1080&height=1920&model=turbo", "Fallback 1")

# 5. Default (High Res)
check("Default (1080p)", "https://image.pollinations.ai/prompt/test?width=1080&height=1920", "Fallback 2")

# 6. Default (Low Res - 512x512) - Key test for free tier limits
check("Default (512p)", "https://image.pollinations.ai/prompt/test?width=512&height=512", "Low Res Workaround")

print("--- DIAGNOSTIC END ---")
