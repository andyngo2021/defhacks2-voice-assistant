import requests
import datetime
# class to get weather data from the OpenWeatherMap API


class WeatherAPI:
    
    def __init__(self):
        #self.key = self.getAPIKey()
        self.key = self.getAPIKey()
        self.data = self.getData()
        self.degree = u"\N{DEGREE SIGN}" + 'F'

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
        exclude = 'minutely,alerts,hourly'
        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&lang={lang}&appid={self.key}&units={units}&exclude={exclude}'
        response = requests.get(url).json()
        return response

    def getWeeklyForecast(self):
        response = self.data
        day_count = 0
        forecast = ''
        for day in response['daily']:
            max_temp = day['temp']['max']
            min_temp = day['temp']['min']
            weather_desc = day['weather'][0]['description']
            calculate_date = datetime.datetime.today() + datetime.timedelta(days=day_count)
            weekday = calculate_date.strftime('%A')
            formatted_date = calculate_date.strftime('%m/%d/%y')
            date = f'{weekday} {formatted_date}'
            data_weather = f'Max: {max_temp}{self.degree}, Min: {min_temp}{self.degree}, Weather: {weather_desc}'
            forecast += date + '\n'
            forecast += data_weather + '\n'
            day_count += 1
        return forecast

    def getCurrentWeather(self):
        response = self.data
        current_temp = response['current']['temp']
        current_description = response['current']['weather'][0]['description']
        current_weather = f'The current temperature is {current_temp}{self.degree}. Weather: {current_description}'
        return current_weather