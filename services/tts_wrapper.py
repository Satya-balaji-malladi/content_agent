
import subprocess
import os
import sys
import json
import re

def parse_srt(srt_file):
    """Parses SRT to word-level JSON if possible, or at least sentence level."""
    # Note: edge-tts SRT is usually at sentence/chunk level. 
    # To get word level, we need --write-subtitles to be more granular or use internal logic.
    # However, for now, let's at least get the timings.
    if not os.path.exists(srt_file):
        return []
        
    with open(srt_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    entries = []
    # Simple SRT parser
    blocks = content.strip().split("\n\n")
    for block in blocks:
        lines = block.split("\n")
        if len(lines) >= 3:
            # line 1: index
            # line 2: 00:00:00,000 --> 00:00:00,000
            # line 3+: text
            times = re.findall(r"(\d+:\d+:\d+,\d+)", lines[1])
            if len(times) == 2:
                start_str = times[0].replace(",", ".")
                end_str = times[1].replace(",", ".")
                
                # Convert to seconds
                def to_sec(s):
                    h, m, s = s.split(":")
                    return int(h)*3600 + int(m)*60 + float(s)
                
                start = to_sec(start_str)
                end = to_sec(end_str)
                text = " ".join(lines[2:])
                
                # Split into words to simulate word-level
                words = text.split()
                if words:
                    dur = (end - start) / len(words)
                    for i, w in enumerate(words):
                        entries.append({
                            "start": start + i*dur,
                            "end": start + (i+1)*dur,
                            "word": w
                        })
    return entries

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python tts_wrapper.py <text> <output_file>")
        sys.exit(1)
        
    text = sys.argv[1]
    output_file = sys.argv[2]
    sub_file = output_file.replace(".mp3", ".json")
    srt_file = output_file.replace(".mp3", ".srt")
    
    # Try Edge CLI (RyanNeural as backup, GuyNeural as primary)
    voices = ["en-US-GuyNeural", "en-US-AriaNeural", "en-GB-RyanNeural"]
    success = False
    
    for voice in voices:
        print(f"Trying voice: {voice}")
        cmd = [
            "edge-tts",
            "--voice", voice,
            "--text", text,
            "--write-media", output_file,
            "--write-subtitles", srt_file
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            word_data = parse_srt(srt_file)
            with open(sub_file, "w", encoding="utf-8") as f:
                json.dump(word_data, f)
            print(f"Success with {voice}")
            success = True
            break
        except Exception as e:
            print(f"Failed with {voice}: {e}")
            
    if not success:
        print("All Edge voices failed. Falling back to gTTS...")
        from gtts import gTTS
        tts = gTTS(text=text, lang='en', tld='co.uk', slow=False)
        tts.save(output_file)
        with open(sub_file, "w") as f: json.dump([], f)
        
    sys.exit(0)
