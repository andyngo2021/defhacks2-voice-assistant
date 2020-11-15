import requests
import json
# class to get weather data from the OpenWeatherMap API


class WeatherAPI:
    def __init__(self):
        #self.key = self.getAPIKey()
        self.key = '76f77d655b85cd7814e1b6fd142aa137'
    
    def getAPIKey(self):
        with open('weatherapikey.txt') as keydata:
            data = keydata.readlines()
            api_key = data[0].strip()
            return str(api_key)
        
    def getData(self):
        lat = '33.7592'
        lon = '-117.9897'
        lang = 'en'
        appid = self.key
        units = 'imperial'
        exclude = 'minutely,alerts,daily,hourly'
        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&lang={lang}&appid={self.key}&units={units}&exclude={exclude}'
        response = requests.get(url).json()
        print(response)
    
a = WeatherAPI()
a.getData()