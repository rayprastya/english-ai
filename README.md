# English Language Tutoring Chatbot with Multiple Roles

## Overview

This project integrates a chatbot with an English Language Tutor, providing users with language tutoring features, including pronunciation assessment, fluency evaluation, pitch analysis, mispronounced words correction. The chatbot is capable of engaging in conversations based on different contexts, enhancing the user experience.

## Features

- Pronunciation assessment with detailed metrics
- Fluency evaluation and scoring
- Pitch analysis per word and overall
- Contextual chatbot interaction
- Mispronounced words recognition and correction
- Name recognition and personalization
- Speech quality scoring with weighted metrics
- Correct pronunciation percentage calculation

## Options 
Choose from different chatbot contexts:

- `Option_01`: Professional event
- `Option_02`: Medical intern-patient conversation
- `Option_03`: Job interview
- `Option_04`: Coffee break with a friend
- `Option_05`: Airline assistant-client conversation
- `Option_06`: Event planner-client conversation (lively, professional, and brief)

## Dependencies

Ensure you have the necessary dependencies installed by running the following command:

```bash
pip install -r requirements.txt
```

## Environment Setup

1. Set up Google Cloud credentials:
   - Place your Google Cloud service account JSON file in a secure location
   - Set the environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"
   ```

2. Set up Gemini API:
   - Get your Gemini API key
   - Set the environment variable:
   ```bash
   export GEMINI_API_KEY="your-gemini-api-key"
   ```

## Usage 
The English language tutoring chatbot provides the following functionalities:
- Provide user input through audio and text
- The system evaluates:
  - Pronunciation accuracy
  - Speech completeness
  - Fluency metrics
  - Pitch analysis per word
  - Overall speech quality score
- Engage in contextual chatbot conversations
- Chatbot recognizes and responds to user names
- The system identifies mispronounced words and provides feedback

### Running the Chatbot

1. To interact with the chatbot through audio files:
```python
python english_tutor_chatbot_while_git.py
```

2. To use the chatbot in function mode:
```python
python english_tutor_chatbot_function_git.py
```

3. To interact with the chatbot through microphone:
```python
python english_tutor_chatbot_mic.py
```

### How it Works

The chatbot operates in the following way:
1. User provides input (text or audio)
2. System evaluates the speech metrics:
   - Accuracy (40% of final score)
   - Completeness (30% of final score)
   - Fluency (20% of final score)
   - Pronunciation (10% of final score)
3. Generates detailed feedback including:
   - Speech quality score
   - Correct pronunciation percentage
   - Per-word pronunciation evaluation
   - Pitch analysis
4. Provides contextual responses based on the chosen role
5. Continues the conversation until the user types 'exit'

## Acknowledgments
- This project utilizes Google's Gemini API for conversation generation
- Google Cloud Text-to-Speech for voice synthesis
- Google Cloud Speech-to-Text for speech recognition
- Google Cloud Speech for pronunciation assessment

