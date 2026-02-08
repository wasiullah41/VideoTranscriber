import streamlit as st
import whisper
import os

# 1. Page Configuration
st.set_page_config(page_title="Akib's AI Transcriber", page_icon="🎙️", layout="wide")

# Custom CSS for a Professional & Attractive UI
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(to right, #f8f9fa, #e9ecef);
    }
    
    /* Custom Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background-color: #2e7d32;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        transform: scale(1.02);
    }

    /* Text Area Styling */
    .stTextArea>div>div>textarea {
        border-radius: 15px;
        border: 2px solid #2e7d32;
        background-color: #ffffff;
    }

    /* Success Message Styling */
    .stSuccess {
        background-color: #e8f5e9;
        border: 1px solid #2e7d32;
        border-radius: 10px;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1a1a1a;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar - Branding & Instructions
with st.sidebar:
    st.markdown(f"<h2 style='text-align: center; color: #4CAF50;'>Developer: Akib</h2>", unsafe_allow_html=True)
    st.write("---")
    st.info("🚀 **Tool Capabilities:**\n- Video & Audio Support\n- Fast AI Processing\n- Original Language Output\n- Instant Download")
    st.write("---")
    st.markdown("### 🛠️ Help")
    st.write("Just upload your file and let the AI do the magic. For any issues, contact Akib.")

# 3. Main Interface Header
st.markdown("<h1 style='text-align: center; color: #1b5e20;'>🎙️ Akib's AI Media Transcriber</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em;'>The smartest way to convert your Audio & Video to Text.</p>", unsafe_allow_html=True)

# Layout: Center the Uploader
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.write("---")
    uploaded_file = st.file_uploader("Drop your video or audio here 👇", type=["mp4", "mkv", "mov", "mp3", "wav", "m4a", "flac"])

    if uploaded_file is not None:
        file_extension = os.path.splitext(uploaded_file.name)[1]
        temp_filename = f"temp_media_input{file_extension}"

        with st.spinner('✨ Akib\'s AI is processing your media...'):
            try:
                # Saving uploaded file
                with open(temp_filename, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Loading Fast AI Model
                model = whisper.load_model("tiny")
                
                # Transcription Process
                result = model.transcribe(temp_filename, fp16=False, task="transcribe")
                
                full_text = result["text"]
                detected_lang = result.get("language", "unknown").upper()

                # Success Celebration
                st.balloons()
                st.success(f"✅ Done! Language Detected: **{detected_lang}**")
                
                # Tabs for Organized Output
                tab1, tab2 = st.tabs(["📄 Transcription Result", "📊 File Info"])
                
                with tab1:
                    st.text_area("Original Text Content:", value=full_text, height=350)
                    st.download_button(
                        label="📥 Download This Transcription",
                        data=full_text,
                        file_name=f"{os.path.splitext(uploaded_file.name)[0]}_by_Akib.txt",
                        mime="text/plain"
                    )
                
                with tab2:
                    st.write(f"**Filename:** {uploaded_file.name}")
                    st.write(f"**Detected Language:** {detected_lang}")
                    st.write(f"**AI Model:** Whisper-Tiny (Fast Mode)")
                    st.write("**Processed by:** Akib's AI Engine")

            except Exception as e:
                st.error(f"Error: {e}")
            
            finally:
                # Cleanup to keep server light
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
    else:
        st.write("")
        st.warning("Waiting for your media file to start...")

# 4. Footer
st.write("---")
st.markdown("<p style='text-align: center; color: grey;'>© 2026 | Designed & Developed by <b>Akib</b></p>", unsafe_allow_html=True)

