# 🎙️ Voice Notes Summarizer

Voice Notes Summarizer converts audio files into full transcriptions and AI-generated summaries. Summaries can be generated in Short, Medium, or Detailed lengths. Both the transcript and summary can be downloaded as text files. All processing is performed on the device, ensuring audio privacy without requiring API keys or external servers.

## How It Works

Step-by-step process:

1. **Upload Audio:** Select a file in MP3, WAV, M4A, FLAC, or OGG format.  
2. **Transcription:** Convert audio to text using OpenAI Whisper.  
3. **Generate Summary:** Choose a summary length and generate a concise AI-powered summary with HuggingFace BART.  
4. **Download Results:** Save both the transcript and the summary as text files.  
5. **Reset (Optional):** Clear all results and start over.

## Tech Stack

| **Feature/Component**        | **Technology Used**                       |
|--------------------------|--------------------------------------|
| Programming Language      | Python                               |
| Web Interface             | Streamlit                            |
| Speech Recognition        | OpenAI Whisper                       |
| Text Summarization        | HuggingFace BART                     |
| Framework                 | PyTorch                              |

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/Srijani-Das07/Voice-Notes-Summarizer.git
    cd Voice-Notes-Summarizer
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the app:
    ```bash
    python -m streamlit run app.py
    ```

## Security & Privacy

- ✅ All processing happens locally on the device.
- ✅ No API keys or external services are required.  
- ✅ Open source models ensure transparency and auditability.  

## Future Features

- Record audio directly in the browser.  
- Translate transcriptions into multiple languages.

## Author 

[Srijani Das](https://github.com/Srijani-Das07)

## License

This project is licensed under the [MIT LICENSE](LICENSE)

