import streamlit as st
import numpy as np
import parselmouth
import plotly.graph_objs as go
from scipy.signal import savgol_filter
import tempfile
import requests

st.set_page_config(page_title="Intonation Visualizer", layout="centered")
st.title("🎵 Intonation Visualizer for Teachers & Researchers")

# === Upload audio ===
audio_file = st.file_uploader("Upload a short audio file (WAV or MP3)", type=["wav", "mp3"])

# === Transcript ===
transcript = st.text_area("Paste the corresponding transcript here:")

# === Controls ===
st.sidebar.header("Visualization Options")
silence_threshold = st.sidebar.slider("Silence threshold (Hz)", 50, 200, 100, 10)
smoothing_window = st.sidebar.slider("Smoothing window size (odd only)", 5, 61, 31, 2)
line_width = st.sidebar.slider("Pitch line width", 1, 10, 4)
normalize = st.sidebar.checkbox("Normalize pitch to semitones", value=True)

if audio_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=audio_file.name) as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name

    # Load with parselmouth
    snd = parselmouth.Sound(tmp_path)
    pitch = snd.to_pitch()
    times = pitch.xs()
    freqs = pitch.selected_array['frequency']
    freqs = np.where(freqs < silence_threshold, np.nan, freqs)

    # Smooth pitch
    valid = ~np.isnan(freqs)
    smoothed = freqs.copy()
    if valid.sum() > smoothing_window:
        smoothed[valid] = savgol_filter(freqs[valid], smoothing_window | 1, 2)

    # Normalize
    if normalize:
        f0_ref = np.nanmedian(smoothed)
        y_vals = 12 * np.log2(smoothed / f0_ref)
        y_label = "Pitch (semitones relative to median)"
    else:
        y_vals = smoothed
        y_label = "Pitch (Hz)"

    # === Send to alignment backend ===
    st.markdown("---")
    st.subheader("⏱️ Aligned Transcript")
    if transcript.strip():
        with open(tmp_path, "rb") as f:
            files = {"audio": (audio_file.name, f, audio_file.type)}
            data = {"transcript": transcript}
            try:
                # Replace with your actual backend URL
                backend_url = "https://your-backend-url.onrender.com/align"
                response = requests.post(backend_url, files=files, data=data)
                if response.ok:
                    segments = response.json().get("segments", [])
                else:
                    segments = []
                    st.error("Alignment failed: " + response.text)
            except Exception as e:
                segments = []
                st.error(f"Error contacting backend: {e}")
    else:
        segments = []
        st.warning("Please paste a transcript above.")

    # === Plot pitch and overlay alignment ===
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=times,
        y=y_vals,
        mode='lines',
        line=dict(width=line_width, shape='spline', color='royalblue'),
        name='Pitch'
    ))

    if segments:
        for seg in segments:
            x0, x1 = seg["start"], seg["end"]
            text = seg["text"]
            fig.add_shape(
                type='rect', x0=x0, x1=x1,
                y0=min(y_vals[np.isfinite(y_vals)]), y1=max(y_vals[np.isfinite(y_vals)]),
                fillcolor='rgba(200,200,255,0.1)', line=dict(width=0), layer='below')
            fig.add_annotation(
                x=(x0 + x1) / 2, y=max(y_vals[np.isfinite(y_vals)]) + 1,
                text=text, showarrow=False, font=dict(size=11))

    fig.update_layout(
        title="Stylized Pitch Contour with Aligned Transcript",
        xaxis_title="Time (s)",
        yaxis_title=y_label,
        height=420
    )
    st.plotly_chart(fig, use_container_width=True)

    # Audio playback
    st.audio(audio_file)
else:
    st.info("👈 Upload an audio file to begin.")
