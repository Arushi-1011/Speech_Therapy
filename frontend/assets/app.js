let mediaRecorder;
let audioChunks = [];
let isRecording = false;

document.addEventListener('DOMContentLoaded', () => {
  if (!localStorage.getItem('patientName')) {
    window.location.href = 'index.html';
  }
});

async function toggleRecording() {
  if (!isRecording) {
    startRecording();
  } else {
    stopRecording();
  }
}

async function startRecording() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

  mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
  audioChunks = [];

  mediaRecorder.ondataavailable = (event) => {
    audioChunks.push(event.data);
  };

  mediaRecorder.onstop = sendAudioToBackend;

  mediaRecorder.start();
  isRecording = true;

  document.getElementById('recordBtn').textContent = 'Stop recording';
  document.getElementById('recordBtn').classList.add('recording');
  document.getElementById('recordStatus').textContent = 'Recording... speak now';
  animateWaveform(true);
}

function stopRecording() {
  mediaRecorder.stop();
  mediaRecorder.stream.getTracks().forEach(track => track.stop());
  isRecording = false;

  document.getElementById('recordBtn').textContent = 'Start recording';
  document.getElementById('recordBtn').classList.remove('recording');
  document.getElementById('recordStatus').textContent = 'Processing your speech...';
  animateWaveform(false);
}

function animateWaveform(active) {
  const bars = document.querySelectorAll('#waveform span');
  bars.forEach(bar => {
    if (active) {
      bar.classList.add('active');
    } else {
      bar.classList.remove('active');
    }
  });
}

async function sendAudioToBackend() {
  const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });

  const formData = new FormData();
  formData.append('audio', audioBlob, 'recording.webm');
  formData.append('patient_name', localStorage.getItem('patientName') || 'Anonymous');

  try {
    const response = await fetch('/analyse', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();
    showResults(data);

  } catch (error) {
    document.getElementById('recordStatus').textContent = 'Something went wrong. Please try again.';
    console.error(error);
  }
}

function showResults(data) {
  document.getElementById('resultsCard').classList.remove('hidden');
  document.getElementById('scoreNumber').textContent = data.intelligibility + '%';
  document.getElementById('confidenceVal').textContent = data.confidence + '%';
  document.getElementById('progressFill').style.width = data.intelligibility + '%';

  const circle = document.getElementById('scoreCircle');
  circle.classList.remove('score-high', 'score-mid', 'score-low');

  if (data.intelligibility >= 85) {
    circle.classList.add('score-high');
    document.getElementById('predictionText').textContent = 'Your speech is clear!';
    document.getElementById('predictionExplain').textContent = 'Great work. Keep practising daily to maintain this level.';
  } else if (data.intelligibility >= 70) {
    circle.classList.add('score-mid');
    document.getElementById('predictionText').textContent = 'Some areas to work on';
    document.getElementById('predictionExplain').textContent = 'Your speech is mostly clear. Targeted exercises will help further.';
  } else {
    circle.classList.add('score-low');
    document.getElementById('predictionText').textContent = "Let's work on this together";
    document.getElementById('predictionExplain').textContent = 'Your exercises have been customised for your speech pattern.';
  }

  document.getElementById('recordStatus').textContent = 'Analysis complete';
  document.getElementById('exerciseLink').href = 'exercises.html?score=' + data.intelligibility;
}