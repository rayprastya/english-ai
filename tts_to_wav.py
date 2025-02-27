from google.cloud import texttospeech

# Set up Google Cloud credentials
# Make sure to set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the path of your service account key file
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"

def text_to_speech(voice_name, input_text, output_filename):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=input_text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=voice_name.split('-')[0],
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio saved to {output_filename}")

# Call the function to perform text-to-speech and save to a WAV file
# text_to_speech('en-US-Wavenet-D', 'Hello, this is a test.', 'output.wav')
