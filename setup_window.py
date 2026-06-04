import os
import tkinter as tk
from dotenv import load_dotenv

def ensure_environment():
    """Ensures the Groq API key exists. If missing, prompts the user via a UI 

    and writes it permanently to a local .env file.
    """
    load_dotenv()
    
    # If the key is already present in your system or .env, skip setup entirely
    if os.getenv("GROQ_API_KEY"):
        return True
        
    # Build a dedicated initialization frame if the environment is empty
    root = tk.Tk()
    root.title("JARVIS OS - Environment Setup")
    root.geometry("550x320")
    root.configure(bg="#050505")
    root.resizable(False, False)
    
    color_accent = "#00ffcc"
    
    def save_and_exit():
        entered_key = key_entry.get().strip()
        if not entered_key:
            return
            
        # 1. Write the key permanently to a local .env file
        with open(".env", "w", encoding="utf-8") as env_file:
            env_file.write(f"GROQ_API_KEY={entered_key}\n")
            
        # 2. Inject it into the current live execution session memory
        os.environ["GROQ_API_KEY"] = entered_key
        
        # 3. Collapse the configuration window to release the main thread
        root.destroy()

    # Layout Elements
    frame = tk.Frame(root, bg="#050505")
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.85)
    
    title = tk.Label(
        frame,
        text="ENVIRONMENT SETUP REQUIRED",
        font=("Consolas", 13, "bold"),
        bg="#050505",
        fg="#ff3333"
    )
    title.pack(pady=(0, 10))
    
    instructions = tk.Label(
        frame,
        text="A valid Groq Cloud API Key is required to authorize the cognitive core. Please enter your credential token below:",
        font=("Consolas", 10),
        bg="#050505",
        fg="#a0a0a0",
        wraplength=450,
        justify=tk.CENTER
    )
    instructions.pack(pady=(0, 20))
    
    key_entry = tk.Entry(
        frame,
        font=("Consolas", 11),
        bg="#0d0d0d",
        fg="#ffffff",
        insertbackground=color_accent,
        show="*",
        borderwidth=0,
        highlightthickness=1,
        highlightbackground="#333333",
        highlightcolor=color_accent
    )
    key_entry.pack(fill=tk.X, ipady=8, pady=(0, 25))
    key_entry.focus_set()
    
    submit_btn = tk.Button(
        frame,
        text="SAVE & BOOT ASSISTANT",
        font=("Consolas", 10, "bold"),
        bg="#111111",
        fg=color_accent,
        activebackground=color_accent,
        activeforeground="#000000",
        borderwidth=1,
        relief=tk.FLAT,
        command=save_and_exit
    )
    submit_btn.pack(ipady=6, ipadx=20)
    
    # Bind Enter key to submit quickly
    root.bind("<Return>", lambda event: save_and_exit())
    root.mainloop()
    return True