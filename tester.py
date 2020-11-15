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
                    # try to make it so that it only activates when you print
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
                    print('Took too long to print')
                    # probably don't need to say anything here
            return audio_data

def respond(audio_data):
    audio_data = audio_data.lower()
    if 'add' in audio_data and 'event' in audio_data and 'calendar' in audio_data:
        # add an event to my primary calendar
        # need: title, date, start time, end time
        time_of_day = None # am or pm
        time_of_end = None
        good_to_go = False

        while not good_to_go:
            print('What\'s the occassion?')
            title = listen()
            print('What day does the event happen?')
            date = listen()
            # test cases:
            # 'tomorrow' November 10th, November 10, next friday, in two days, etc...
            year = '2020'
            date = date.split(' ')
            month = date[0]
            day = date[1].strip('th')
            print('When does the event start?')
            start_time = listen()
            # make sure to check if it's AM or PM
            if start_time[-4:] not in ['a.m.', 'p.m.']:
                time_of_day = listen()
            else:
                time_of_day = start_time[-4:]
            start_time = start_time.strip(' ' + time_of_day)
            print('When does the event end?')
            end_time = listen()
            # same as above lol
            if end_time[-4:] not in ['a.m.', 'p.m.']:
                speak('Is that A.M. or P.M.?')
                time_of_end = listen()
            else:
                time_of_end = end_time[-4:]
            end_time = end_time.strip(' ' + time_of_end)
            print('Are the following details correct?')
            print(f'''
                Title = {title}
                Date = {month} {day}, {year}
                Time = {start_time} {time_of_day} - {end_time} {time_of_end}
            ''')
            resp = listen()
            if 'yes' in resp:
                good_to_go = True
            else:
                good_to_go = False

print('ready')
respond(listen())