import speech_recognition as sr
import time
import os
import playsound
import random
from gtts import gTTS
import webbrowser
# make sure to import the youtube class here later

# class for the voice assistant goes here

'''
Stuff to do:
    add speech to text
    Basic command ideas:
        - what's my name
        - search the internet
        - play music from youtube
        - check for unread emails
        - make a reminder
        - add calendar events
        - weather api 
        - COVID facts bc why not
        - canvas api for schoolwork >.<
'''

class VoiceAssistant:
    def __init__(self, name, mode):
        self.name = name
        self.recognizer = sr.Recognizer()
        
        self.mode = mode
        if self.mode == 1:
            self.speak = self.speakText
        else:
            self.speak = self.speakVoice

    # my laptop is kind of a toaster and it takes a while for the speech to load, so there's a text option for faster response
    def speakText(self, text):
        print(text)

    def speakVoice(self, text):
        pass
    
    def listen(self, question=None):
        with sr.Microphone() as source:
            if question:
                self.speak(question)
            audio_data = None
            while audio_data is None:
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    # timeout = how long the microphone listens for a prompt
                    # phrase_time_limit = how long the microphone will listen for (my mic is kinda bad and picks up a lot of noise)
                    audio_data = self.recognizer.recognize_google(audio)
                    # using google's api to convert the audio to a string
                    print(f'You said: {audio_data}') # so the user can get feedback on what the voice assistant heard
                except sr.UnknownValueError:
                    self.speak('Sorry, I didn\'t get that. Could you please repeat what you said?')
                except sr.RequestError:
                    self.speak('Sorry, my speech service is currently unavailable. Please try again.')
                except sr.WaitTimeoutError:
                    self.speak('Took too long to speak')
                    # probably don't need to say anything here
            return audio_data

    def respond(self, audio_data):
        audio_data = audio_data.lower() # standardize the string, probably other things i can do to make it better
        if 'hello' in audio_data:
            self.speak('Hello World!')

    def run(self):
        self.speak('Hello, how can I help you?')
        while True:
            print('Waiting for further instructions...') # Just so i can see if the bot is actually listening
            speech_data = self.listen()
            self.respond(speech_data)


bob = VoiceAssistant('Bob', 1)
bob.run()