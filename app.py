import streamlit as st
import whisper
import os

# 1. Page Configuration
st.set_page_config(page_title="Akib's AI Transcriber", page_icon="🪄", layout="wide")

# Custom CSS for Professional UI & Image Styling
st.markdown("""
    <style>
    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        color: white;
    }
    
    /* Profile Image Styling - Circular with Neon Glow */
    .profile-container {
        display: flex;
        justify-content: center;
        padding: 10px;
    }
    
    .profile-img {
        width: 160px;
        height: 160px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #4ade80;
        box-shadow: 0 0 25px rgba(74, 222, 128, 0.6);
    }

    .neon-text {
        color: #4ade80;
        text-shadow: 0 0 10px rgba(74, 222, 128, 0.5);
        font-weight: bold;
        text-align: center;
        font-size: 1.4em;
        margin-top: 10px;
    }

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
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 15px rgba(22, 163, 74, 0.3);
        transition: 0.3s;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar with your Specific Photo Name
with st.sidebar:
    st.markdown('<p class="neon-text">AKIB AI HUB</p>', unsafe_allow_html=True)
    
    # Updated logic for your specific file name
    photo_path = "my_photo.jpg.png"
    
    if os.path.exists(photo_path):
        # Image ko center karne ke liye columns ka use
        col_img1, col_img2, col_img3 = st.columns([1, 4, 1])
        with col_img2:
            st.image(photo_path, use_container_width=True)
    else:
        # Fallback agar file nahi milti
        st.warning("Photo not found. Make sure 'my_photo.jpg.png' is in your GitHub repo.")
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    
    st.markdown("<h3 style='text-align: center; margin-bottom: 0;'>Akib</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>B.Sc. IT Developer</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    st.markdown("""
    <div class="sidebar-card">
        <p style='color: #4ade80; font-weight: bold; margin-bottom: 5px;'>🚀 Tool Stats</p>
        <p style='font-size: 0.9em; margin: 0;'>• Engine: Whisper AI</p>
        <p style='font-size: 0.9em; margin: 0;'>• Status: Online ✅</p>
    </div>
    <div class="sidebar-card">
        <p style='color: #4ade80; font-weight: bold; margin-bottom: 5px;'>🛠️ Support</p>
        <p style='font-size: 0.8em;'>Contact Akib for custom AI solutions.</p>
    </div>
    """, unsafe_allow_html=True)

# 3. Main Interface
st.markdown("<h1 style='text-align: center;'>🪄 Akib's AI Media Transcriber</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.write("")
    uploaded_file = st.file_uploader("", type=["mp4", "mkv", "mov", "mp3", "wav", "m4a", "flac"])

    if uploaded_file is not None:
        file_ext = os.path.splitext(uploaded_file.name)[1]
        temp_name = f"temp_input{file_ext}"

        with st.spinner('✨ Akib\'s AI is magic in progress...'):
            try:
                with open(temp_name, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                model = whisper.load_model("tiny")
                result = model.transcribe(temp_name, fp16=False, task="transcribe")
                
                st.balloons()
                st.success(f"✅ Completed! Language: {result.get('language', 'unknown').upper()}")
                
                tab1, tab2 = st.tabs(["📄 Transcription", "ℹ️ File Info"])
                with tab1:
                    st.text_area("Result:", value=result["text"], height=300)
                    st.download_button("📥 Download Result", data=result["text"], file_name=f"{uploaded_file.name}_by_Akib.txt")
                with tab2:
                    st.write(f"**Filename:** {uploaded_file.name}")
                    st.write(f"**Model:** Whisper Tiny")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                if os.path.exists(temp_name): os.remove(temp_name)
    else:
        st.info("👋 Hello! Upload a file to start transcribing.")

st.write("---")
st.markdown("<p style='text-align: center; color: #94a3b8;'>© 2026 Akib Developer</p>", unsafe_allow_html=True)
