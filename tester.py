from gtts import gTTS
import playsound
import speech_recognition as sr

recognizer = sr.Recognizer()

def listen(question=None):
        with sr.Microphone() as source:
            audio_data = None
            while audio_data is None:
                try:
                    audio = recognizer.listen(source, phrase_time_limit=7)
                    # still need to tweak the settings a bit 
                    # try to make it so that it only activates when you speak
                    # timeout = how long the microphone listens for a prompt
                    # phrase_time_limit = how long the microphone will listen for (my mic is kinda bad and picks up a lot of noise)
                    audio_data = recognizer.recognize_google(audio)
                    # using google's api to convert the audio to a string
                    print(f'You said: {audio_data}') # so the user can get feedback on what the voice assistant heard
                except sr.UnknownValueError:
                    print('Sorry, I didn\'t get that. Could you please repeat what you said?')
                except sr.RequestError:
                    print('Sorry, my speech service is currently unavailable. Please try again.')
                except sr.WaitTimeoutError:
                    print('Took too long to speak')
                    # probably don't need to say anything here
            return audio_data

print('ready')
a = listen()