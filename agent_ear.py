"""The speech-to-text side of a voice agent on AssemblyAI STT 3.7 Realtime Agent.

Streams the microphone, stops "agent playback" on SpeechStarted (barge-in),
hands each final turn to your LLM, and passes the agent's reply back as
agent_context so the next short answer resolves in context.

Run: python agent_ear.py   (Ctrl+C to stop)
"""
import os

import pyaudio
from assemblyai.streaming.v3 import (
    RealTimeEvents,
    RealTimeParameters,
    RealTimeSessionParameters,
    RealTimeTranscriber,
    RealTimeTranscriberOptions,
    SpeechStartedEvent,
    TurnEvent,
)

SAMPLE_RATE = 16000
FRAMES_PER_BUFFER = 800  # 50 ms at 16 kHz
GREETING = "Thanks for calling. Can I get the order number?"


def generate_reply(user_text: str) -> str:
    # Replace with your LLM call (for example, through LLM Gateway).
    return "Got it. And what's the email on the order?"


def stop_playback() -> None:
    # Replace with your TTS player's stop() so the agent stops talking.
    print("[barge-in] stopping agent audio")


def on_speech_started(client: RealTimeTranscriber, event: SpeechStartedEvent) -> None:
    stop_playback()


def on_turn(client: RealTimeTranscriber, event: TurnEvent) -> None:
    if not (event.end_of_turn and event.transcript):
        return
    print(f"Caller: {event.transcript}")
    reply = generate_reply(event.transcript)
    print(f"Agent:  {reply}")
    # Give the model the agent's side of the conversation for the next turn.
    client.set_params(RealTimeSessionParameters(agent_context=reply))


def main() -> None:
    client = RealTimeTranscriber(
        RealTimeTranscriberOptions(),
        api_key=os.environ["ASSEMBLYAI_API_KEY"],
    )
    client.on(RealTimeEvents.SpeechStarted, on_speech_started)
    client.on(RealTimeEvents.Turn, on_turn)
    client.connect(
        RealTimeParameters(
            speech_model="assemblyai-stt-3-7-realtime-agent",
            sample_rate=SAMPLE_RATE,
            agent_context=GREETING,
            keyterms_prompt=["order number", "tracking ID"],
        )
    )
    print(f"Agent:  {GREETING}")

    pa = pyaudio.PyAudio()
    mic = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER,
    )
    try:
        while True:
            client.stream(mic.read(FRAMES_PER_BUFFER, exception_on_overflow=False))
    except KeyboardInterrupt:
        pass
    finally:
        mic.stop_stream()
        mic.close()
        pa.terminate()
        client.disconnect(terminate=True)


if __name__ == "__main__":
    main()
