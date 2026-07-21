import os
import numpy as np
import librosa
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# -----------------------------
# SETTINGS
# -----------------------------
data_root = "dataset"
sample_rate = 16000
max_duration = 2
max_length = sample_rate * max_duration

# Speaker-independent split
train_speakers = ["F01", "F03", "FC01", "FC02"]
test_speakers = ["F04", "FC03"]

X_train, y_train = [], []
X_test, y_test = [], []

print("Extracting features (Speaker-Independent Mode)...")

# -----------------------------
# LOAD DATA
# -----------------------------
for label_name in os.listdir(data_root):
    label_path = os.path.join(data_root, label_name)

    if not os.path.isdir(label_path):
        continue

    # Assign label
    if label_name == "non_dysarthric":
        label = 0
    elif label_name == "dysarthric":
        label = 1
    else:
        continue

    for speaker in os.listdir(label_path):
        speaker_path = os.path.join(label_path, speaker)

        if not os.path.isdir(speaker_path):
            continue

        for file in os.listdir(speaker_path):
            if file.endswith(".wav"):
                file_path = os.path.join(speaker_path, file)

                try:
                    audio, sr = librosa.load(file_path, sr=sample_rate)

                    # Fix length
                    if len(audio) > max_length:
                        audio = audio[:max_length]
                    else:
                        audio = np.pad(audio, (0, max_length - len(audio)))

                    # Extract MFCC
                    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
                    mfcc_mean = np.mean(mfcc.T, axis=0)

                    # Assign to train or test set
                    if speaker in train_speakers:
                        X_train.append(mfcc_mean)
                        y_train.append(label)
                    elif speaker in test_speakers:
                        X_test.append(mfcc_mean)
                        y_test.append(label)

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

print("Feature extraction complete.")
print("Train samples:", len(X_train))
print("Test samples:", len(X_test))

# Convert to numpy arrays
X_train = np.array(X_train)
y_train = np.array(y_train)
X_test = np.array(X_test)
y_test = np.array(y_test)

# -----------------------------
# TRAIN MODEL
# -----------------------------
print("\nTraining model (Speaker-Independent)...")

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# -----------------------------
# EVALUATION
# -----------------------------
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nSpeaker-Independent Accuracy:", round(accuracy * 100, 2), "%")
print("\nClassification Report:\n")
print(classification_report(
    y_test,
    y_pred,
    target_names=["Non-Dysarthric", "Dysarthric"]
))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)

plt.figure(figsize=(6,5))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Non-Dysarthric", "Dysarthric"],
    yticklabels=["Non-Dysarthric", "Dysarthric"]
)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Speaker-Independent Confusion Matrix")
plt.tight_layout()
plt.show()
import joblib

joblib.dump(model, "dysarthria_model.pkl")

print("Model saved successfully")