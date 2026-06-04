import os
import sys
import threading

# =====================================================================
# INTERCEPT & VERIFY ENVIRONMENT (Pre-Boot Layer)
# =====================================================================
from setup_window import ensure_environment
ensure_environment()  # Blocks until a key is confirmed or loaded

# =====================================================================
# STANDARD SYSTEM IMPORTS (Safe to compile now)
# =====================================================================
from core.brain import JarvisBrain
from audio.ears import JarvisEars
from core.mouth import JarvisMouth
from core.actions import JarvisActions
from core.gui import JarvisHUD

# Global reference for the graphical workspace shell
app = None

# =====================================================================
# BACKGROUND AI THREAD
# =====================================================================
def run_jarvis_engine():
    """Runs the cognitive core processing loops entirely separate from the UI."""
    print("==========================================")
    print("        JARVIS OS: BOOT SEQUENCE          ")
    print("==========================================")
    
    try:
        brain = JarvisBrain()
        ears = JarvisEars()
        mouth = JarvisMouth()
        actions = JarvisActions()
        
        print("\n[READY] Jarvis is completely online, Sir.")
        app.set_state("speaking")
        mouth.speak("All systems operational. Core network linked successfully, Sir.")
        app.set_state("idle")
        
    except Exception as e:
        print(f"\n[CRITICAL FAILURE] Initialization failed: {str(e)}")
        return

    # THE MASTER PIPELINE LOOP
    while True:
        app.set_state("listening")
        spoken_text = ears.listen()
        
        if not spoken_text or spoken_text.startswith("Audio Error:"):
            app.set_state("idle")
            continue
            
        print(f"\nYou (Spoken): {spoken_text}")
        command = spoken_text.lower().strip()
        
        if "exit system" in command or "shut down" in command:
            app.set_state("speaking")
            shutdown_msg = "Terminating all operational frameworks. Goodbye, Sir."
            print(f"\nJarvis: {shutdown_msg}")
            mouth.speak(shutdown_msg)
            os._exit(0)

        # --- LOCAL ACTIONS ROUTER ---
        if "time" in command:
            app.set_state("processing")
            ai_response = actions.get_time()
            app.set_state("speaking")
            print(f"\nJarvis: {ai_response}")
            mouth.speak(ai_response)
            continue  
            
        elif "open" in command:
            app.set_state("processing")
            ai_response = actions.open_website(spoken_text)
            app.set_state("speaking")
            print(f"\nJarvis: {ai_response}")
            mouth.speak(ai_response)
            continue
            
        elif "calculator" in command:
            app.set_state("processing")
            ai_response = actions.open_calculator()
            app.set_state("speaking")
            print(f"\nJarvis: {ai_response}")
            mouth.speak(ai_response)
            continue

        elif "screenshot" in command or "capture screen" in command:
            app.set_state("processing")
            ai_response = actions.take_screenshot()
            app.set_state("speaking")
            print(f"\nJarvis: {ai_response}")
            mouth.speak(ai_response)
            continue

        elif "weather" in command:
            app.set_state("processing")
            ai_response = actions.get_weather(spoken_text)
            app.set_state("speaking")
            print(f"\nJarvis: {ai_response}")
            mouth.speak(ai_response)
            continue

        # --- CLOUD AGENT CORE ---
        app.set_state("processing")
        print("[PROCESSING] Analyzing complex context...")
        ai_response = brain.think(spoken_text)
        
        app.set_state("speaking")
        print(f"\nJarvis: {ai_response}")
        mouth.speak(ai_response)
        print("------------------------------------------")

# =====================================================================
# SYSTEM MAIN ENTRY ROUTER
# =====================================================================
def boot_system():
    """Initializes the background AI processor thread safely."""
    ai_thread = threading.Thread(target=run_jarvis_engine, daemon=True)
    ai_thread.start()

if __name__ == "__main__":
    # Launch main interactive terminal dashboard
    app = JarvisHUD(start_ai_engine_callback=boot_system)
    app.run()