import streamlit as st
import whisper
import os
import base64

# Page configuration for a professional look
st.set_page_config(page_title="AI Media Transcriber", page_icon="🎙️", layout="centered")

st.title("🎙️ AI Audio & Video to Text Converter")
st.markdown("Upload any media file to get a full text transcription instantly.")

# Step 1 & 2: Supporting both Audio and Video formats
uploaded_file = st.file_uploader("Upload Media (Video or Audio)", type=["mp4", "mkv", "mov", "mp3", "wav", "m4a", "flac"])

if uploaded_file is not None:
    # Step 3: Handling any File Name by saving it with a fixed internal name
    # Isse user ki file name ka "locha" khatam ho jayega
    file_extension = os.path.splitext(uploaded_file.name)[1]
    temp_filename = f"temp_media_input{file_extension}"

    try:
        with st.status("Processing your file...", expanded=True) as status:
            st.write("Uploading and saving file...")
            with open(temp_filename, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Step 1: Using 'tiny' model for maximum speed
            st.write("Loading AI Model (Whisper Tiny)...")
            model = whisper.load_model("tiny")
            
            st.write("Transcribing... This might take a moment depending on length.")
            # Transcribing the full duration
            result = model.transcribe(temp_filename, fp16=False)
            
            full_text = result["text"]
            status.update(label="Transcription Completed!", state="complete", expanded=False)

        # Displaying the Result in English
        st.success("Success! Here is your transcription:")
        st.text_area("Full Transcription:", value=full_text, height=300)

        # Step 2: Download Button
        st.download_button(
            label="📥 Download Transcription as TXT",
            data=full_text,
            file_name=f"{os.path.splitext(uploaded_file.name)[0]}_transcription.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"An error occurred: {e}")
    
    finally:
        # Cleaning up temp files to save server memory
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

else:
    st.info("Please upload a file to start the transcription process.")

st.divider()
st.caption("Powered by OpenAI Whisper • Built with Streamlit")
