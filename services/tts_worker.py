import edge_tts
import asyncio
import sys

async def generate(text, output_file):
    voice = "en-US-AriaNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

if __name__ == "__main__":
    # stored in sys.argv[1] is the text, sys.argv[2] is output file
    if len(sys.argv) < 3:
        print("Usage: python tts_worker.py <text> <output_file>")
        sys.exit(1)
        
    text = sys.argv[1]
    output_key = sys.argv[2]
    
    asyncio.run(generate(text, output_key))
