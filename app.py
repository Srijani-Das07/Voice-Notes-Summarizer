import streamlit as st
import tempfile
import whisper
from transformers import pipeline
import torch
import os

# ------------------- Page Configuration -------------------
st.set_page_config(page_title="Voice Notes Summarizer", layout="wide")

# ------------------- Load CSS -------------------
def load_css(file_name):
    try:
        with open(file_name, 'r') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # Fallback minimal styling if CSS file not found
        st.markdown("""
        <style>
        .stApp { background: linear-gradient(-45deg, #000510, #001122); }
        </style>
        """, unsafe_allow_html=True)

load_css('animated_styles.css')

# ------------------- Configuration -------------------
CONFIG = {
    'MAX_FILE_SIZE': 10 * 1024 * 1024,
    'SUPPORTED_FORMATS': {'.mp3', '.wav', '.m4a', '.flac', '.ogg'}
}

# ------------------- Session State -------------------
if "transcription" not in st.session_state:
    st.session_state.transcription = None
if "summary" not in st.session_state:
    st.session_state.summary = None
if "summary_type" not in st.session_state:
    st.session_state.summary_type = None

# ------------------- Load Models -------------------
@st.cache_resource
def load_whisper_model():
    """Load Whisper model (cached for performance)"""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("base", device=device)
    return model

@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

# Load models quietly (only show spinner on first load)
if 'models_loaded' not in st.session_state:
    with st.spinner("Loading AI models... (this may take a minute on first run)"):
        whisper_model = load_whisper_model()
        summarizer = load_summarizer()
    st.session_state.models_loaded = True
else:
    whisper_model = load_whisper_model()
    summarizer = load_summarizer()

# ------------------- Functions -------------------
def summarize_text(text, summary_type="Medium"):
    if summary_type == "Short":
        out = summarizer(text, max_length=100, min_length=20, do_sample=False)
    elif summary_type == "Medium":
        out = summarizer(text, max_length=200, min_length=40, do_sample=False)
    else:  # Detailed
        out = summarizer(text, max_length=500, min_length=80, do_sample=False)

    return out[0]['summary_text']

def transcribe_audio_whisper(uploaded_file):
    """Transcription function using local Whisper model"""
    tmp_path = None
    
    try:
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        
        # Create temp file with correct extension
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        
        # Validate file
        if not os.path.exists(tmp_path) or os.path.getsize(tmp_path) == 0:
            st.error("⚠️ Audio file is empty or corrupted")
            return None
        
        # Transcribe with local Whisper        
        result = whisper_model.transcribe(
            tmp_path,
            language=None,
            task="transcribe",
            verbose=False
        )
        
        transcript_text = result["text"]
        
        if not transcript_text or transcript_text.strip() == "":
            st.warning("⚠️ No speech detected - audio might be too quiet or unclear")
            return None
        return transcript_text.strip()
            
    except Exception as e:
        st.error(f"⚠️ Transcription error: {e}")
        return None
    
    finally:
        # Clean up temporary files
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except:
                pass

# ------------------- Streamlit UI -------------------
st.title("🎙️ Voice Notes Summarizer")
st.markdown("**Upload an audio file to get an AI-powered transcript and summary**")

# Clean, minimal info section
with st.expander("ℹ️ App Info", expanded=False):
    device = "GPU" if torch.cuda.is_available() else "CPU"
    st.write(f"• Processing on: **{device}**")
    st.write("• 100% local processing - no data sent to external servers")
    st.write("• Supported formats: MP3, WAV, M4A, FLAC, OGG (max 10MB)")

# Step 1: Upload
st.subheader("Step 1: Upload Audio")
uploaded_file = st.file_uploader(
    "Choose an audio file", 
    type=["mp3", "wav", "m4a", "flac", "ogg"],
    help="Maximum file size: 10MB"
)

# Only shows file info if file is uploaded
if uploaded_file:
    if uploaded_file.size > CONFIG['MAX_FILE_SIZE']:
        st.error("⚠️ File too large! Maximum size is 10MB.")
        st.stop()
    else:
        file_size = uploaded_file.size / 1024 / 1024
        st.success(f"✅ **{uploaded_file.name}** ({file_size:.1f} MB)")

# Step 2: Transcribe (only shows if file uploaded)
if uploaded_file:
    st.subheader("Step 2: Get Transcript")
    
    if st.button("🎯 Transcribe Audio", type="primary", use_container_width=True):
        with st.spinner("Processing audio..."):
            st.session_state.transcription = transcribe_audio_whisper(uploaded_file)
            if st.session_state.transcription:
                char_count = len(st.session_state.transcription)
                st.success(f"✅ Transcript ready! ({char_count} characters)")

# Display Transcript (only if exists)
if st.session_state.transcription:
    st.subheader("📝 Transcript")
    
    # Clean transcript display
    with st.container():
        st.text_area(
            "Transcript text:",
            value=st.session_state.transcription,
            height=200,
            disabled=True,
            label_visibility="collapsed"
        )
        
        st.download_button(
            "📥 Download Transcript", 
            st.session_state.transcription, 
            "transcript.txt",
            mime="text/plain",
            use_container_width=True
        )

    # Step 3: Summarize
    st.subheader("Step 3: Generate Summary")
    
    summary_type = st.selectbox("Summary length:", ["Short", "Medium", "Detailed"])
    generate_summary = st.button("✨ Summarize", type="secondary", use_container_width=True)
    
    if generate_summary:
        with st.spinner("Generating summary..."):
            st.session_state.summary = summarize_text(st.session_state.transcription, summary_type)
            st.session_state.summary_type = summary_type

# Display Summary (only if exists)
if st.session_state.summary:
    st.subheader("📋 Summary")
    
    with st.container():
        st.text_area(
            "Summary text:",
            value=st.session_state.summary,
            height=200,
            disabled=True,
            label_visibility="collapsed"
        )
        
        st.download_button(
            "📥 Download Summary", 
            st.session_state.summary, 
            f"summary_{st.session_state.get('summary_type', 'medium').lower()}.txt",  # Use stored value
            mime="text/plain",
            use_container_width=True
        )

# Reset button (only shows if there's something to reset)
if st.session_state.transcription or st.session_state.summary:
    st.divider()
    if st.button("🔄 Reset All", help="Clear all results and start fresh"):
        for key in ['transcription', 'summary', 'summary_type']:  
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

