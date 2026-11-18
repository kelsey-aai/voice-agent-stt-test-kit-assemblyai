# Voice agent speech-to-text test kit (AssemblyAI STT 3.7 Realtime Agent)

Companion code for the AssemblyAI blog post [How to choose a speech-to-text API for voice agents: 7 tests that matter](https://www.assemblyai.com/blog/choosing-a-stt-api-for-voice-agents).

| File | What it does |
|---|---|
| `agent_ear.py` | Streams your mic to **AssemblyAI STT 3.7 Realtime Agent** (`assemblyai-stt-3-7-realtime-agent`, $0.45/hr), stops agent playback on `SpeechStarted`, hands final turns to a stub LLM, and passes each reply back as `agent_context` |
| `sync_turn.sh` | Sends one finished turn to the Sync API (`universal-3-6-pro`) over a single HTTP request, for agents that detect turns themselves |

Use it as a harness for the post's tests: run the same scripted turns with and without `agent_context` (Test 4), time barge-in with and without background noise (Test 5), and kill the network mid-session to check your reconnect path (Test 7).

## Setup

```bash
brew install portaudio            # or: sudo apt install portaudio19-dev
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ASSEMBLYAI_API_KEY=your_api_key_here
```

## Run

```bash
python agent_ear.py
./sync_turn.sh turn.wav
```

## Notes

- Requires `assemblyai` 1.10.1+, which lists both STT 3.7 model IDs. Mid-session updates use `client.set_params(RealTimeSessionParameters(...))`.
- Building notetakers or captions instead? Use `assemblyai-stt-3-7-realtime` (AssemblyAI STT 3.7 Realtime, $0.30/hr).
- Streaming is billed on session duration. The script always calls `client.disconnect(terminate=True)`.
- Docs: [Turn detection](https://www.assemblyai.com/docs/streaming/turn-detection) · [Context carryover](https://www.assemblyai.com/docs/streaming/universal-3-5-pro/context-carryover) · [Sync API](https://www.assemblyai.com/docs/sync-stt/getting-started/transcribe-a-short-audio-file)
