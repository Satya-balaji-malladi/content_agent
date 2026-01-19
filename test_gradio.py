from gradio_client import Client
import time

print("Connecting to ModelScope...")
# Using a popular mirror or the main space
client = Client("damo-vilab/modelscope-text-to-video-synthesis")

prompt = "A futuristic cyberpunk city with neon lights, flying cars, cinematic 4k"

print(f"Generating vide for: {prompt}")
print("This might take 60-100 seconds if the queue is busy...")

result = client.predict(
		prompt,	# str  in 'Input Text' Textbox component
		-1,	# float  in 'Seed' Number component
		fn_index=0
)

print(f"Video saved at: {result}")

# Rename to mp4 for ease
import shutil
shutil.move(result, "test_gradio_video.mp4")
print("Moved to test_gradio_video.mp4")
