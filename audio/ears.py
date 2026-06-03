import os
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from groq import Groq

class JarvisEars:
    def __init__(self):
        """Initializes the microphone settings and Groq Whisper connection."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Critical Error: GROQ_API_KEY missing from .env file.")
        
        self.client = Groq(api_key=api_key)
        
        # Audio Configuration
        self.sample_rate = 16000  # Standard CD-quality sample rate (Hz)
        self.duration = 5         # Duration of the recording window in seconds
        self.temp_filename = "temp_audio.wav"

    def listen(self):
        """Records audio from the mic, saves it temporarily, and transcribes it via Groq."""
        print(f"\n[🎤 Listening for {self.duration} seconds... Speak now!]")
        
        try:
            # 1. Capture raw audio data from the default microphone
            recording = sd.rec(
                int(self.duration * self.sample_rate), 
                samplerate=self.sample_rate, 
                channels=1, 
                dtype='int16'
            )
            sd.wait()  # Block execution until the recording duration completes
            
            # 2. Save the recording with a WAV header (Overwrites the previous file)
            write(self.temp_filename, self.sample_rate, recording)
            print("[✅ Recording complete. Transcribing via Whisper...]")
            
            # 3. Stream the file to Groq's high-speed Whisper Large V3 model
            with open(self.temp_filename, "rb") as file:
                transcription = self.client.audio.transcriptions.create(
                    file=(self.temp_filename, file.read()),
                    model="whisper-large-v3",
                    response_format="text",
                    language="en"
                )
            
            return transcription.strip()
            
        except Exception as e:
            return f"Audio Error: {str(e)}"

# =====================================================================
# ISOLATED UNIT TESTING
# =====================================================================
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    print("--- Jarvis Ears Unit Test ---")
    try:
        ears = JarvisEars()
        text_output = ears.listen()
        print(f"\nTranscription Result:\n>>> {text_output}")
    except Exception as e:
        print(f"\nInitialization failed: {e}")