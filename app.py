
import streamlit as st
import whisper
import os
from moviepy import VideoFileClip


ffmpeg_path = r"C:\Users\ansar\Downloads\ffmpeg-8.0.1\bin\ffmpeg.exe" 
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path
# -----------------------
import streamlit as st
import whisper
import os
from moviepy import VideoFileClip

# Page ki settings (Mobile friendly)
st.set_page_config(page_title="AI Video Transcriber", page_icon="🎙️")

st.title("🎙️ AI Video to Text Converter")
st.markdown("Upload a video and let AI transcribe it for you.")

# 1. File Upload ka option
uploaded_file = st.file_uploader("Apni video select karein (mp4, mov, mkv)", type=["mp4", "mov", "mkv"])

if uploaded_file is not None:
    # Video preview dikhayega
    st.video(uploaded_file)
    
    if st.button("Transcribe Video"):
        with st.spinner("AI sun raha hai... Isme thoda waqt lag sakta hai"):
            try:
                # Video ko temporary save karna
                with open("temp_video.mp4", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Step 1: Audio Extract karna
                video = VideoFileClip("temp_video.mp4")
                video.audio.write_audiofile("temp_audio.mp3")
                video.close()
                
                # Step 2: Whisper AI se text nikalna
                model = whisper.load_model("base")
                result = model.transcribe("temp_audio.mp3", fp16=False)
                
                # Step 3: Result dikhana
                st.success("Kaam Khatam!")
                st.subheader("Video ka Text:")
                st.text_area("Transcript", result["text"], height=300)
                
                # Download button dena
                st.download_button(
                    label="Download Text File",
                    data=result["text"],
                    file_name="transcription.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"Ek error aaya: {e}")
            
            finally:
                # Faltu files delete karna
                if os.path.exists("temp_video.mp4"): os.remove("temp_video.mp4")
                if os.path.exists("temp_audio.mp3"): os.remove("temp_audio.mp3")

                import static_ffmpeg



