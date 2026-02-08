import streamlit as st
import whisper
import os

# 1. Page Configuration
st.set_page_config(page_title="Akib's AI Transcriber", page_icon="🪄", layout="wide")

# Custom CSS for "Real" & Modern UI
st.markdown("""
    <style>
    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        color: white;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Neon Text for Name */
    .neon-text {
        color: #4ade80;
        text-shadow: 0 0 10px rgba(74, 222, 128, 0.5);
        font-weight: bold;
        text-align: center;
        font-size: 1.5em;
    }

    /* Professional Sidebar Cards */
    .sidebar-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Main UI Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: linear-gradient(90deg, #22c55e 0%, #16a34a 100%);
        color: white;
        border: none;
        box-shadow: 0 4px 15px rgba(22, 163, 74, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(22, 163, 74, 0.4);
    }

    /* Text Area Styling */
    .stTextArea>div>div>textarea {
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Advanced Sidebar
with st.sidebar:
    # Developer Branding
    st.markdown('<p class="neon-text">AKIB AI HUB</p>', unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80) # Placeholder profile icon
    st.markdown("<h3 style='text-align: center;'>Akib</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>B.Sc. IT Developer</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    # Tool Capabilities Card
    st.markdown("""
    <div class="sidebar-card">
        <p style='color: #4ade80; font-weight: bold; margin-bottom: 5px;'>🚀 Tool Stats</p>
        <p style='font-size: 0.9em; margin: 0;'>• Engine: Whisper AI</p>
        <p style='font-size: 0.9em; margin: 0;'>• Latency: Ultra-Low</p>
        <p style='font-size: 0.9em; margin: 0;'>• Status: Online ✅</p>
    </div>
    """, unsafe_allow_html=True)

    # Support Section
    st.markdown("""
    <div class="sidebar-card">
        <p style='color: #4ade80; font-weight: bold; margin-bottom: 5px;'>🛠️ Support</p>
        <p style='font-size: 0.8em;'>Need help with your project? Contact Akib for custom AI solutions.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("---")
    st.caption("Version 2.0.1 | Built with ❤️")

# 3. Main Interface Header
st.markdown("<h1 style='text-align: center;'>🪄 Akib's AI Media Transcriber</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>Convert any Video or Audio to text instantly using state-of-the-art AI.</p>", unsafe_allow_html=True)

# Layout: Center the Uploader
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.write("")
    uploaded_file = st.file_uploader("", type=["mp4", "mkv", "mov", "mp3", "wav", "m4a", "flac"])

    if uploaded_file is not None:
        file_extension = os.path.splitext(uploaded_file.name)[1]
        temp_filename = f"temp_media_input{file_extension}"

        with st.spinner('✨ Akib\'s AI is magic in progress...'):
            try:
                with open(temp_filename, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                model = whisper.load_model("tiny")
                result = model.transcribe(temp_filename, fp16=False, task="transcribe")
                
                full_text = result["text"]
                detected_lang = result.get("language", "unknown").upper()

                st.balloons()
                st.success(f"✅ Transcription Complete! Language: **{detected_lang}**")
                
                tab1, tab2 = st.tabs(["📄 Text Result", "ℹ️ File Details"])
                
                with tab1:
                    st.text_area("Result:", value=full_text, height=350)
                    st.download_button(
                        label="📥 Download TXT File",
                        data=full_text,
                        file_name=f"{os.path.splitext(uploaded_file.name)[0]}_by_Akib.txt",
                        mime="text/plain"
                    )
                
                with tab2:
                    st.json({
                        "File Name": uploaded_file.name,
                        "Detected Language": detected_lang,
                        "AI Model": "Whisper Tiny v2",
                        "Developer": "Akib"
                    })

            except Exception as e:
                st.error(f"Error: {e}")
            
            finally:
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
    else:
        st.info("👋 Welcome! Please upload a file to begin.")

# 4. Footer
st.write("---")
st.markdown("<p style='text-align: center; color: #94a3b8;'>© 2026 Akib Developer | All Rights Reserved</p>", unsafe_allow_html=True)
