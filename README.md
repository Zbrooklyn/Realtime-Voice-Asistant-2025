


---

# Realtime Voice Assistant 2025

A fully offline voice assistant that combines RealtimeSTT, Ollama, and RealtimeTTS (with Piper support) to provide real-time speech recognition, LLM responses, and text-to-speech playback.
Runs on Linux (Raspberry Pi OS + KDE) and Windows.


---

✨ Features

🎙️ RealtimeSTT – low-latency speech-to-text (STT)

🧠 Ollama – run local LLMs with streaming response

🔊 RealtimeTTS (Piper) – fast, high-quality offline text-to-speech (TTS)

⚡ Works on Linux (Raspberry Pi OS, Ubuntu, etc.) and Windows

🔌 Modular config for easy swapping of STT, TTS, or LLM engines



---

📦 Installation

Clone the repo and enter the project folder:

git clone https://github.com/Zbrooklyn/Realtime-Voice-Asistant-2025.git
cd Realtime-Voice-Asistant-2025

Create a virtual environment (recommended):

python -m venv .venv
source .venv/bin/activate    # Linux / Mac
.venv\Scripts\activate       # Windows

Install requirements:

pip install -r requirements.txt


---

⚙️ Configuration

Edit config.yaml to set your engines:

stt:
  provider: "RealtimeSTT"
  model: "base.en"

tts:
  provider: "RealtimeTTS"
  voice: "piper/en_US-amy-low"

llm:
  provider: "ollama"
  model: "llama2"

STT Provider: Currently uses RealtimeSTT

TTS Provider: Uses RealtimeTTS with Piper

LLM Provider: Ollama



---

🚀 Quick Start

Linux (Raspberry Pi OS / Ubuntu)

# 1. Start Ollama in background
ollama serve &

# 2. Run the assistant
python main.py

Windows (PowerShell)

# 1. Start Ollama server
ollama serve

# 2. Run the assistant
python main.py


---

🛠 Project Structure

Realtime-Voice-Asistant-2025/
│── main.py          # Main entry point
│── requirements.txt # Python dependencies
│── config.yaml      # Config file for STT, TTS, LLM
│── README.md        # This file


---

🔧 Requirements

Python 3.9+

Ollama installed and running

Microphone & speaker setup

Works on Linux (tested on Raspberry Pi OS + KDE) and Windows



---

📌 Roadmap

[ ] Add wake word detection

[ ] Add multiple voice options

[ ] GUI dashboard for settings

[ ] Package into .deb / .exe installers



---

🙌 Credits

RealtimeSTT

RealtimeTTS

Piper TTS

Ollama



