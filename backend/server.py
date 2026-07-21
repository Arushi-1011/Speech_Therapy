from flask import Flask, request, jsonify, send_from_directory
import io
import sqlite3
import os
import soundfile as sf
from pydub import AudioSegment

from app_logic import analyse_audio

app = Flask(__name__)

# Serve frontend files
@app.route('/')
def index():
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_path, 'index.html')

@app.route('/<path:filename>')
def serve_frontend(filename):
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_path, filename)

@app.route('/analyse', methods=['OPTIONS'])
def analyse_options():
    return '', 204

@app.route('/history', methods=['OPTIONS'])
def history_options():
    return '', 204

@app.route("/analyse", methods=["POST"])
def analyse():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file received"}), 400

    audio_file = request.files["audio"]
    patient_name = request.form.get("patient_name", "Anonymous")

    try:
        webm_bytes = audio_file.read()
        webm_audio = AudioSegment.from_file(io.BytesIO(webm_bytes), format="webm")
        wav_buffer = io.BytesIO()
        webm_audio.export(wav_buffer, format="wav")
        wav_buffer.seek(0)
        audio_data, sr = sf.read(wav_buffer)
    except Exception as e:
        return jsonify({"error": f"Could not read audio file: {e}"}), 400

    audio_input = (sr, audio_data)

    plot_path, result_text, exercises, history_text = analyse_audio(audio_input, patient_name)

    if plot_path is None:
        return jsonify({"error": result_text}), 500

    parsed = parse_result_text(result_text)

    return jsonify({
        "prediction": parsed.get("prediction", "Unknown"),
        "confidence": parsed.get("confidence", 0),
        "intelligibility": parsed.get("intelligibility", 0),
        "num_errors": parsed.get("num_errors", 0),
        "exercises": exercises,
        "history": history_text
    })

def parse_result_text(text):
    lines = [l.strip() for l in text.strip().split("\n")]
    data = {}
    for line in lines:
        if line.startswith("Prediction:"):
            data["prediction"] = line.replace("Prediction:", "").strip()
        elif line.startswith("Model Confidence:"):
            data["confidence"] = float(line.replace("Model Confidence:", "").replace("%", "").strip())
        elif line.startswith("Intelligibility Score:"):
            data["intelligibility"] = float(line.replace("Intelligibility Score:", "").replace("%", "").strip())
        elif line.startswith("Error Segments Detected:"):
            data["num_errors"] = int(line.replace("Error Segments Detected:", "").strip())
    return data

@app.route("/history", methods=["GET"])
def history():
    patient_name = request.args.get("patient_name", "")
    if not patient_name:
        return jsonify({"error": "No patient name provided"}), 400

    conn = sqlite3.connect("sessions.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(
        "SELECT timestamp, prediction, confidence, intelligibility, num_errors FROM sessions WHERE patient_name=? ORDER BY timestamp ASC",
        (patient_name,)
    )
    rows = c.fetchall()
    conn.close()

    sessions = [dict(row) for row in rows]
    return jsonify({"sessions": sessions})

if __name__ == "__main__":
    app.run(debug=True, port=5000)