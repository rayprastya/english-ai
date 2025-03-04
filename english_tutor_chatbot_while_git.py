import pronounce_assessment_file
import intonation
import tts_to_wav
import google.generativeai as genai
import stt
import tts 
import os 

voice_name = 'en-US-Standard-C'
wrong_pronounce = []
user_name = None
user_input_text = ''

#-------------- GETTING USER INPUT --------------
option = 6
# user_input_audio = 'D:\\GPT\\GPT\\english_tutoring_chatbot_shared_final\\i_am_good_how_are_you.wav'
# user_input_text = 'nothing much what about you'
base_path = os.path.dirname(os.path.abspath(__file__))
user_input_audio = os.path.join(base_path, 'i_am_good_how_are_you.wav')

#-------------- INITIALIZE GEMINI --------------
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

def get_completion_from_messages(messages, temperature=0):
    # Convert OpenAI message format to Gemini format
    prompt = ""
    for message in messages:
        role = message['role']
        content = message['content']
        if role == 'system':
            prompt += f"Instructions: {content}\n"
        elif role == 'user':
            prompt += f"User: {content}\n"
        elif role == 'assistant':
            prompt += f"Assistant: {content}\n"
    
    response = gemini_model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=temperature
        )
    )
    return response.text

while user_input_text != 'exit':
    #-------------- MISPRONOUNCED WORDS --------------
    mispronounced_words = []
    user_input_text = stt.recognize_from_microphone(user_input_audio)
    print(user_input_text)
    output_filename = 'output.wav'

    #-------------- CHATBOT CONTEXT --------------
    if option == 1:
        context = [
            {'role': 'system', 'content': 'you are at a professional event engaging with people at a sophisticated and professional level. keep the conversation brief'}
        ]
    elif option == 2:
        context = [
            {'role': 'system', 'content': 'you are a medical MD intern at a hospital talking to a patient. continue the conversation accordingly.'}
        ]
    elif option == 3:
        context = [
            {'role': 'system', 'content': 'you are inteviewing a potential candidate for a job. keep the conversation brief'}
        ]
    elif option == 4:
        context = [
            {'role': 'system', 'content': 'you are meeting a friend at a coffee break. keep the conversation lively'}
        ]
    elif option == 5:
        context = [
            {'role': 'system', 'content': 'you are an airline assistant talking to a client. keep the conversation professional and brief'}
        ]
    elif option == 6:
        context = [
            {'role': 'system', 'content': 'you are an event planner talking to a client regarding an upcomng event. keep the conversation lively, professional and brief'}
        ]

    #-------------- CHATBOT FUNCTION -------------
    prompt = user_input_text
    user_input_audio = user_input_audio
    option = option

    #-------------- EVALUATING USER INPUT -------------- 
    accuracy, completeness, fluency, per_word_pronounciation_evaluation, final_words = pronounce_assessment_file.pronunciation_assessment_continuous_from_file(user_input_audio, 'en-US', prompt)
    pitch_input_text = prompt.split(' ')
    pitch_per_word, overall_pitch = intonation.pitch(pitch_input_text, user_input_audio)
    print(f'Accuracy: {accuracy} \nCompleteness: {completeness} \nFluency: {fluency} \nPer Word Evaluation: {per_word_pronounciation_evaluation} \nPitch Per Word: {pitch_per_word} \nOverall Pitch: {overall_pitch}')
    print('Final Words:', final_words)
    for word in final_words:
        # Check if the word was mispronounced (error_type is not None)
        if word['error_type'] != 'None':
            mispronounced_words.append(f"{word['word']}: mispronounced")
            print('\nYou mispronounced:', word['word'])
            # print(mispronounced_words)
    
    #-------------- GETTING AND RETURNING USERNAME -------------- 
    if 'what is my name' in prompt:
        if user_name:
            response=  'Your name is ' + user_name
        else: 
            response =  'I don\'t know your name. You can tell me by saying: my name is [Your Name]'
    elif 'my name is' in prompt:
        user_name = prompt.split("my name is")[1].strip() 
        response =  'Nice to meet you ' + user_name + '!'
    

    #-------------- GETTING CHATBOT RESPONSE --------------
    context.append({'role': 'user', 'content': f"{prompt}"})
    # print('User: ', prompt)
    response = get_completion_from_messages(context)
    context.append({'role': 'assistant', 'content': f"{response}"})
    print('Assistant:', response)

    #-------------- TEXT TO SPEECH CHATBOT RESPONSE --------------
    tts.text_to_speech(voice_name, response, output_filename)

    #-------------- PRINTING CONTEXT --------------
    print('Context: ', context)
