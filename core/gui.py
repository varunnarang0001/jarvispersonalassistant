import tkinter as tk
import sys
import math

class ConsoleRedirector:
    """Intercepts terminal print statements and routes them to the GUI."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        self.text_widget.update_idletasks()

    def flush(self):
        pass

class JarvisHUD:
    def __init__(self, start_ai_engine_callback):
        """Initializes the graphical user interface with an animated voice sphere."""
        self.root = tk.Tk()
        self.root.title("JARVIS OS - Core Engine")
        self.root.geometry("700x850")
        self.root.configure(bg="#050505")  # Deep OLED Black
        
        self.color_accent = "#00ffcc"  # Cyberpunk Neon Cyan
        self.color_glow = "#005544"    # Dark Teal for Glow effect
        
        # Animation Variables
        self.animation_step = 0
        self.current_state = "listening"  # Options: "idle", "listening", "processing", "speaking"
        
        self._build_layout()
        
        # Intercept print statements
        sys.stdout = ConsoleRedirector(self.console_output)
        
        # Start the animation loop
        self.animate_sphere()
        
        # Trigger the AI background engine thread after window maps
        self.root.after(500, start_ai_engine_callback)

    def _build_layout(self):
        """Constructs the visual grid and canvas layout."""
        # Top Header
        header = tk.Label(
            self.root, 
            text="JARVIS", 
            font=("Consolas", 12, "bold"),
            bg="#050505", 
            fg=self.color_accent,
            pady=10
        )
        header.pack(fill=tk.X)
        
        # =====================================================================
        # CORE VOICE SPHERE CANVAS
        # =====================================================================
        self.canvas_size = 250
        self.canvas = tk.Canvas(
            self.root, 
            width=self.canvas_size, 
            height=self.canvas_size, 
            bg="#050505", 
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        # Lower Console Terminal Output
        self.console_output = tk.Text(
            self.root, 
            font=("Consolas", 10), 
            bg="#0d0d0d", 
            fg="#e0e0e0", 
            wrap=tk.WORD,
            padx=15, 
            pady=15,
            borderwidth=0,
            highlightthickness=1,
            highlightbackground="#1f1f1f"
        )
        self.console_output.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    def set_state(self, state):
        """Allows the external main.py loop to dynamically change the sphere behavior."""
        if state in ["idle", "listening", "processing", "speaking"]:
            self.current_state = state

    def animate_sphere(self):
        """Mathematical redraw loop that mimics a fluid, reactive voice sphere."""
        self.canvas.delete("all")
        center = self.canvas_size // 2
        self.animation_step += 0.05
        
        # 1. Map physical variables based on the active system state
        if self.current_state == "idle":
            # Slow, deep rhythmic breathing pattern
            base_radius = 50
            pulse = math.sin(self.animation_step * 2) * 4
            color = "#00aaaa"
            num_rings = 2
        elif self.current_state == "listening":
            # Highly energetic, rapid vibratory tracking
            base_radius = 55
            pulse = math.sin(self.animation_step * 8) * 12
            color = "#00ffcc"
            num_rings = 4
        elif self.current_state == "processing":
            # Swirling wave offset phase calculation
            base_radius = 60
            pulse = math.cos(self.animation_step * 4) * 6
            color = "#9900ff"  # Shifts to a deep processing purple
            num_rings = 3
        elif self.current_state == "speaking":
            # Erratic shifts simulating vocal amplitude bursts
            base_radius = 55
            pulse = abs(math.sin(self.animation_step * 5)) * 18
            color = "#ffffff"  # Pure articulate white light
            num_rings = 3

        # 2. Render concentric fading halo fields for a real glow illusion
        for i in range(num_rings, 0, -1):
            factor = i * 12
            r = base_radius + pulse + factor
            # Inner core stays solid, outer layers act as alpha shadows
            fill_color = "" if i > 1 else color
            outline_color = color if i == 1 else self.color_glow
            
            self.canvas.create_oval(
                center - r, center - r, 
                center + r, center + r, 
                fill=fill_color, 
                outline=outline_color, 
                width=1.5
            )
            
        # 3. Request next visual frame configuration from Tkinter clock loop (30 FPS target)
        self.root.after(33, self.animate_sphere)

    def run(self):
        """Engages window thread execution."""
        self.root.mainloop()