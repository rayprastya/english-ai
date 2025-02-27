from google.cloud import speech
import pyaudio
import wave
import time
import string
import difflib

wrong_pronounce = []
is_listening = False

def record_audio(filename, duration=5, sample_rate=16000, channels=1):
    """Records audio from the microphone and saves it to a file."""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=channels, rate=sample_rate, input=True, frames_per_buffer=1024)
    frames = []

    print("Recording...")
    for _ in range(0, int(sample_rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)
    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

def pronunciation_assessment_from_microphone(language, reference):
    """Performs one-shot pronunciation assessment asynchronously with input from microphone."""

    filename = "temp_audio.wav"
    record_audio(filename)

    client = speech.SpeechClient()

    with wave.open(filename, 'rb') as audio_file:
        content = audio_file.readframes(audio_file.getnframes())

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=audio_file.getframerate(),
        language_code=language,
        enable_word_time_offsets=True
    )

    response = client.recognize(config=config, audio=audio)

    recognized_words = []
    durations = []
    per_word_pronounciation_evaluation = []

    for result in response.results:
        for word_info in result.alternatives[0].words:
            recognized_words.append(word_info.word)
            durations.append(word_info.end_time.total_seconds() - word_info.start_time.total_seconds())

    reference_words = [w.strip(string.punctuation) for w in reference.lower().split()]

    enable_miscue = True
    if enable_miscue:
        diff = difflib.SequenceMatcher(None, reference_words, [x.lower() for x in recognized_words])
        final_words = []
        for tag, i1, i2, j1, j2 in diff.get_opcodes():
            if tag in ['insert', 'replace']:
                for word in recognized_words[j1:j2]:
                    final_words.append({'word': word, 'error_type': 'Insertion'})
            if tag in ['delete', 'replace']:
                for word_text in reference_words[i1:i2]:
                    final_words.append({'word': word_text, 'error_type': 'Omission'})
            if tag == 'equal':
                final_words += [{'word': word, 'error_type': 'None'} for word in recognized_words[j1:j2]]
    else:
        final_words = [{'word': word, 'error_type': 'None'} for word in recognized_words]

    final_accuracy_scores = []
    for word in final_words:
        if word['error_type'] == 'Insertion':
            continue
        else:
            final_accuracy_scores.append(100)
    accuracy_score = sum(final_accuracy_scores) / len(final_accuracy_scores)
    fluency_score = sum(durations) / len(durations)
    completeness_score = len([w for w in final_words if w['error_type'] == "None"]) / len(reference_words) * 100
    completeness_score = completeness_score if completeness_score <= 100 else 100

    for idx, word in enumerate(final_words):
        per_word_pronounciation_evaluation.append(f'word {idx + 1}: {word["word"]}, error type: {word["error_type"]}')

    print('Evaluating Results...')
    print('  Pronunciation Assessment Result:')
    print('    Accuracy score: {}, Completeness score : {}, FluencyScore: {}'.format(
        accuracy_score, completeness_score, fluency_score
    ))
    print('  Word-level details:')
    for idx, word in enumerate(final_words):
        print('    {}: word: {}, error type: {};'.format(
            idx + 1, word['word'], word['error_type']
        ))

    return accuracy_score, completeness_score, fluency_score, per_word_pronounciation_evaluation, final_words