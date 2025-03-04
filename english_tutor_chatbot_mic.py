import os
import google.generativeai as genai
import pronounce_assessment_mic
import tts
import string

option = 6
voice_name = 'en-US-JennyMultilingualNeural'
wrong_pronounce = []
user_name = None

#-------------- INITIALIZE GEMINI --------------
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')
output_filename = 'output.wav'

def get_completion_from_messages(messages, model='gemini-1.5-flash', temperature=0):
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
    
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=temperature
        )
    )
    return response.text

def chat():
    #-------------- GETTING USER INPUT --------------
    prompt = ''

    #-------------- VARIABLE TO GET AND SET USERNAME --------------
    global user_name  

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
    while prompt != 'exit':
        prompt = input('User: ')
        prompt = prompt.lower()

        #-------------- EVALUATING USER INPUT -------------- 
        tts.text_to_speech(voice_name, prompt)
        results = pronounce_assessment_mic.pronunciation_assessment_from_microphone('en-US', prompt)
        for word in results.words:
            acc = word.accuracy_score
            while acc < 50:
                print('You mispronounced ', word.word)
                # wrong_pronounce.append(word.word)
                tts.text_to_speech(voice_name, word.word)
                re_pronounce = pronounce_assessment_mic.pronunciation_assessment_from_microphone('en-US', word.word)
                for i in re_pronounce.words:
                    acc = i.accuracy_score

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
        # print('Context: ', context)

chat()
