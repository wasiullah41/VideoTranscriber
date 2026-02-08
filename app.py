import streamlit as st
import whisper
import os
import base64
from deep_translator import GoogleTranslator

# 1. Page Configuration
st.set_page_config(page_title="Wasiullah's AI Hub", page_icon="🪄", layout="wide")

# Base64 Image Loader for Sidebar
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

img_base64 = get_base64_image("my_photo.jpg.png")

# Premium SaaS UI Styling
st.markdown(f"""
    <style>
    .stApp {{ background-color: #f8fafc; }}
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #1e1b4b 0%, #312e81 100%);
        color: white;
        border-right: 3px solid #4ade80;
    }}
    .circle-img {{
        width: 160px; height: 160px; border-radius: 50%; object-fit: cover;
        border: 4px solid #4ade80; box-shadow: 0 0 25px rgba(74, 222, 128, 0.5);
        display: block; margin: 20px auto;
    }}
    .sidebar-card {{
        background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 15px;
        margin: 12px 0; border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    .contact-card {{
        background: white; padding: 35px; border-radius: 24px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;
    }}
    .contact-btn {{
        background: linear-gradient(90deg, #22c55e, #16a34a); color: white;
        padding: 16px; border: none; border-radius: 12px; width: 100%;
        font-weight: bold; cursor: pointer; transition: 0.3s;
    }}
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar - Detailed Branding
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #4ade80;'>WASIULLAH AI HUB</h2>", unsafe_allow_html=True)
    if img_base64:
        st.markdown(f'<img src="data:image/png;base64,{img_base64}" class="circle-img">', unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center; color: white;'>Wasiullah</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>B.Sc. IT Developer</p>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("""
    <div class="sidebar-card">
        <p style='color: #4ade80; font-weight: bold;'>⚙️ Intelligence Mode</p>
        <p style='font-size: 0.85em;'>• Engine: <b>Whisper Base v2</b><br>• Task: <b>Full Transcription</b><br>• Status: <b>High Accuracy ✅</b></p>
    </div>
    """, unsafe_allow_html=True)

# 3. Main Dashboard
st.markdown("<h1 style='text-align: center;'>🪄 Wasiullah's Pro Transcriber</h1>", unsafe_allow_html=True)

col_l, col_m, col_r = st.columns([1, 2, 1])

with col_m:
    uploaded_file = st.file_uploader("Upload Video or Audio", type=["mp4", "mp3", "wav", "m4a", "mov", "mkv"])

    if uploaded_file:
        file_ext = os.path.splitext(uploaded_file.name)[1]
        temp_name = f"temp_input{file_ext}"

        with st.spinner('🚀 Wasiullah\'s AI is analyzing every second of audio...'):
            try:
                with open(temp_name, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Accuracy ke liye Base model fix kiya hai
                model = whisper.load_model("base")
                
                # Task: Transcribe ensures original language text is captured fully
                result = model.transcribe(temp_name, fp16=False, task="transcribe")
                original_text = result["text"]
                detected_lang = result.get("language", "hi")

                st.balloons()
                st.success(f"✅ Success! Full Transcription Complete. Language: **{detected_lang.upper()}**")
                
                # Show full text in UI
                st.subheader("📝 Complete Transcription Result:")
                st.text_area("", value=original_text, height=350)

                # 4. Smart Language Options for Download
                st.write("---")
                st.subheader("📥 Professional Download Section")
                target_lang = st.selectbox("Choose Language to Translate & Download:", 
                                         ["Original", "English", "Hindi", "Urdu", "Marathi", "Bengali"])

                final_text = original_text

                if target_lang != "Original":
                    with st.spinner(f'Translating full text to {target_lang}...'):
                        lang_map = {"English": "en", "Hindi": "hi", "Urdu": "ur", "Marathi": "mr", "Bengali": "bn"}
                        # Translating the whole piece of text
                        final_text = GoogleTranslator(source='auto', target=lang_map[target_lang]).translate(original_text)
                        st.write(f"**Preview ({target_lang}):**")
                        st.info(final_text)

                # Branded Download Button
                st.download_button(
                    label=f"📥 Download Transcription in {target_lang}",
                    data=final_text,
                    file_name=f"{os.path.splitext(uploaded_file.name)[0]}_By_Wasiullah_{target_lang}.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                if os.path.exists(temp_name): os.remove(temp_name)

    # 5. Premium Contact Section
    st.write("---")
    st.markdown("<h2 style='text-align: center;'>📬 Get in Touch</h2>", unsafe_allow_html=True)
    contact_html = f"""
    <div class="contact-card">
        <form action="https://formsubmit.co/wasiullah9702@gmail.com" method="POST">
            <input type="text" name="name" placeholder="Full Name" style="width:100%; padding:12px; margin:8px 0; border-radius:10px; border:1px solid #ccc;" required>
            <input type="email" name="email" placeholder="Email Address" style="width:100%; padding:12px; margin:8px 0; border-radius:10px; border:1px solid #ccc;" required>
            <textarea name="message" placeholder="Your Message..." style="width:100%; padding:12px; margin:8px 0; border-radius:10px; border:1px solid #ccc; height:120px;" required></textarea>
            <button type="submit" class="contact-btn">Send Message to Wasiullah</button>
        </form>
    </div>
    """
    st.markdown(contact_html, unsafe_allow_html=True)

st.write("---")
st.markdown("<p style='text-align: center;'>© 2026 Developed by <b>Wasiullah</b> | B.Sc. IT Project</p>", unsafe_allow_html=True)
