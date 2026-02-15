import sys
import os
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Setup logging
logging.basicConfig(level=logging.INFO)

print("--- Starting Fallback Test ---")

try:
    from services.gemini_gen import generate_image
    print("Function imported successfully.")
    
    # Test
    success = generate_image("A futuristic cyberpunk city", "fallback_test.jpg")
    if success:
        print("TEST PASSED: Image generated.")
    else:
        print("TEST FAILED: All strategies exhausted.")
except Exception as e:
    print(f"TEST ERROR: {e}")
