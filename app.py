import gradio as gr
import numpy as np
import librosa
import joblib
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime

model = joblib.load("dysarthria_model_v2.pkl")
scaler = joblib.load("scaler.pkl")
SAMPLE_RATE = 16000
N_MFCC = 40

def init_db():
    conn = sqlite3.connect("sessions.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            patient_name TEXT,
            prediction TEXT,
            confidence REAL,
            intelligibility REAL,
            num_errors INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

def save_session(name, prediction, confidence, intelligibility, num_errors):
    conn = sqlite3.connect("sessions.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO sessions (timestamp,patient_name,prediction,confidence,intelligibility,num_errors) VALUES (?,?,?,?,?,?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, prediction, confidence, intelligibility, num_errors)
    )
    conn.commit()
    conn.close()

def get_history(name):
    conn = sqlite3.connect("sessions.db")
    df = pd.read_sql_query(
        "SELECT * FROM sessions WHERE patient_name=? ORDER BY timestamp DESC LIMIT 10",
        conn, params=(name,)
    )
    conn.close()
    return df

def extract_features(audio, sr=SAMPLE_RATE):
    features = []
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=N_MFCC)
    mfcc_delta = librosa.feature.delta(mfcc)
    mfcc_delta2 = librosa.feature.delta(mfcc, order=2)
    for matrix in [mfcc, mfcc_delta, mfcc_delta2]:
        features.append(np.mean(matrix, axis=1))
        features.append(np.std(matrix, axis=1))
    f0 = librosa.yin(audio, fmin=65, fmax=2093, sr=sr)
    f0_voiced = f0[f0 > 0]
    features.append(np.array([
        np.mean(f0_voiced) if len(f0_voiced) > 0 else 0.0,
        np.std(f0_voiced) if len(f0_voiced) > 0 else 0.0,
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

def plot_waveform(audio, sr, error_segments, intelligibility, prediction):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
    fig.patch.set_facecolor("#1a1a2e")
    time_axis = np.linspace(0, len(audio)/sr, len(audio))
    color = "#e94560" if prediction == "Dysarthric" else "#0f3460"
    ax1.plot(time_axis, audio, color=color, linewidth=0.6, alpha=0.9)
    for (t_start, t_end) in error_segments:
        ax1.axvspan(t_start, t_end, color="red", alpha=0.35)
    ax1.set_facecolor("#16213e")
    ax1.set_title(f"Waveform - {prediction} | Intelligibility: {intelligibility}%", color="white", fontsize=12)
    ax1.set_xlabel("Time (s)", color="white")
    ax1.set_ylabel("Amplitude", color="white")
    ax1.tick_params(colors="white")
    p1 = mpatches.Patch(color=color, label="Speech signal")
    p2 = mpatches.Patch(color="red", alpha=0.4, label="Uncertain region")
    ax1.legend(handles=[p1, p2], facecolor="#1a1a2e", labelcolor="white", fontsize=9)
    bar_color = "#e94560" if intelligibility < 70 else "#f5a623" if intelligibility < 85 else "#4caf50"
    ax2.barh(["Intelligibility"], [intelligibility], color=bar_color, height=0.4)
    ax2.barh(["Intelligibility"], [100 - intelligibility], left=[intelligibility], color="#333355", height=0.4)
    ax2.set_xlim(0, 100)
    ax2.set_facecolor("#16213e")
    ax2.set_title("Speech Clarity Score", color="white", fontsize=12)
    ax2.tick_params(colors="white")
    ax2.text(intelligibility + 1, 0, f"{intelligibility}%", va="center", color="white", fontsize=11)
    plt.tight_layout()
    plt.savefig("waveform_output.png", dpi=130, bbox_inches="tight", facecolor="#1a1a2e")
    plt.close()
    return "waveform_output.png"

def get_exercises(prediction, intelligibility, num_errors):
    if prediction == "Non-Dysarthric":
        return "Speech patterns appear normal. Keep practising clear articulation daily!"
    exercises = ["Recommended Speech Exercises:\n"]
    if intelligibility < 70:
        exercises.append("1. Slow Speech Drill - speak 30% slower, 10 mins/day")
        exercises.append("2. Exaggerated Articulation - over-pronounce each word")
        exercises.append("3. Breath Support - deep breath before each sentence")
    elif intelligibility < 85:
        exercises.append("1. Tongue Twisters - She sells seashells x5 daily")
        exercises.append("2. Vowel Prolongation - hold each vowel for 5 seconds")
        exercises.append("3. Pitch Variation - read a sentence going high then low")
    else:
        exercises.append("1. Reading Aloud - read a paragraph clearly, 15 mins/day")
        exercises.append("2. Conversation Practice - record and listen back daily")
        exercises.append("3. Facial Muscle Warm-up - lip trills and tongue stretches")
    if num_errors > 3:
        exercises.append("4. Phoneme Targeting - focus on isolated consonant sounds")
    return "\n".join(exercises)

def analyse_audio(audio_input, patient_name):
    if audio_input is None:
        return None, "No audio provided.", "", ""
    if not patient_name.strip():
        patient_name = "Anonymous"
    sr, audio_data = audio_input
    audio = audio_data.astype(np.float32)
    if audio.max() > 1.0:
        audio = audio / 32768.0
    if len(audio.shape) > 1:
        audio = audio.mean(axis=1)
    if sr != SAMPLE_RATE:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=SAMPLE_RATE)
    target_len = SAMPLE_RATE * 2
    if len(audio) > target_len:
        audio = audio[:target_len]
    else:
        audio = np.pad(audio, (0, target_len - len(audio)))
    try:
        features = extract_features(audio)
        features_scaled = scaler.transform(features.reshape(1, -1))
        prediction_idx = model.predict(features_scaled)[0]
        prediction = "Dysarthric" if prediction_idx == 1 else "Non-Dysarthric"
        proba = model.predict_proba(features_scaled)[0]
        confidence = round(float(max(proba)) * 100, 1)
    except Exception as e:
        return None, f"Error: {e}", "", ""
    rms = librosa.feature.rms(y=audio)[0]
    rms_cv = np.std(rms) / (np.mean(rms) + 1e-8)
    base_score = max(0, min(100, 100 - rms_cv * 200))
    if prediction == "Dysarthric":
        base_score = base_score * 0.75
    intelligibility = round(base_score, 1)
    threshold = np.mean(rms) * 0.3
    error_segments = []
    in_error = False
    frame_dur = 512 / SAMPLE_RATE
    start = 0
    for i, e in enumerate(rms):
        t = i * frame_dur
        if e < threshold and not in_error:
            start = t
            in_error = True
        elif e >= threshold and in_error:
            if t - start > 0.05:
                error_segments.append((round(start, 3), round(t, 3)))
            in_error = False
    num_errors = len(error_segments)
    plot_path = plot_waveform(audio, SAMPLE_RATE, error_segments, intelligibility, prediction)
    exercises = get_exercises(prediction, intelligibility, num_errors)
    save_session(patient_name, prediction, confidence, intelligibility, num_errors)
    result_text = f"""Patient: {patient_name}
    Prediction: {prediction}
Model Confidence: {confidence}%
Intelligibility Score: {intelligibility}%
Error Segments Detected: {num_errors}
Analysed At: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"""
    history_df = get_history(patient_name)
    if len(history_df) > 1:
        history_text = "Your Recent Sessions:\n"
        for _, row in history_df.iterrows():
            history_text += f"- {row['timestamp']} | {row['prediction']} | Score: {row['intelligibility']}%\n"
    else:
        history_text = "First session recorded! Keep practising to track your progress."
    return plot_path, result_text, exercises, history_text

with gr.Blocks(title="Speech Therapy Assistant", theme=gr.themes.Soft()) as app:
    gr.Markdown("# Speech Therapy Assistant\n### Dysarthria Detection and Speech Feedback System")
    with gr.Row():
        with gr.Column(scale=1):
            patient_name = gr.Textbox(label="Patient Name", placeholder="Enter your name...", value="Patient")
            audio_input = gr.Audio(label="Record or Upload Voice Sample", type="numpy", sources=["microphone", "upload"])
            analyse_btn = gr.Button("Analyse Speech", variant="primary", size="lg")
        with gr.Column(scale=2):
            waveform_plot = gr.Image(label="Waveform and Intelligibility Score")
            result_text = gr.Markdown(label="Analysis Result")
    with gr.Row():
        with gr.Column():
            exercises_out = gr.Markdown(label="Therapy Exercises")
        with gr.Column():
            history_out = gr.Markdown(label="Session History")
    analyse_btn.click(
        fn=analyse_audio,
        inputs=[audio_input, patient_name],
        outputs=[waveform_plot, result_text, exercises_out, history_out]
    )
    gr.Markdown("---\n*Built with TORGO Dataset | Wav2Vec2 | XGBoost | Gradio*")

if name == "main":
    app.launch(share=True)
