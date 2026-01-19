from pydub import AudioSegment
from pydub.generators import Sine, WhiteNoise
import os

def generate_assets():
    # 1. Click (0.1s sharp sine beep)
    click = Sine(1000).to_audio_segment(duration=50).fade_out(20).apply_gain(-5)
    click.export("click.mp3", format="mp3")
    print("Generated click.mp3")

    # 2. Riser (6s white noise rising volume)
    duration_ms = 8000
    riser = WhiteNoise().to_audio_segment(duration=duration_ms).apply_gain(-40)
    # Linear gain increase from -40 to -5
    riser = riser.fade(from_gain=-40, to_gain=-5, start=0, duration=duration_ms)
    riser.export("riser.mp3", format="mp3")
    print("Generated riser.mp3")

if __name__ == "__main__":
    generate_assets()
