import streamlit as st
import whisper
import os
import base64

# 1. Page Configuration
st.set_page_config(page_title="Wasiullah's AI Transcriber", page_icon="🪄", layout="wide")

# Function to convert image to base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# Custom CSS for UI, Circular Image and Contact Form
img_base64 = get_base64_image("my_photo.jpg.png")

st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        color: white;
    }}
    
    .circle-img {{
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #4ade80;
        box-shadow: 0 0 20px rgba(74, 222, 128, 0.6);
        display: block;
        margin: 20px auto;
    }}

    .neon-text {{
        color: #4ade80;
        text-shadow: 0 0 10px rgba(74, 222, 128, 0.5);
        font-weight: bold;
        text-align: center;
        font-size: 1.4em;
    }}

    .sidebar-card {{
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}

    /* Contact Form Styling */
    input[type=text], input[type=email], textarea {{
        width: 100%;
        padding: 12px;
        border: 1px solid #ccc;
        border-radius: 8px;
        box-sizing: border-box;
        margin-top: 6px;
        margin-bottom: 16px;
    }}

    button[type=submit] {{
        background-color: #22c55e;
        color: white;
        padding: 12px 20px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        width: 100%;
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar with Wasiullah's Branding
with st.sidebar:
    st.markdown('<p class="neon-text">WASIULLAH AI HUB</p>', unsafe_allow_html=True)
    
    if img_base64:
        st.markdown(f'<img src="data:image/png;base64,{img_base64}" class="circle-img">', unsafe_allow_html=True)
    else:
        st.info("Photo 'my_photo.jpg.png' not found in repo.")
    
    st.markdown("<h3 style='text-align: center; margin-bottom: 0;'>Wasiullah</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>B.Sc. IT Developer</p>", unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("""
    <div class="sidebar-card">
        <p style='color: #4ade80; font-weight: bold; margin: 0;'>🚀 Status: Online</p>
        <p style='font-size: 0.8em; color: #94a3b8;'>AI Engine: Whisper Tiny</p>
    </div>
    """, unsafe_allow_html=True)

# 3. Main Interface
st.markdown("<h1 style='text-align: center;'>🪄 Wasiullah's AI Media Transcriber</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    uploaded_file = st.file_uploader("Upload Video or Audio", type=["mp4", "mp3", "wav", "m4a", "mov"])

    if uploaded_file:
        file_ext = os.path.splitext(uploaded_file.name)[1]
        temp_name = f"temp_file{file_ext}"

        with st.spinner('Wasiullah\'s AI is working...'):
            try:
                with open(temp_name, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                model = whisper.load_model("tiny")
                result = model.transcribe(temp_name, fp16=False)
                
                st.balloons()
                st.success("Transcription Completed!")
                st.text_area("Result:", value=result["text"], height=300)
                st.download_button("📥 Download Result", data=result["text"], file_name=f"{uploaded_file.name}_by_Wasiullah.txt")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                if os.path.exists(temp_name): os.remove(temp_name)

    # 4. Contact Form Section
    st.write("---")
    st.subheader("📬 Get In Touch with Wasiullah")
    
    contact_form = f"""
    <form action="https://formsubmit.co/wasiullah9702@gmail.com" method="POST">
        <input type="hidden" name="_subject" value="New Message from AI Transcriber!">
        <input type="text" name="name" placeholder="Your Name" required>
        <input type="email" name="email" placeholder="Your Email" required>
        <textarea name="message" placeholder="Your Message Here..." required></textarea>
        <button type="submit">Send Message</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)

st.write("---")
st.markdown("<p style='text-align: center; color: #94a3b8;'>© 2026 Designed & Developed by <b>Wasiullah</b></p>", unsafe_allow_html=True)
