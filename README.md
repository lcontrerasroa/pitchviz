# PITCHVIZ - Intonation Visualizer 🗣️🎵

This is a simple, interactive **Streamlit web app** designed for **teachers, researchers, and students** who want to explore **intonation contours** in short audio clips. It allows users to upload a brief speech recording, input a transcript manually, and visualize the **pitch contour** with several customizable settings.

---

## 🎯 Features

- 🔊 Upload audio (MP3 or WAV)
- ✍️ Paste transcript manually
- 📈 Automatic pitch extraction using [Praat](https://www.fon.hum.uva.nl/praat/) via `parselmouth`
- 📐 Smoothed pitch contour with options for stylization
- 🎛️ Interactive visualization with:
  - Silence threshold (to filter low, noisy pitch values)
  - Smoothing window size (controls how stylized the pitch contour looks)
  - Line width (thicker or thinner pitch curve)
  - Pitch normalization (to show pitch in semitones relative to median pitch)
- 🎧 Built-in audio playback
- 📜 Transcript display below the curve

---

## 🧪 Example Use Cases
- Teaching English intonation patterns (e.g., rising questions, falling statements)
- Exploring speech melody in sociolinguistic fieldwork
- Demonstrating pitch variation in multilingual contexts
- Rapid prosodic feedback in pronunciation training

---

## 🚀 How to Run It

### Locally
```bash
pip install -r requirements.txt
streamlit run pitchviz.py
```

### On Streamlit Cloud
1. Upload or push this folder to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Create a new app from the GitHub repo
4. Streamlit Cloud will install dependencies and launch the app!

---

## 📦 Requirements
### For frontend
pip install -r requirements-streamlit.txt

### For backend (Render uses this one)
Dockerfile + requirements.txt


---

## 📌 Notes
- This version assumes **manual transcription**. Alignment with automatic word-level timestamps (e.g., WhisperX or MFA) is planned for future versions.
- For best results, use clear audio snippets under 10 seconds.

---

## ✨ Future Ideas
- Word-level time alignment
- Highlight current pitch position during playback
- Export contour data for further research (CSV or JSON)
- Compare intonation across speakers/languages
- Multilingual UI for classroom use

---

Made with ❤️ by a linguist-developer with *loads of help from ChatGPT*. For educators and researchers.
