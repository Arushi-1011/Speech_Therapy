import gradio as gr
from app_logic import analyse_audio

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

if __name__ == "__main__":
    app.launch(share=True)