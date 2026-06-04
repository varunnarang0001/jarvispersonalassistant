# JARVIS: Desktop Voice Assistant (V1.0)

A high-performance, multi-threaded desktop voice assistant featuring a real-time reactive canvas UI, secure local environment gateway initialization, and low-latency cloud inference routing.

## 🪐 Architectural Overview
Unlike standard sequential scripts that block execution workflows, Jarvis OS utilizes an asynchronous multi-threaded architecture to decouple heavy physical input/output (I/O) processing from user interface rendering loops:

1. **Main UI Thread:** Governs the Tkinter engine rendering at a locked 30 FPS. It maps mathematical trigonometric calculations directly to a native graphics canvas to draw a fluid, state-reactive neural sphere.
2. **Background Engine Thread:** Spawns an isolated worker thread using Python's `threading` library. This thread manages uninterrupted hardware audio processing (`sounddevice` + `numpy`), streams payloads to remote inference clusters, and coordinates automation execution pipelines.

```text
   +-----------------------------------------------------------+
   |                       MAIN THREAD                         |
   |   [Tkinter UI Shell] <--- (Redirection Wrapper) --- Print |
   |            |                                              |
   |    (State Updates)                                        |
   |            v                                              |
   |   [Animated Voice Sphere] (30 FPS Trigonometric Canvas)    |
   +------------+----------------------------------------------+
                |
         (Spawns As Daemonic)
                v
   +-----------------------------------------------------------+
   |                    BACKGROUND THREAD                      |
   |  [Hardware Mic Stream] -> [RMS VAD Gate] -> [WAV Payload] |
   |                                                    |      |
   |  [Edge-TTS Synthesis]  <- [Llama 3.1 LLM] <- [Groq Cloud] |
   +-----------------------------------------------------------+
```

## 📂 Project Structure
```text
├── audio/
│   └── ears.py          # Sounddevice + NumPy RMS Voice Activity Detection
├── core/
│   ├── actions.py       # OS Automation Executions (Web, Screenshots, Apps)
│   ├── brain.py         # Groq Client Llama 3.1 Cloud Inference Interface
│   ├── gui.py           # Tkinter HUD Assembly & Trigonometric Canvas Animation
│   └── mouth.py         # Asynchronous Edge-TTS Voice Generation Pipeline
├── .gitignore           # Explicit Git Security Exclusions File
├── main.py              # Master Core Orchestrator & Multithreading Linker
├── requirements.txt     # System Dependency Manifest
└── setup_window.py      # Pre-boot Environmental Key Management & Setup UI
```

## 🛠️ Tech Stack & Infrastructure
* **Core Runtime:** Python 3.10+
* **User Interface:** Tkinter Canvas Component + Multithreading Wrappers
* **Cognitive Processing Core:** Groq Cloud Infrastructure Pipeline (Llama 3.1 Engine)
* **Automatic Speech Recognition (ASR):** Groq Whisper-Large-V3 API
* **Voice Activity Detection (VAD):** Sounddevice + NumPy Root Mean Square (RMS) Amplitude Gate
* **Speech Synthesis Engine:** Edge-TTS Asynchronous Script Wrapper + Pygame Audio Channel Streams
* **OS Automation Executive:** PyAutoGUI Component Layer

## ✨ Core Features
* **Zero-Lag Input Termination:** Custom RMS-based voice activity detection stops microphone tracking exactly 0.4 seconds after speaking stops, eliminating cloud truncation delays.
* **State-Driven Neural Orb:** Canvas geometry automatically switches animation states between `idle` (breathing cyan), `listening` (vibrating cyan), `processing` (orbital purple), and `speaking` (bursting white) to provide continuous feedback.
* **Environment Gatekeeper Pattern:** Secures local executions. If a system environmental variable (`GROQ_API_KEY`) is missing, `setup_window.py` isolates runtime execution and builds an entry UI dashboard to ingest and verify keys cleanly, writing them to a secure `.env` file automatically.
* **Local Executive Automation:** Directly intercepts high-priority local keywords to pull hardware metrics, capture screens, parse web data, or load local applications before fallback cloud calls occur.

## 🚀 Installation & Quickstart

1. **Clone the Framework Asset:**
```bash
   git clone [https://github.com/varunnarang0001/jarvispersonalassistant.git](https://github.com/varunnarang0001/jarvispersonalassistant.git)
   cd jarvispersonalassistant
   ```

2. **Deploy Local Dependencies:**
```bash
   pip install -r requirements.txt
   ```

3. **Initialize the Operational Environment:**
   Run the master initialization orchestrator:
```bash
   python main.py
   ```
   *Note: On your first boot, if no local `.env` configuration exists, the `setup_window.py` layer intercepts execution to request your Groq Cloud Token and map system paths automatically.*

## 🔒 Security & Git Management
This repository is configured with strict security protocols. Local variables, credential files (`.env`), database buffers, and temporary binary speech exports (`temp_speech.mp3`, `temp_input.wav`) are explicitly ignored by Git tracking protocols to prevent accidental identity leakage.
```
