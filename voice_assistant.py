import time
import os
import random
import webbrowser
# need to pip install
import pyjokes
from gtts import gTTS
import playsound
import speech_recognition as sr
# custom written modules
from YTSearch import YouTubeAPI
from inspirationalquotes import getInspirationalQuote
from COVIDstats import USACOVID
from weatherapi import WeatherAPI


# class for the voice assistant goes here

'''
Stuff to do:
    add speech to text
    Basic command ideas:
        - check for unread emails
        - make a reminder
        - add calendar events
        - weather api 
        - COVID facts bc why not
        - canvas api for schoolwork >.<
'''

'''
Stuff that's "done" or can be touched up on later:
    - search the internet
    - play music from youtube
    - give me an inspirational quote lol
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
            # not sure if i still need or want to keep the question argument
            if question:
                self.speak(question)
            audio_data = None
            while audio_data is None:
                try:
                    audio = self.recognizer.listen(source, phrase_time_limit=10)
                    # still need to tweak the settings a bit 
                    # try to make it so that it only activates when you speak
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

        # add internet searching with webbrowser module
        elif 'search up' in audio_data:
            keywords = audio_data.split()[2:]
            # the first two words are probably 'search up', so we just need to look for whatever the user says afterwards
            # kind of fragile looking code tho LOL
            keywords = ' '.join(keywords) # to turn it from a list into a string
            url = 'https://google.com/search?q='
            if 'picture' in audio_data:
                url = 'https://www.google.com/search?tbm=isch&q='
            url += keywords # append keywords at the end
            webbrowser.get().open(url)

        # add play music with youtube
        elif 'play' in audio_data and ('song' in audio_data or 'music' in audio_data):
            self.speak('What do you want me to play?')
            song_information = self.listen()
            # need to clean the song_information string later to remove (play and by)
            yt_player = YouTubeAPI()
            videoURL = yt_player.SearchForVideo(song_information)
            webbrowser.get().open(videoURL)

        # get a joke from pyjokes
        elif 'tell me a joke' in audio_data:
            self.speak(pyjokes.get_joke())
        
        elif 'quote' in audio_data:
            self.speak(getInspirationalQuote())
        
        elif 'data' in audio_data and ('covid' in audio_data or 'pandemic' in audio_data):
            self.speak(USACOVID())

        elif 'weather' in audio_data or 'forecast' in audio_data:
            w = WeatherAPI()
            if 'forecast' in audio_data or 'week' in audio_data:
                self.speak(w.getWeeklyForecast())
            elif 'current' in audio_data:
                self.speak(w.getCurrentWeather())

        # might remove later idk
        elif 'quit' in audio_data:
            exit()
        


    def run(self):
        self.speak('Hello, how can I help you?')
        while True:
            print('Waiting for further instructions...') # Just so i can see if the bot is actually listening
            speech_data = self.listen()
            self.respond(speech_data)


bob = VoiceAssistant('Bob', 1)
bob.run()