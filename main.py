import os
import sys
import threading
from dotenv import load_dotenv

# =====================================================================
# SYSTEM BOOTSTRAP: LOAD CONFIGURATION
# =====================================================================
load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    print("[CRITICAL ERROR] GROQ_API_KEY is missing from your environment configuration.")
    print("Please check your .env file in the root directory.")
    sys.exit(1)

# =====================================================================
# IMPORT MODULES (Reflected Directory Structure)
# =====================================================================
try:
    from core.brain import JarvisBrain
    from audio.ears import JarvisEars
    from core.mouth import JarvisMouth
    from core.actions import JarvisActions
    from core.gui import JarvisHUD
except ModuleNotFoundError as e:
    print(f"[CRITICAL ERROR] Failed to import internal modules: {str(e)}")
    print("Please verify your folder structure matches:")
    print("├── audio/ears.py\n├── core/brain.py, mouth.py, actions.py, gui.py\n└── main.py")
    sys.exit(1)

# Global reference for the GUI application interface
app = None

# =====================================================================
# BACKGROUND AI THREAD
# =====================================================================
def run_jarvis_engine():
    """Runs the cognitive core entirely decoupled from the main UI thread."""
    print("=====================================================================")
    print("                        JARVIS OS: BOOT SEQUENCE          ")
    print("=====================================================================")
    
    try:
        brain = JarvisBrain()
        ears = JarvisEars()
        mouth = JarvisMouth()
        actions = JarvisActions()
        print("\n[READY] Jarvis is completely online, Sir.")
        
        # Audio confirmation and resetting state to idle
        app.set_state("speaking")
        mouth.speak("All systems operational. Cognitive interface loaded and online, Sir.")
        app.set_state("idle")
        
    except Exception as e:
        print(f"\n[CRITICAL FAILURE] Initialization failed: {str(e)}")
        return

    # =====================================================================
    # THE MASTER EXECUTION LOOP (Data Routing Engine)
    # =====================================================================
    while True:
        # Step 1: Set state to listening and capture voice input via sounddevice
        app.set_state("listening")
        spoken_text = ears.listen()
        
        # Guard clause: Return to idle/listening if recording was silent or errored
        if not spoken_text or spoken_text.startswith("Audio Error:"):
            app.set_state("idle")
            continue
            
        print(f"\nYou (Spoken): {spoken_text}")
        command = spoken_text.lower().strip()
        
        # Step 2: Immediate Hard Shutdown Command
        if "exit system" in command or "shut down" in command:
            app.set_state("speaking")
            shutdown_msg = "Terminating all operational frameworks. Goodbye, Sir."
            print(f"\nJarvis: {shutdown_msg}")
            mouth.speak(shutdown_msg)
            os._exit(0)  # Cleanly collapses the visual shell and background threads

        # =====================================================================
        # STEP 3: THE AUTOMATION INTERCEPTOR (Local Action Routing)
        # =====================================================================
        
        # Command Rule A: System Time
        if "time" in command:
            app.set_state("processing")
            ai_response = actions.get_time()
            
            app.set_state("speaking")
            print(f"\nJarvis: {ai_response}")
            mouth.speak(ai_response)
            continue  
            
        # Command Rule B: Dynamic Web Browsing / Google Searching
        elif "open" in command:
            app.set_state("processing")
            ai_response = actions.open_website(spoken_text)
            
            app.set_state("speaking")
            print(f"\nJarvis: {ai_response}")
            mouth.speak(ai_response)
            continue
            
        # Command Rule C: Calculator Application
        elif "calculator" in command:
            app.set_state("processing")
            ai_response = actions.open_calculator()
            
            app.set_state("speaking")
            print(f"\nJarvis: {ai_response}")
            mouth.speak(ai_response)
            continue

        # Command Rule D: Desktop Screen Capture
        elif "screenshot" in command or "capture screen" in command:
            app.set_state("processing")
            ai_response = actions.take_screenshot()
            
            app.set_state("speaking")
            print(f"\nJarvis: {ai_response}")
            mouth.speak(ai_response)
            continue

        # Command Rule E: Current Weather Forecasting
        elif "weather" in command:
            app.set_state("processing")
            ai_response = actions.get_weather(spoken_text)
            
            app.set_state("speaking")
            print(f"\nJarvis: {ai_response}")
            mouth.speak(ai_response)
            continue

        # =====================================================================
        # STEP 4: COGNITIVE FALLBACK (Cloud Intelligence Core)
        # =====================================================================
        # If no local keyword triggers, route the message to Llama 3.1
        app.set_state("processing")
        print("[PROCESSING] Analyzing complex context...")
        ai_response = brain.think(spoken_text)
        
        app.set_state("speaking")
        print(f"\nJarvis: {ai_response}")
        mouth.speak(ai_response)
        print("------------------------------------------")

# =====================================================================
# MAIN THREAD (GUI EXECUTION GATEWAY)
# =====================================================================
def boot_system():
    """Initializes the background AI processor thread safely."""
    ai_thread = threading.Thread(target=run_jarvis_engine, daemon=True)
    ai_thread.start()

if __name__ == "__main__":
    # Mount the visual HUD environment on the main thread
    app = JarvisHUD(start_ai_engine_callback=boot_system)
    app.run()