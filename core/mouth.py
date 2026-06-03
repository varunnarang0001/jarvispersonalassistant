import os
import re
import time
import asyncio
import edge_tts
import pygame

class JarvisMouth:
    def __init__(self):
        """Initializes the Microsoft Edge TTS and Pygame audio mixer."""
        pygame.mixer.init()
        self.temp_file = "temp_speech.mp3"
        
        # ==========================================
        # VOICE PROFILES (Uncomment the one you want)
        # ==========================================
        # self.voice = "en-US-GuyNeural"         # Crisp American Male
        self.voice = "en-GB-RyanNeural"        # Professional British Male
        # self.voice = "en-IN-PrabhatNeural"     # Clear Indian Male
        # self.voice = "en-US-ChristopherNeural" # Deep American Male

    def clean_text(self, text):
        """Strips Llama 3.1 Markdown and emojis before speaking."""
        text = re.sub(r'[*_#`~]', '', text)
        text = text.encode('ascii', 'ignore').decode('ascii')
        return text.strip()

    def speak(self, text):
        """Generates an MP3 via Edge TTS, plays it, and cleans it up."""
        safe_text = self.clean_text(text)
        
        if not safe_text:
            return
            
        try:
            # 1. Generate the audio file using edge-tts (requires async run)
            communicate = edge_tts.Communicate(safe_text, self.voice)
            asyncio.run(communicate.save(self.temp_file))
            
            # 2. Load and play the audio file safely
            pygame.mixer.music.load(self.temp_file)
            pygame.mixer.music.play()
            
            # 3. Block the execution loop until the audio finishes playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            # 4. Release the file lock so it can be overwritten next time
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            
            # Give the OS a tiny fraction of a second to release the file
            time.sleep(0.1)
            
            # Cleanup the temporary file
            if os.path.exists(self.temp_file):
                os.remove(self.temp_file)
                
        except Exception as e:
            print(f"\n[SYSTEM] Audio articulation failure: {e}")

# =====================================================================
# ISOLATED UNIT TESTING
# =====================================================================
if __name__ == "__main__":
    print("--- Jarvis Male Voice Failsafe Test ---")
    mouth = JarvisMouth()
    print("[SYSTEM] Attempting to speak...")
    mouth.speak("Audio engine reboot complete. I am using the Edge cloud framework with a masculine voice, Sir.")
    print("[✅] Test complete.")