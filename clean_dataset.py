import os
import librosa
import numpy as np

INPUT_PATH = "dataset"
OUTPUT_PATH = "cleaned_dataset"

os.makedirs(OUTPUT_PATH, exist_ok=True)

SAMPLE_RATE = 16000
DURATION = 2

def process_file(path):
    try:
        audio, sr = librosa.load(path, sr=SAMPLE_RATE)
        audio, _ = librosa.effects.trim(audio)
        if len(audio) > SAMPLE_RATE * DURATION:
            audio = audio[:SAMPLE_RATE * DURATION]
        else:
            padding = SAMPLE_RATE * DURATION - len(audio)
            audio = np.pad(audio, (0, padding))
        return audio
    except:
        return None

count = 0

for label_folder in ["non_dysarthric", "dysarthric"]:
    label = 0 if label_folder == "non_dysarthric" else 1
    folder_path = os.path.join(INPUT_PATH, label_folder)

    for speaker in os.listdir(folder_path):
        speaker_path = os.path.join(folder_path, speaker)
        if not os.path.isdir(speaker_path):
            continue

        for file in os.listdir(speaker_path):
            if file.endswith(".wav"):
                file_path = os.path.join(speaker_path, file)
                audio = process_file(file_path)
                if audio is not None:
                    np.save(
                        os.path.join(OUTPUT_PATH, f"{label}_{count}.npy"),
                        audio
                    )
                    count += 1

print("Cleaning complete")
print("Total processed files:", count)
