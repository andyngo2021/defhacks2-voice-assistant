# **defhacks2-voice-assistant** #

For the 2020 DefHacks Hackathon 11/14-11/15 :D

Running on Python 3.8.5 64-bit

<br>

# **Python Virtual Assistant** #

### **Meet Bob** (or whatever you want to name it) ###
Bob is a pretty basic voice assistant who strives to reach the same level as Siri-sama and Alexa-chan. Unfortunately, he wasn't programmed by someone who really knew what they doing so he can only do super basic tasks :((

*I still love Bob tho <3*

Bob works by using a speech recognition API and listens for **keywords** to figure out what to do. There's a [list of keywords](#cheatsheet) you can refer to down below. :)

<br>

### **What can Bob do?** ###
Not much LOL But here are some of the tasks he can do:
* *Play a song on YouTube*
    * tell Bob to play a song and he'll ask you which one!
    * he'll open up a YouTube page with your song and you can jam out to it with him :D
* *Give you an inspirational quote*
    * You ever write an essay for english but need a baller quote to kick it off or something?? Or maybe you're feeling a bit down in the dumps and need an uplifting quote?
    * Just ask bob to give you a 'quote' and he'll spit out a really nice quote :D
* *Search the Internet for something*
    * want to look at pictures of cows or something else? Tell bob to 'search up' something and he'll do just that!
* *COVID-19 Statistics in the USA*
    * Since COVID-19 is still a super serious thing, Bob can give you some data regarding COVID-19 in the USA if you ask for it
    * Keywords to mention: 'covid or pandemic, data'
* *Give you information about the weather*
    * Tell him to give you 'current' weather data
    * or tell him to give you a 'forecast' for this week's weather
* *Tell you your schedule from Google Calendar*
    * By far my greatest accomplishment LOL
    * ask him for your 'schedule' or for 'upcoming events' and he'll tell you important events that are coming up
* *Create events for you on Google Calendar*
    * My other greatest accomplishment <3
    * tell him that you want to 'add an event' to your schedule and he'll ask you for the event name, starting time, and ending time before adding it to your Google Calendar :D
* *Tell you a joke*
    * ask Bob to tell you a joke and he'll give you a programming joke from the pyjokes module!
    
<br>

<h2 id="cheatsheet"> **Cheat Sheet for Bob's Commands** </h2>
---
You could just look through the code in voice_assistant.py but here's a cool table you could use to get a fast summary of how to use Bob.

Command | Command Description | Keywords Bob Listens For | Example
| :---: | :---: | :---: | :---: |
Play song on YouTube | plays a song on youtube | 'play' and ('music' or 'song') | *"play me a song Bob"*
Get a quote | prints an inspirational quote | 'quote' | *"give me a quote"*
Search the internet | tell Bob to search something up for you | 'search up (what you want to search up)' | *"search up pictures of cows"*
USA COVID-19 Quick Facts | get the latest data regarding COVID in the USA | 'data' and 'covid or pandemic' | *"fetch me data about the pandemic"*
Weather Info | gives you data about weather in MY location | 'weather or forecast' (if you include 'current', he'll give you current weather, if you include 'week or forecast' he gives you the forcase for the week) | *"what's this week's weather like?"*
Google Calendar Upcoming Events | fetch upcoming events from your calendar | 'calendar' or 'upcoming events' or 'schedule' | *"show me my schedule"*
Create Google Calendar Event | create a new event on your calendar | 'add event' and ('calendar' or 'schedule') | *"add an event to my calendar"*
Get a joke | Bob tells you a corny programming joke | 'joke' | *"tell me a joke"*

<br>

## **About the Author** ##
---
Hello! My name is Andy and I'm a high school student from Southern California. This was my first hackathon and I was super pumped to be a part of it! I picked up Python last year and messed around the basics in my free time but I never really built anything cool until now.

### **Backstory** ###
I happened to stumble across a [random YouTube video](https://youtu.be/x8xjj6cR9Nc) one day and thought how cool it would be if I made my own voice assistant in Python. Would it be better than Siri or Alexa? Probably not XD, but I still wanted to give it a shot and see what ideas I could think of within a span of two days. Turns out that the basics in Python don't really teach you how to uses APIs so just ended up spending a lot of time during DefHacks 2.0 to watch a bunch of tutorials on how to use Google's API and how to use the requests module. 

<br>

## **Miscellaneous Stuff** ##

### **Dependencies** ###
pip install these!!
* pyjokes 
* gTTS
* SpeechRecognition
* google-api-python-client

### **APIs Used** ###
* [Google Calendar API](https://developers.google.com/calendar)
    * I needed to do all that Authorization stuff to get my hands on the client credentials
* [YouTube Data API](https://developers.google.com/youtube/v3)
    * Same as the Google Calendar API
* [COVID Data API](https://covid19api.com/)
* [OpenWeatherMap API](https://openweathermap.org/api)
    * Needed to create an account and generate an API key
* [Inspirational Quotes](https://type.fit/api/quotes)

<br>

## **Features I Want To Add in the Future** ##
* get email updates
* make a reminder
* give Bob a voice and let him work just as fast
    * I didn't use the playsound module because my toaster laptop would lag everytime he spoke >.<
* make it more personalized
    * get the user's name, location, etc. to give a more personalized experience
* touch up on the other features that are already built in (there's so many bugs lol)
* maybe use a raspberry pi or some other microcontroller and attach a mic to it
* there's probably more but I can't think properly rn >.<