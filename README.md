# 🎙️ Voice Notes Summarizer

[Live Demo](https://voice-notes-summarizer-hkaxkgyj9zvv6zesunccfa.streamlit.app/)

A secure, **local voice transcription and summarization app** using OpenAI Whisper.

---

## Description

The **Voice Notes Summarizer** allows users to upload an audio file (MP3, WAV, M4A, FLAC, OGG) and perform **AI-powered transcription and summarization locally**.  

Here’s what happens in the app:

1. **Upload Audio:** Users select an audio file (max 10MB). The app validates the file.  
2. **Transcription:** The audio is processed with OpenAI Whisper locally, generating a text transcript.  
3. **Transcript Display & Download:** The transcription is shown in a text area, and users can download it as a `.txt` file.  
4. **Summarization:** Users select a summary length (Short, Medium, Detailed) and generate a concise summary of the transcript using the BART model.  
5. **Summary Display & Download:** The summary is displayed, and users can download it as a `.txt` file.  
6. **Reset Option:** Users can clear all uploaded data, transcript, and summary to start fresh.  

Everything happens **locally**, so no audio data is uploaded to external servers, ensuring privacy and security.

---

## Features

- Upload audio files (MP3, WAV, M4A, FLAC, OGG, max 10MB)  
- **Local transcription** – no external API calls  
- AI-powered summarization using BART  
- Multiple summary lengths: Short, Medium, Detailed  
- Download transcripts and summaries  
- **100% local processing** – your audio never leaves your computer  

> Recording feature coming soon!

---

## Setup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/Srijani-Das07/Voice-Notes-Summarizer.git
   cd Voice-Notes-Summarizer

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python -m streamlit run app.py`

### 🛡️ Security Features:
- ✅ **100% Local Processing** - All transcription happens on your machine
- ✅ **No API Keys Required** - No risk of key compromise
- ✅ **No External Data Transfer** - Your audio never leaves your computer  
- ✅ **Open Source Models** - Transparent and auditable code

*Recording feature coming soon!*
