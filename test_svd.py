from gradio_client import Client

print("Connecting to Stable Video Diffusion...")
try:
    client = Client("multimodalart/stable-video-diffusion")
    
    # We need an input image for SVD. Let's use one we generated.
    input_img = "scene_1.jpg" # Ensuring this exists
    
    print("Generating video from image...")
    result = client.predict(
            input_img,	
            "video_frames", # 
            25, # Motion bucket id
            1, # FPS
            0, # Augmentation level
            fn_index=0
    )
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
