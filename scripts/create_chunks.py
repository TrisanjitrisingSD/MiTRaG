import os
import json
from faster_whisper import WhisperModel

model = WhisperModel(
    "small",
    device="cuda",
    compute_type="float16"
)

audio_dir = "/content/drive/MyDrive/Audios"
output_dir = "/content/drive/MyDrive/JSONs"

os.makedirs(output_dir, exist_ok=True)

files = sorted(os.listdir(audio_dir))

print(f"Found {len(files)} audio files\n")

for f in files:
    print(f)
    
for audio in files:

    if not audio.endswith(".mp3"):
        continue

    json_name = audio.replace(".mp3", ".json")
    json_path = os.path.join(output_dir, json_name)

    # Skip already processed lectures
    if os.path.exists(json_path):
        print(f"Skipping {audio}")
        continue

    print(f"\nProcessing {audio}")

    audio_path = os.path.join(audio_dir, audio)

    segments, info = model.transcribe(
        audio_path,
        language="en",
        word_timestamps=False
    )

    chunks = []

    lecture_number = audio.split("_")[0]
    title = "_".join(audio.split("_")[1:]).replace(".mp3", "")

    full_text = ""

    for segment in segments:

        chunks.append({
            "number": lecture_number,
            "title": title,
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip()
        })

        full_text += segment.text.strip() + " "

    output = {
        "chunks": chunks,
        "text": full_text.strip()
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f"Saved {json_name}")    