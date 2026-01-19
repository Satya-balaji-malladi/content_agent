
import edge_tts
import asyncio

async def test_tts():
    try:
        communicate = edge_tts.Communicate("Testing the voice engine.", "en-US-GuyNeural")
        await communicate.save("test_edge.mp3")
        print("Edge TTS Success")
    except Exception as e:
        print(f"Edge TTS Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_tts())
