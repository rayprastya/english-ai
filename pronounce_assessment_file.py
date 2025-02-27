from google.cloud import speech
import difflib
import json
import wave
import time
import string

# Set up Google Cloud credentials
# Make sure to set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the path of your service account key file
# export GOOGLE_APPLICATION_CREDENTIALS="/Users/rayprastya/project/tutor/aiproject/EnglishLanguageTutorChatbot/stellar-smoke-398203-9f9aaeb00229.json"

def pronunciation_assessment_continuous_from_file(filename, language, reference_text):
    """Performs continuous pronunciation assessment asynchronously with input from an audio file."""

    client = speech.SpeechClient()

    # Load audio file
    with wave.open(filename, 'rb') as audio_file:
        content = audio_file.readframes(audio_file.getnframes())

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=audio_file.getframerate(),
        language_code=language,
        enable_word_time_offsets=True
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=90)

    recognized_words = []
    fluency_scores = []
    durations = []
    per_word_pronounciation_evaluation = []

    for result in response.results:
        for word_info in result.alternatives[0].words:
            recognized_words.append(word_info.word)
            durations.append(word_info.end_time.total_seconds() - word_info.start_time.total_seconds())

    reference_words = [w.strip(string.punctuation) for w in reference_text.lower().split()]

    # For continuous pronunciation assessment mode, the service won't return the words with `Insertion` or `Omission`
    # even if miscue is enabled.
    # We need to compare with the reference text after received all recognized words to get these error words.
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

    # We can calculate whole accuracy by averaging
    final_accuracy_scores = []
    for word in final_words:
        if word['error_type'] == 'Insertion':
            continue
        else:
            final_accuracy_scores.append(100)  # Assuming 100% accuracy for recognized words
    accuracy_score = sum(final_accuracy_scores) / len(final_accuracy_scores)
    # Re-calculate fluency score
    fluency_score = sum(durations) / len(durations)
    # Calculate whole completeness score
    completeness_score = len([w for w in final_words if w['error_type'] == "None"]) / len(reference_words) * 100
    completeness_score = completeness_score if completeness_score <= 100 else 100

    for idx, word in enumerate(final_words):
        per_word_pronounciation_evaluation.append(f'word {idx + 1}: {word["word"]}, error type: {word["error_type"]}')

    return accuracy_score, completeness_score, fluency_score, per_word_pronounciation_evaluation, final_words

# pronunciation_assessment_continuous_from_file(filename, language, reference_text)