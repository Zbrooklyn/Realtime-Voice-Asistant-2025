# Realtime-Voice-Asistant-2025

# rt-voice (offline voice assistant)

Minimal offline loop using **RealtimeSTT** (Whisper), **Ollama** (local LLM, streaming), and **RealtimeTTS** with **Piper** (fallback to system TTS).

## Quick Start

### Linux (Raspberry Pi OS / Debian)
```bash
git clone https://github.com/<you>/rt-voice.git && cd rt-voice
python3 -m venv .venv && source .venv/bin/activate && \
pip install -U pip && pip install -r requirements.txt
curl -fsSL https://ollama.com/install.sh | sh && sudo systemctl enable --now ollama && \
ollama pull phi3:mini
# (Recommended) Piper + a voice
sudo apt update && sudo apt install -y piper
export PIPER_VOICE=/usr/share/piper-voices/en/en_US-amy-medium.onnx
python app.py
