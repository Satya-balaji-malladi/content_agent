import sys
import os
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Import
try:
    from services.gemini_gen import generate_image
except ImportError:
    pass

logging.basicConfig(level=logging.INFO)

print("--- Testing Generation Logic ---")
try:
    success = generate_image("test prompt", "test_final.jpg")
    if success:
        print("SUCCESS: Image generated.")
    else:
        print("FAILURE: Service likely down, but handled gracefully (returned False).")
except Exception as e:
    print(f"CRITICAL ERROR: {e}")
