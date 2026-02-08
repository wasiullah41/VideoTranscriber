import streamlit as st
import whisper
import os
import base64
from deep_translator import GoogleTranslator

# 1. Page Configuration
st.set_page_config(page_title="Wasiullah's AI Hub", page_icon="🪄", layout="wide")

# Image Loader Function
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

img_base64 = get_base64_image("my_photo.jpg.png")

# Premium UI Styling
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
    .contact-card {{
        background: white; padding: 30px; border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-top: 40px;
    }}
    .contact-btn {{
        background: linear-gradient(90deg, #22c55e, #16a34a); color: white;
        padding: 15px; border: none; border-radius: 12px; width: 100%; font-weight: bold; cursor: pointer;
    }}
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar Branding
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #4ade80;'>WASIULLAH AI HUB</h2>", unsafe_allow_html=True)
    if img_base64:
        st.markdown(f'<img src="data:image/png;base64,{img_base64}" class="circle-img">', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Wasiullah</h3>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("⚙️ **Engine:** Whisper Base\n\n🛡️ **Status:** High Accuracy Mode")

# 3. Main UI
st.markdown("<h1 style='text-align: center;'>🪄 Wasiullah's Pro Transcriber</h1>", unsafe_allow_html=True)

col_l, col_m, col_r = st.columns([1, 2, 1])

with col_m:
    uploaded_file = st.file_uploader("Upload Audio/Video", type=["mp4", "mp3", "wav", "m4a", "mov"])

    if uploaded_file:
        file_ext = os.path.splitext(uploaded_file.name)[1]
        temp_name = f"temp_input{file_ext}"

        with st.spinner('🚀 Wasiullah\'s AI is analyzing full audio length...'):
            try:
                with open(temp_name, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Accuracy ke liye base model use kar rahe hain
                model = whisper.load_model("base")
                
                # Original language mein poora text nikalne ke liye
                result = model.transcribe(temp_name, fp16=False, task="transcribe")
                original_text = result["text"]
                detected_lang = result.get("language", "hi")

                st.balloons()
                st.success(f"✅ Full Transcription Done! (Language: {detected_lang.upper()})")
                
                st.subheader("📝 Original Text (Hindi/English):")
                st.text_area("", value=original_text, height=300)

                # 4. Multi-Language Download Option
                st.write("---")
                st.subheader("📥 Smart Language Converter")
                target_lang = st.selectbox("Convert & Download in:", 
                                         ["Original", "English", "Hindi", "Urdu", "Marathi", "Bengali"])

                final_text = original_text

                if target_lang != "Original":
                    with st.spinner(f'Converting to {target_lang}...'):
                        lang_map = {"English": "en", "Hindi": "hi", "Urdu": "ur", "Marathi": "mr", "Bengali": "bn"}
                        # Full text translation
                        final_text = GoogleTranslator(source='auto', target=lang_map[target_lang]).translate(original_text)
                        st.write(f"**Preview ({target_lang}):**")
                        st.write(final_text)

                st.download_button(
                    label=f"📥 Download in {target_lang}",
                    data=final_text,
                    file_name=f"Wasiullah_AI_{target_lang}.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                if os.path.exists(temp_name): os.remove(temp_name)

    # 5. Contact Form
    st.write("---")
    st.markdown("<h2 style='text-align: center;'>📬 Contact Wasiullah</h2>", unsafe_allow_html=True)
    contact_html = f"""
    <div class="contact-card">
        <form action="https://formsubmit.co/wasiullah9702@gmail.com" method="POST">
            <input type="text" name="name" placeholder="Your Name" style="width:100%; padding:10px; margin:5px 0;" required>
            <input type="email" name="email" placeholder="Your Email" style="width:100%; padding:10px; margin:5px 0;" required>
            <textarea name="message" placeholder="Your Message..." style="width:100%; padding:10px; margin:5px 0; height:80px;" required></textarea>
            <button type="submit" class="contact-btn">Send Message</button>
        </form>
    </div>
    """
    st.markdown(contact_html, unsafe_allow_html=True)
