import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import googleapiclient.discovery 
import datetime

class CalendarEvent:
    def __init__(self, title, start, end, location=None):
        self.title = title
        self.start = start # tuple (month, day, year, time, time_of_day)
        self.end = end
        self.location = location
        self.time_frame = self.GetTimeFrame(self.start, self.end)

    def __str__(self):
        return f"{self.title} | {self.time_frame} | {self.location}"

    def GetTimeFrame(self, start, end):
        # both start and end should be in the same form as formatted_data
        formatted_timeframe = None
        sameDay = False
        start_month, start_day, start_year, start_time, start_time_of_day = start
        end_month, end_day, end_year, end_time, end_time_of_day = end
        if start_month == end_month and start_day == end_day and end_year == end_year:
            sameDay = True
        # if same day: 11/14/2020 (08:30 AM - 09:00 AM)
        # else: 11/14/2020 (08:30 AM) - 11/16/2020 (09:30 AM) 
        if sameDay:
            formatted_timeframe = f'{start_month}/{start_day}/{start_year} ({start_time} {start_time_of_day} - {end_time} {end_time_of_day})'
        else:
            formatted_timeframe = f'{start_month}/{start_day}/{start_year} ({start_time} {start_time_of_day}) - {end_month}/{end_day}/{end_year} ({end_time} {end_time_of_day})'
       
        return formatted_timeframe

class GoogleCalendarAPI:
    def __init__(self):
        self.credentials = None
        self.calendar = None
        self.LoadCredentials()
        
    def LoadCredentials(self):
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.credentials = pickle.load(token)
        
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json',
                    scopes=['https://www.googleapis.com/auth/calendar']
                )
                flow.run_local_server(port=8080, prompt='consent', authorization_prompt_message='')
                self.credentials = flow.credentials
                with open('token.pickle', 'wb') as f:
                    pickle.dump(self.credentials, f)
        
        self.calendar = googleapiclient.discovery.build('calendar', 'v3', credentials=self.credentials)

    def GetCalendarList(self):
        page_token = None
        calendarIDs = []
        while True:
            calendars = self.calendar.calendarList().list(pageToken=page_token).execute()
            for calendar in calendars['items']:
                calendarIDs.append((calendar['summary'], calendar['id']))
            page_token = calendars.get('nextPageToken')
            if not page_token:
                break
        return calendarIDs # (name, id)

    def GetEvents(self, calendar_info): # calendar info contains name, and ID
        calendar_name, calendar_id = calendar_info
        calendar_events = []
        page_token = None
        while True:
            events = self.calendar.events().list(calendarId=calendar_id, pageToken=page_token, singleEvents=True, orderBy='startTime').execute()
            for event in events['items']:
                # title, start, end, location=None 
                title = event['summary']
                start = self.FormatTime(event['start']['dateTime'])
                end = self.FormatTime(event['end']['dateTime'])
                location = event['location']
                event_data = CalendarEvent(title, start, end, location)
                if self.CheckIfNotHappenedYet(event_data):
                    calendar_events.append(event_data)

            page_token = events.get('nextPageToken')
            if not page_token:
                break
        return calendar_events
    
    def PrintCalendarEvents(self, calendar_events):
        for event in calendar_events:
            print(event)
    
    def FormatTime(self, data):
        # given in this format: 2020-11-14T08:30:00-08:00
        #                       0123456789
        year = data[0:4]
        month = data[5:7]
        day = data[8:10]
        time = data[11:16] # 08:30
        time_of_day = 'AM'
        if int(time[0:2]) > 12:
            time_of_day = 'PM'
            formatted_hour = str(int(time[0:2])%12).zfill(2)
            time = formatted_hour + time[2:]
        elif time[0:2] == '00':
            formatted_hour = '12'
            time = formatted_hour + time[2:]
            
        formatted_data = month, day, year, time, time_of_day
        return formatted_data

    def GetCurrentTime(self):
        current_time = str(datetime.datetime.now())
        # 2020-11-15 01:32:16.826450
        year = current_time[0:4]
        month = current_time[5:7]
        day = current_time[8:10]
        time = current_time[11:16]
        time_of_day = datetime.datetime.now().strftime('%p')
        
        formatted_data = month, day, year, time, time_of_day
        # return it in a similar way as formatted data
        return formatted_data

    def CheckIfNotHappenedYet(self, event):
        # want to use some date module to check if an event has occured or not
        # the CompareTwoTimes will return true IF first event occurs before the next event
        return self.CompareTwoTimes(self.GetCurrentTime(), event.start)


    def CompareTwoTimes(self, time_1, time_2):
        # compare two times to see which one came first
        # helper function for the CheckIfNotHappeendYet function
        month1, day1, year1, time1, time_of_day1 = time_1
        month2, day2, year2, time2, time_of_day2 = time_2
        if month1==month2 and day1==day2 and year1==year2:
            if (time_of_day1 <= time_of_day2):
                if (time1 <= time2):
                    return True
        return False
        


# cal = GoogleCalendarAPI()
# cal.PrintCalendarEvents(cal.GetEvents(cal.GetCalendarList()[3]))
