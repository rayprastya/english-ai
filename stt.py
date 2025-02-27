import os
from google.cloud import speech
import wave

# Set up Google Cloud credentials
# Make sure to set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the path of your service account key file
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"

def recognize_from_microphone(filename):
    client = speech.SpeechClient()

    with wave.open(filename, 'rb') as audio_file:
        content = audio_file.readframes(audio_file.getnframes())

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=audio_file.getframerate(),
        language_code="en-US"
    )

    response = client.recognize(config=config, audio=audio)

    if response.results:
        recognized_text = response.results[0].alternatives[0].transcript
        print("Recognized: {}".format(recognized_text))
    else:
        print("No speech could be recognized")

    return recognized_text if response.results else ""

# recognize_from_microphone(filename)