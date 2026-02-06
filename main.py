import customtkinter as ctk
from tkinter import filedialog
import whisper
import os
from moviepy import VideoFileClip 
import threading
import sys

# 1. FFmpeg Setup
try:
    import static_ffmpeg
    static_ffmpeg.add_paths()
except Exception as e:
    print(f"FFmpeg Path Error: {e}")

class TranscriberApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("AI Video to Text Pro")
        self.geometry("700x600")
        ctk.set_appearance_mode("dark")

        # UI Elements
        self.label = ctk.CTkLabel(self, text="Professional Video Transcriber", font=("Arial", 24, "bold"))
        self.label.pack(pady=20)

        self.btn = ctk.CTkButton(self, text="Select Video File", command=self.browse_file, height=45, font=("Arial", 14, "bold"))
        self.btn.pack(pady=10)

        self.status = ctk.CTkLabel(self, text="Status: Ready", text_color="#2ecc71", font=("Arial", 14))
        self.status.pack(pady=10)

        self.textbox = ctk.CTkTextbox(self, width=620, height=300, font=("Arial", 13))
        self.textbox.pack(pady=15, padx=20)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.mkv *.avi *.mov")])
        if file_path:
            self.status.configure(text="Processing Started...", text_color="#f1c40f")
            self.textbox.delete("0.0", "end")
            threading.Thread(target=self.process, args=(file_path,), daemon=True).start()

    def process(self, path):
        audio_temp = "temp_audio_file.mp3"
        try:
            # Step A: Audio Extraction
            print(f"--- Processing: {path} ---")
            video = VideoFileClip(path)
            self.status.configure(text="Extracting Audio...", text_color="#3498db")
            video.audio.write_audiofile(audio_temp, logger=None)
            video.close()
            
            # Step B: AI Transcription
            print("--- Loading AI Model... ---")
            self.status.configure(text="Loading AI (Pehli baar time lagta hai)...", text_color="#e67e22")
            model = whisper.load_model("base")
            
            print("--- Transcribing... (Waiting for AI) ---")
            self.status.configure(text="AI is Listening & Typing...", text_color="#f39c12")
            
            # fp16=False is important for CPU users
            result = model.transcribe(audio_temp, fp16=False)
            
            # Step C: Update UI
            final_text = result["text"].strip()
            
            if final_text:
                self.textbox.insert("0.0", final_text)
                self.status.configure(text="Success! Transcription Finished.", text_color="#2ecc71")
                print("--- Done! Text generated successfully. ---")
            else:
                self.textbox.insert("0.0", "AI ko koi awaaz nahi mili.")
                self.status.configure(text="Warning: No Speech Detected", text_color="#e74c3c")

            # Save to file
            with open("transcription_result.txt", "w", encoding="utf-8") as f:
                f.write(final_text)

        except Exception as e:
            print(f"Error: {e}")
            self.status.configure(text=f"Error: {str(e)}", text_color="#e74c3c")
        
        finally:
            if os.path.exists(audio_temp):
                try: os.remove(audio_temp)
                except: pass

if __name__ == "__main__":
    app = TranscriberApp()
    app.mainloop()