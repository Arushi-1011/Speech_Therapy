import os
import numpy as np
import librosa
import pandas as pd
from tqdm import tqdm

CLEANED_PATH = "cleaned_dataset"
OUTPUT_CSV   = "features.csv"
SAMPLE_RATE  = 16000
N_MFCC       = 40

def extract_features(audio, sr=SAMPLE_RATE):
    features = []

    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=N_MFCC)
    mfcc_delta  = librosa.feature.delta(mfcc)
    mfcc_delta2 = librosa.feature.delta(mfcc, order=2)

    for matrix in [mfcc, mfcc_delta, mfcc_delta2]:
        features.append(np.mean(matrix, axis=1))
        features.append(np.std(matrix,  axis=1))

    f0, voiced_flag, _ = librosa.pyin(
        audio,
        fmin=librosa.note_to_hz("C2"),
        fmax=librosa.note_to_hz("C7"),
        sr=sr
    )
    f0_voiced = f0[voiced_flag]
    features.append(np.array([
        np.mean(f0_voiced) if len(f0_voiced) > 0 else 0.0,
        np.std(f0_voiced)  if len(f0_voiced) > 0 else 0.0,
    ]))

    rms = librosa.feature.rms(y=audio)[0]
    features.append(np.array([np.mean(rms), np.std(rms)]))

    zcr = librosa.feature.zero_crossing_rate(audio)[0]
    features.append(np.array([np.mean(zcr), np.std(zcr)]))

    centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
    features.append(np.array([np.mean(centroid), np.std(centroid)]))

    rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr)[0]
    features.append(np.array([np.mean(rolloff), np.std(rolloff)]))

    return np.concatenate(features)

def parse_filename(filename):
    parts = filename.replace(".npy", "").split("_")
    label = int(parts[0])
    label_name = "non_dysarthric" if label == 0 else "dysarthric"
    return label, label_name

rows = []
files = [f for f in os.listdir(CLEANED_PATH) if f.endswith(".npy")]

print(f"Found {len(files)} files in '{CLEANED_PATH}'")
print("Extracting features...\n")

feat_vector = None

for filename in tqdm(files):
    filepath = os.path.join(CLEANED_PATH, filename)
    audio = np.load(filepath)

    if audio is None or len(audio) == 0 or np.max(np.abs(audio)) < 1e-4:
        print(f"  Skipping (silent/corrupt): {filename}")
        continue

    try:
        feat_vector = extract_features(audio)
    except Exception as e:
        print(f"  Error on {filename}: {e}")
        continue

    label, label_name = parse_filename(filename)
    row = {"filename": filename, "label": label, "label_name": label_name}
    for i, val in enumerate(feat_vector):
        row[f"feat_{i}"] = val
    rows.append(row)

df = pd.DataFrame(rows)
df.to_csv(OUTPUT_CSV, index=False)

print(f"\nDone. Extracted {len(df)} samples.")
if feat_vector is not None:
    print(f"Feature vector size: {len(feat_vector)} values per sample")
print(f"Label distribution:\n{df['label_name'].value_counts().to_string()}")
print(f"\nSaved to: {OUTPUT_CSV}")
