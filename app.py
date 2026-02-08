import streamlit as st
import whisper
import os
import base64

# Try to import translator, handle error if missing
try:
    from deep_translator import GoogleTranslator
    HAS_TRANSLATOR = True
except ImportError:
    HAS_TRANSLATOR = False

# 1. Page Configuration
st.set_page_config(page_title="Wasiullah's AI Hub", page_icon="🪄", layout="wide")

# Base64 Image Loader for Sidebar Photo
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
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        color: white;
        border-right: 3px solid #4ade80;
    }}
    .circle-img {{
        width: 160px; height: 160px; border-radius: 50%; object-fit: cover;
        border: 4px solid #4ade80; box-shadow: 0 0 25px rgba(74, 222, 128, 0.5);
        display: block; margin: 20px auto;
    }}
    .sidebar-card {{
        background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 15px;
        margin: 12px 0; border: 1px solid rgba(255, 255, 255, 0.1);
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
    .contact-btn:hover {{ transform: translateY(-3px); box-shadow: 0 10px 20px rgba(22,163,74,0.2); }}
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar Branding
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #4ade80;'>WASIULLAH AI HUB</h2>", unsafe_allow_html=True)
    if img_base64:
        st.markdown(f'<img src="data:image/png;base64,{img_base64}" class="circle-img">', unsafe_allow_html=True)
    else:
        st.warning("Upload 'my_photo.jpg.png' to GitHub to see your photo here.")
    
    st.markdown("<h3 style='text-align: center; color: white;'>Wasiullah</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>B.Sc. IT Developer</p>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("""
    <div class="sidebar-card">
        <p style='color: #4ade80; font-weight: bold;'>⚙️ System Specs</p>
        <p style='font-size: 0.85em;'>• Engine: <b>Whisper Base</b><br>• Audio Filter: <b>Auto-Clean</b><br>• Status: <b>Online ✅</b></p>
    </div>
    """, unsafe_allow_html=True)

# 3. Main Dashboard Area
st.markdown("<h1 style='text-align: center; color: #1e293b;'>🪄 Wasiullah's Pro Transcriber</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>High-accuracy Video & Audio transcription in original language.</p>", unsafe_allow_html=True)

col_l, col_m, col_r = st.columns([1, 2, 1])

with col_m:
    if not HAS_TRANSLATOR:
        st.error("⚠️ Library Error: Please make sure 'deep-translator' is added to your requirements.txt file and the app is rebooted.")

    uploaded_file = st.file_uploader("Drop your media file here", type=["mp4", "mp3", "wav", "m4a", "mov"])

    if uploaded_file:
        file_ext = os.path.splitext(uploaded_file.name)[1]
        temp_name = f"temp_input{file_ext}"

        with st.spinner('🚀 Wasiullah\'s AI is analyzing and cleaning audio...'):
            try:
                with open(temp_name, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Using base model for better Hinglish accuracy
                model = whisper.load_model("base")
                result = model.transcribe(temp_name, fp16=False)
                original_text = result["text"]

                st.balloons()
                st.success(f"✅ Success! Language: {result.get('language', 'unknown').upper()}")
                st.text_area("Original Text:", value=original_text, height=250)

                # Translation & Download Section
                if HAS_TRANSLATOR:
                    st.write("---")
                    st.subheader("📥 Smart Download")
                    target_lang = st.selectbox("Download in:", ["Original", "English", "Hindi", "Urdu"])
                    
                    final_text = original_text
                    if target_lang != "Original":
                        lang_map = {"English": "en", "Hindi": "hi", "Urdu": "ur"}
                        final_text = GoogleTranslator(source='auto', target=lang_map[target_lang]).translate(original_text)
                        st.write(f"**Preview ({target_lang}):** {final_text}")

                    st.download_button(label=f"Download {target_lang} TXT", data=final_text, 
                                     file_name=f"Wasiullah_AI_{target_lang}.txt")

            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                if os.path.exists(temp_name): os.remove(temp_name)

    # 4. Premium Contact Form
    st.write("---")
    st.markdown("<h2 style='text-align: center;'>📬 Get in Touch</h2>", unsafe_allow_html=True)
    contact_html = f"""
    <div class="contact-card">
        <form action="https://formsubmit.co/wasiullah9702@gmail.com" method="POST">
            <input type="text" name="name" placeholder="Full Name" style="width:100%; padding:12px; margin:8px 0; border-radius:10px; border:1px solid #ccc;" required>
            <input type="email" name="email" placeholder="Email Address" style="width:100%; padding:12px; margin:8px 0; border-radius:10px; border:1px solid #ccc;" required>
            <textarea name="message" placeholder="Message Wasiullah..." style="width:100%; padding:12px; margin:8px 0; border-radius:10px; border:1px solid #ccc; height:100px;" required></textarea>
            <button type="submit" class="contact-btn">Send Message</button>
        </form>
    </div>
    """
    st.markdown(contact_html, unsafe_allow_html=True)

st.write("---")
st.markdown("<p style='text-align: center;'>© 2026 Developed by <b>Wasiullah</b></p>", unsafe_allow_html=True)
