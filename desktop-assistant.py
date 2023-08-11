import speech_recognition as sr
import pyttsx3
import os
import openai

openai.api_key = "put your key here"

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

conversation = ""
user_name = "Dan"
bot_name = "John"

while True:
    with mic as source:
        print("\nListening...")
        r.adjust_for_ambient_noise(source, duration=0.1)
        audio = r.listen(source)
    print("No longer listening")

    try:
        user_input = r.recognize_google(audio)
    except sr.UnknownValueError:
        continue

    prompt = user_name + ": " + user_input + "\n" + bot_name + ": "
    conversation += prompt

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=conversation,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    response_str = response.choices[0].text.replace("\n", "")
    response_str = response_str.split(user_name + ":", 1)[0].split(bot_name + ":", 1)[0]

    conversation += response_str + "\n"
    print(response_str)

    engine.say(response_str)
    engine.runAndWait()
