import requests
import urllib.parse
import time
import sys

def test(name, url):
    print(f"TESTING: {name}", flush=True)
    print(f"URL: {url}", flush=True)
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        # Try with a fresh session
        s = requests.Session()
        resp = s.get(url, headers=headers, timeout=10)
        print(f"STATUS: {resp.status_code}", flush=True)
        if resp.status_code == 200:
            if len(resp.content) > 100:
                print("RESULT: SUCCESS", flush=True)
            else:
                print("RESULT: SUCCESS (But content small)", flush=True)
        else:
            print(f"RESULT: FAIL ({resp.status_code})", flush=True)
            print(f"BODY: {resp.text[:200]}", flush=True)
    except Exception as e:
        print(f"RESULT: ERROR ({e})", flush=True)
    print("-" * 20, flush=True)

prompt = "A cinematic shot of a cyberpunk city"
enc = urllib.parse.quote(prompt)

# 1. User's requested configuration (Flux + NoLogo)
test("Flux + NoLogo (User Request)", f"https://image.pollinations.ai/prompt/{enc}?width=1080&height=1920&model=flux&nologo=true")

# 2. Flux without nologo parameter
test("Flux (Clean)", f"https://image.pollinations.ai/prompt/{enc}?width=1080&height=1920&model=flux")

# 3. Turbo (Reliable fallback)
test("Turbo", f"https://image.pollinations.ai/prompt/{enc}?width=1080&height=1920&model=turbo")

# 4. Flux-Realism
test("Flux Realism", f"https://image.pollinations.ai/prompt/{enc}?width=1080&height=1920&model=flux-realism")
