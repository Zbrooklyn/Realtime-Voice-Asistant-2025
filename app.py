#!/usr/bin/env python3
"""
Minimal offline voice assistant using:
  - RealtimeSTT (Whisper) for STT
  - Ollama for LLM (streaming tokens)
  - RealtimeTTS PiperEngine for realtime TTS (fallback: SystemEngine/pyttsx3)

Use:
  Press ENTER to talk (auto-stops on silence). Reply streams & speaks in near real-time.

Env vars (optional):
  OLLAMA_URL   (default: http://localhost:11434)
  OLLAMA_MODEL (default: phi3:mini)
  AUDIO_INPUT_INDEX / AUDIO_OUTPUT_INDEX  (sounddevice indices)
  PIPER_BIN    (default: "piper" on Linux; e.g., C:\\piper\\piper.exe on Windows)
  PIPER_VOICE  (path to voice *.onnx)
  PIPER_CFG    (optional: voice *.onnx.json)
"""

import os, sys, json, shutil, requests
from typing import Iterator, Optional

# --- optional device selection ---
MIC_INDEX = os.environ.get("AUDIO_INPUT_INDEX")
SPK_INDEX = os.environ.get("AUDIO_OUTPUT_INDEX")
try:
    import sounddevice as sd
    if MIC_INDEX is not None or SPK_INDEX is not None:
        sd.default.device = (
            int(MIC_INDEX) if MIC_INDEX is not None else None,
            int(SPK_INDEX) if SPK_INDEX is not None else None,
        )
except Exception:
    pass

# --- config ---
OLLAMA_URL   = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "phi3:mini")

# --- deps ---
from RealtimeSTT import AudioToTextRecorder
from RealtimeTTS import TextToAudioStream, PiperEngine, SystemEngine

# --- Ollama stream ---
def ollama_stream(prompt: str) -> Iterator[str]:
    r = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": True},
        stream=True, timeout=300
    )
    r.raise_for_status()
    for line in r.iter_lines(decode_unicode=True):
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        tok = obj.get("response", "")
        if tok:
            yield tok

def build_tts_stream() -> TextToAudioStream:
    """
    Prefer Piper if available; otherwise use system TTS (pyttsx3).
    """
    piper_bin  = os.environ.get("PIPER_BIN", "piper")
    voice_path = os.environ.get("PIPER_VOICE", "")
    cfg_path   = os.environ.get("PIPER_CFG") or (voice_path + ".json" if voice_path else "")

    piper_ok = bool(shutil.which(piper_bin)) and voice_path and os.path.exists(voice_path)
    if piper_ok:
        try:
            eng = PiperEngine(
                voice_path=voice_path,
                piper_path=piper_bin,
                config_path=cfg_path if cfg_path and os.path.exists(cfg_path) else None
            )
            return TextToAudioStream(eng)
        except Exception as e:
            print(f"⚠️ PiperEngine failed ({e}); using SystemEngine.", file=sys.stderr)

    # Fallback: pyttsx3 via SystemEngine (offline)
    return TextToAudioStream(SystemEngine())

def main():
    print("Loading STT…")
    rec = AudioToTextRecorder(
        model="base",            # 'base' = faster; 'small' = better accuracy
        language="en",
        compute_type="int8",
        post_speech_silence_duration=0.6,
        silero_sensitivity=0.4,
        webrtc_sensitivity=0.5,
        min_length=4,
    )

    print("\nReady. Press ENTER to talk. Ctrl+C to quit.")
    try:
        while True:
            input()
            print("🎙️  Speak… (auto-stops on silence)")
            text: Optional[str] = rec.text()
            if not text:
                print("…no speech detected.")
                continue
            print(f"👤 You: {text}")

            print("🤖 Streaming from Ollama (speaking as it comes)…")
            tts = build_tts_stream()
            tts.feed(ollama_stream(text))
            tts.play()  # blocking until the streamed text finishes
            print("(end)\n")
    except KeyboardInterrupt:
        print("\nBye.")

if __name__ == "__main__":
    main()
