import os
import sounddevice as sd
import numpy as np
import wave
import assemblyai as aai
import tempfile
from pynput import keyboard
from dotenv import load_dotenv

load_dotenv()
assembly_api_key = os.getenv('ASSEMBLY_API_KEY')
# AssemblyAI setup
aai.settings.api_key = assembly_api_key
transcriber = aai.Transcriber()

# Audio recording parameters
sample_rate = 44100  # Sample rate in Hz
channels = 1  # Mono audio
device_id = 2  # Hardcoded device ID for the microphone


def start_recording(duration, device_id, sample_rate, channels):
    print("Recording started... Press the space-bar again to stop recording.")
    return sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, device=device_id)


def stop_recording(recording, filename, channels, sample_rate):
    sd.stop()
    print("Recording stopped.")

    # Save the recording to a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 2 bytes per sample
        wf.setframerate(sample_rate)
        wf.writeframes(np.array(recording * 32767, dtype=np.int16).tobytes())


# Transcribe the recorded audio
def transcribe_audio(filename, transcriber):
    transcript = transcriber.transcribe(filename)
    return transcript.text


def record_and_transcribe(duration=30, sample_rate=44100, channels=1, device_id=2):
    # Temporary file to save the recording
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_filename = temp_file.name

    # Start recording
    recording = start_recording(duration, device_id, sample_rate, channels)

    # Wait for the user to press the space bar to stop recording
    with keyboard.Listener(on_press=lambda key: stop_recording_on_space(key, recording, temp_filename, channels,
                                                                        sample_rate)) as listener:
        listener.join()

    # Transcribe the audio after recording stops
    transcript = transcribe_audio(temp_filename, transcriber)
    return transcript


def stop_recording_on_space(key, recording, temp_filename, channels, sample_rate):
    if key == keyboard.Key.space:
        stop_recording(recording, temp_filename, channels, sample_rate)
        return False  # Stop the listener