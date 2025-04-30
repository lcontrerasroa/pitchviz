import streamlit as st
import numpy as np
import parselmouth
import plotly.graph_objs as go
from scipy.signal import savgol_filter
import tempfile

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
        snd = parselmouth.Sound(tmp.name)

    # Extract pitch
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

    # Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=times,
        y=y_vals,
        mode='lines',
        line=dict(width=line_width, shape='spline', color='royalblue'),
        name='Pitch'
    ))
    fig.update_layout(
        title="Stylized Pitch Contour",
        xaxis_title="Time (s)",
        yaxis_title=y_label,
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Show transcript
    if transcript.strip():
        st.markdown("### Transcript")
        st.markdown(f"> {transcript.strip()}")

    # Audio playback
    st.audio(audio_file)
else:
    st.info("👈 Upload an audio file to begin.")
