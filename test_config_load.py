import os
# Simulate missing env var
if "IMGBB_API_KEY" in os.environ:
    del os.environ["IMGBB_API_KEY"]

try:
    from config import settings
    print(f"✅ SUCCESS: Config loaded without crashing.")
    print(f"   Key Value: '{settings.IMGBB_API_KEY}'")
except Exception as e:
    print(f"❌ FAILED: Config crashed with error: {e}")
