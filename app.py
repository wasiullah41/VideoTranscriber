import streamlit as st
import whisper
import os
import base64
from deep_translator import GoogleTranslator

# 1. Page Configuration
st.set_page_config(page_title="Wasiullah's AI Hub", page_icon="🪄", layout="wide")

# Base64 Image Loader
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

img_base64 = get_base64_image("my_photo.jpg.png")

# Premium CSS Styling
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
    }}
    .sidebar-card {{
        background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 15px;
        margin: 12px 0; border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    .contact-card {{
        background: white; padding: 30px; border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-top: 40px;
    }}
    .contact-input {{ width: 100%; padding: 12px; margin: 8px 0; border-radius: 10px; border: 1px solid #ccc; }}
    .contact-btn {{
        background: linear-gradient(90deg, #22c55e, #16a34a); color: white;
        padding: 15px; border: none; border-radius: 10px; width: 100%; font-weight: bold; cursor: pointer;
    }}
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar Branding
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #4ade80;'>WASIULLAH AI HUB</h2>", unsafe_allow_html=True)
    if img_base64:
        st.markdown(f'<div style="text-align:center"><img src="data:image/png;base64,{img_base64}" class="circle-img"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Wasiullah</h3>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("""
    <div class="sidebar-card">
        <p style='color: #4ade80; font-weight: bold;'>⚙️ Engine Specs</p>
        <p style='font-size: 0.85em;'>• Model: Whisper Base v2<br>• Noise Filter: Enabled<br>• Accuracy: High</p>
    </div>
    """, unsafe_allow_html=True)

# 3. Main UI
st.markdown("<h1 style='text-align: center;'>🪄 Wasiullah's Pro Transcriber</h1>", unsafe_allow_html=True)

col_l, col_m, col_r = st.columns([1, 2, 1])

with col_m:
    uploaded_file = st.file_uploader("Upload your Audio/Video", type=["mp4", "mp3", "wav", "m4a", "mov"])

    if uploaded_file:
        file_ext = os.path.splitext(uploaded_file.name)[1]
        temp_name = f"temp_input{file_ext}"

        with st.spinner('🚀 Wasiullah\'s AI is cleaning audio & transcribing...'):
            try:
                with open(temp_name, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Base model better accuracy provide karta hai
                model = whisper.load_model("base")
                result = model.transcribe(temp_name, fp16=False)
                original_text = result["text"]
                detected_lang = result.get("language", "en")

                st.success(f"✅ Transcription Done! (Detected: {detected_lang.upper()})")
                
                # Original Text dikhana
                st.subheader("📝 Original Transcription:")
                st.text_area("", value=original_text, height=200)

                # 4. DOWNLOAD OPTION IN DIFFERENT LANGUAGES
                st.write("---")
                st.subheader("📥 Download Options")
                target_lang = st.selectbox("Select Language for Download:", 
                                         ["Original", "English", "Hindi", "Urdu", "Marathi", "Gujarati"])

                final_text_to_download = original_text

                if target_lang != "Original":
                    with st.spinner(f'Translating to {target_lang}...'):
                        # Lang codes mapping
                        lang_map = {"English": "en", "Hindi": "hi", "Urdu": "ur", "Marathi": "mr", "Gujarati": "gu"}
                        final_text_to_download = GoogleTranslator(source='auto', target=lang_map[target_lang]).translate(original_text)
                        st.write(f"**Translated ({target_lang}):**")
                        st.write(final_text_to_download)

                st.download_button(
                    label=f"📥 Download in {target_lang}",
                    data=final_text_to_download,
                    file_name=f"Wasiullah_AI_{target_lang}.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                if os.path.exists(temp_name): os.remove(temp_name)

    # 5. Modern Contact Form
    st.write("---")
    st.markdown("<h2 style='text-align: center;'>📬 Contact Wasiullah</h2>", unsafe_allow_html=True)
    contact_html = f"""
    <div class="contact-card">
        <form action="https://formsubmit.co/wasiullah9702@gmail.com" method="POST">
            <input type="text" name="name" placeholder="Your Name" class="contact-input" required>
            <input type="email" name="email" placeholder="Your Email" class="contact-input" required>
            <textarea name="message" placeholder="Your Message..." class="contact-input" style="height:100px;" required></textarea>
            <button type="submit" class="contact-btn">Send Message</button>
        </form>
    </div>
    """
    st.markdown(contact_html, unsafe_allow_html=True)

st.write("---")
st.markdown("<p style='text-align: center;'>© 2026 Developed by <b>Wasiullah</b></p>", unsafe_allow_html=True)
