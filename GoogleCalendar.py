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
        return f"{self.title.strip()} | {self.time_frame} | {self.location}"

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

    def GetEvents(self, all_calendars): # calendar info contains name, and ID
        # print(all_calendars)
        calendar_events = []
        for calendar_info in all_calendars:
            calendar_name, calendar_id = calendar_info
            page_token = None
            while True:
                events = self.calendar.events().list(calendarId=calendar_id, pageToken=page_token, singleEvents=True, orderBy='startTime').execute()
                for event in events['items']:
                    # print(event)
                    # title, start, end, location=None 
                    title = event['summary']
                    try:
                        start = self.FormatTime(event['start']['dateTime'])
                        end = self.FormatTime(event['end']['dateTime'])
                    except:
                        start = None
                        end = None
                    location = None
                    try:
                        location = event['location']
                    except:
                        location = ''
                    event_data = CalendarEvent(title, start, end, location)
                    # print(event_data)
                    if self.CheckIfNotHappenedYet(event_data):
                        calendar_events.append(event_data)
                        # print(f'Amount of upcoming events: {len(calendar_events)}')

                page_token = events.get('nextPageToken')
                if not page_token:
                    break
        # sort here
        calendar_events = sorted(calendar_events, key=self.SortingKeyForTimes)
        return calendar_events
    
    def SortingKeyForTimes(self, event):
        # input = formatted(month, day, year, time, time_of_day)
        # return it in 24 hour time
        time = event.start
        month = time[0]
        day = time[1]
        year = time[2]
        hour_min = time[3]
        time_of_day = time[4]
        if time_of_day == 'p.m.' and int(hour_min[0:2]) < 12:
            hour = str(int(hour_min[0:2])+12)
            hour_min = hour + hour_min[2:]
        if time_of_day == 'a.m.' and int(hour_min[0:2]) == 12:
            hour = '00'
            hour_min = hour + hour_min[2:]
        return year, month, day, hour_min
            

    def PrintCalendarEvents(self, calendar_events):
        for event in calendar_events:
            print(event)
    
    def GetUpcomingEvents(self):
        calendars = self.GetCalendarList()
        target = [calendars[0], calendars[3]]
        self.PrintCalendarEvents(self.GetEvents(target))

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
        if int(time[0:2]) > 12:
            formatted_hour = str(int(time[0:2])%12).zfill(2)
            time = formatted_hour + time[2:]
        time_of_day = datetime.datetime.now().strftime('%p')
        
        formatted_data = month, day, year, time, time_of_day
        # return it in a similar way as formatted data
        return formatted_data

    def CheckIfNotHappenedYet(self, event):
        # want to use some date module to check if an event has occured or not
        # the CompareTwoTimes will return true IF first event occurs before the next event
        # print(f'Comparing now {self.GetCurrentTime()} and {event.start}')
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

    def ConvertMonthToInt(self, month):
        month = month.lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        number = str(months.index(month)+1).zfill(2)
        return number

    
    def GetDateTimeFormat(self, month, day, year, time, time_of_day):
        # return something that looks like this 2015-05-28T09:00:00-08:00
        minus = '-08:00' # subtract 8 hours from UTC to get PST
        month = month.zfill(2)
        day = day.zfill(2)
        if len(time) == 1:
            # if it's like just a single digit i want to add a 0 in front
            time = time.zfill(2)
        if ':' not in time:
            time += (':00')
        if time_of_day == 'p.m.':
            # 04:43
            time = str(int(time[0:2])+12) + time[2:]
            # 16:43
        if time[0:2] == '12' and time_of_day == 'a.m.':
            time = '00' + time[2:]
        
        formatted = f'{year}-{month}-{day}T{time}:00{minus}'
        return formatted
        


        formatted = f'{year}-{month}-{day}T{time}:00{minus}'
        pass

    def MakeNewEvent(self, title, month, day, year, start_time, time_of_day, end_time, time_of_end):
        month = self.ConvertMonthToInt(month)
        event_data = {
            'summary': title,
            'start': {
                'dateTime': self.GetDateTimeFormat(month, day, year, start_time, time_of_day)
            },
            'end': {
                'dateTime': self.GetDateTimeFormat(month, day, year, end_time, time_of_end)
            }
        }
        event = self.calendar.events().insert(calendarId='primary', body=event_data).execute()
        print('Event created: %s' % (event.get('htmlLink')))
        
    


# cal = GoogleCalendarAPI()
# cal.PrintCalendarEvents(cal.GetEvents(cal.GetCalendarList()[3]))
