import streamlit as st
import whisper
import os
import base64

# 1. Page Configuration
st.set_page_config(page_title="Wasiullah's AI Hub", page_icon="🪄", layout="wide")

# Base64 Image Loader
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

img_base64 = get_base64_image("my_photo.jpg.png")

# Advanced Custom CSS for SaaS Look
st.markdown(f"""
    <style>
    /* Main Background */
    .stApp {{
        background-color: #f8fafc;
    }}

    /* Premium Sidebar */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #1e1b4b 0%, #312e81 100%);
        color: white;
        border-right: 2px solid #4ade80;
    }}
    
    /* Circular Profile Image */
    .profile-container {{
        text-align: center;
        margin-top: 20px;
    }}
    .circle-img {{
        width: 160px;
        height: 160px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #4ade80;
        box-shadow: 0 0 25px rgba(74, 222, 128, 0.4);
    }}

    /* Sidebar Cards */
    .sidebar-card {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}

    /* Modern Contact Form */
    .contact-container {{
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }}
    .contact-input {{
        width: 100%;
        padding: 12px;
        margin: 10px 0;
        border-radius: 10px;
        border: 1px solid #cbd5e1;
        outline: none;
    }}
    .contact-btn {{
        background: linear-gradient(90deg, #22c55e, #16a34a);
        color: white;
        padding: 15px;
        border: none;
        border-radius: 10px;
        width: 100%;
        font-weight: bold;
        cursor: pointer;
        transition: 0.3s;
    }}
    .contact-btn:hover {{
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(22, 163, 74, 0.3);
    }}
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar - Detailed & Colorful
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #4ade80;'>WASIULLAH AI HUB</h2>", unsafe_allow_html=True)
    
    if img_base64:
        st.markdown(f'<div class="profile-container"><img src="data:image/png;base64,{img_base64}" class="circle-img"></div>', unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center; color: white;'>Wasiullah</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>B.Sc. IT Developer | AI Enthusiast</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    # Detailed Stats Card
    st.markdown("""
    <div class="sidebar-card">
        <p style='color: #4ade80; font-weight: bold; margin-bottom: 8px;'>📊 System Performance</p>
        <p style='font-size: 0.85em; margin: 2px;'>• AI Model: <b>Whisper Tiny v2</b></p>
        <p style='font-size: 0.85em; margin: 2px;'>• Speed: <b>Ultra-Fast</b></p>
        <p style='font-size: 0.85em; margin: 2px;'>• Language: <b>Auto-Detection</b></p>
        <p style='font-size: 0.85em; margin: 2px;'>• Uptime: <b>99.9% Online ✅</b></p>
    </div>
    
    <div class="sidebar-card">
        <p style='color: #4ade80; font-weight: bold; margin-bottom: 8px;'>🛡️ Security & Privacy</p>
        <p style='font-size: 0.85em;'>Your files are processed locally in the cloud and deleted instantly after use.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.caption("Developed by Wasiullah © 2026")

# 3. Main Dashboard Area
st.markdown("<h1 style='text-align: center; color: #1e293b;'>🪄 Wasiullah's AI Video-to-Text</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>The most advanced way to transcribe your media with 100% accuracy.</p>", unsafe_allow_html=True)

col_left, col_mid, col_right = st.columns([1, 2, 1])

with col_mid:
    # Feature info box before uploader
    st.info("💡 **Pro Tip:** Upload 1080p videos or high-quality MP3s for the best results. All languages supported!")
    
    uploaded_file = st.file_uploader("Drop your media file here", type=["mp4", "mp3", "wav", "m4a", "mov", "mkv"])

    if uploaded_file:
        file_ext = os.path.splitext(uploaded_file.name)[1]
        temp_name = f"temp_input{file_ext}"

        with st.spinner('🚀 Wasiullah\'s AI is analyzing your media...'):
            try:
                with open(temp_name, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                model = whisper.load_model("tiny")
                result = model.transcribe(temp_name, fp16=False, task="transcribe")
                
                st.balloons()
                st.success(f"✅ Success! Detected Language: **{result.get('language', 'unknown').upper()}**")
                
                # Result Section
                st.subheader("📝 Transcription Result")
                st.text_area("", value=result["text"], height=300)
                
                st.download_button(
                    label="📥 Download Official Transcript",
                    data=result["text"],
                    file_name=f"{uploaded_file.name}_Transcript_Wasiullah.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                if os.path.exists(temp_name): os.remove(temp_name)
    else:
        st.warning("⚠️ Waiting for a file to be uploaded...")

    # 4. Premium Contact Form
    st.write("---")
    st.markdown("<h2 style='text-align: center;'>📬 Get in Touch</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>Have a custom project idea? Let's discuss!</p>", unsafe_allow_html=True)
    
    # Styled Form using HTML and FormSubmit
    contact_html = f"""
    <div class="contact-container">
        <form action="https://formsubmit.co/wasiullah9702@gmail.com" method="POST">
            <input type="hidden" name="_subject" value="New Inquiry - Wasiullah AI Transcriber">
            <input type="text" name="name" placeholder="Full Name" class="contact-input" required>
            <input type="email" name="email" placeholder="Email Address" class="contact-input" required>
            <textarea name="message" placeholder="Describe your project or feedback..." class="contact-input" style="height:120px;" required></textarea>
            <button type="submit" class="contact-btn">Send Message to Wasiullah</button>
        </form>
    </div>
    """
    st.markdown(contact_html, unsafe_allow_html=True)

st.write("---")
st.markdown("<p style='text-align: center; color: #94a3b8;'>Built with ❤️ by <b>Wasiullah</b> | B.Sc. IT Student</p>", unsafe_allow_html=True)
