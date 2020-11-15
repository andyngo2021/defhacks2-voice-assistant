import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import googleapiclient.discovery 

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
        page_token = None
        while True:
            events = self.calendar.events().list(calendarId=calendar_id, pageToken=page_token, singleEvents=True, orderBy='startTime').execute()
            for event in events['items']:
                # print(event)
                start_time = self.FormatTime(event['start']['dateTime'])
                end_time = self.FormatTime(event['end']['dateTime'])
                time_frame = self.GetTimeFrame(start_time, end_time)
                print(f"{event['summary']} | {time_frame} | {event['location']}")
            page_token = events.get('nextPageToken')
            if not page_token:
                break

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
        elif int(time[0:2] == 00):
            formatted_hour = 12
            time = formatted_hour + time[2:]
            
        formatted_data = month, day, year, time, time_of_day
        return formatted_data

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

    def CheckIfNotHappenedYet(self, event):
        # want to use some date module to check if an event has occured or not
        pass

    def CompareTwoTimes(self, time_1, time_2):
        # compare two times to see which one came first
        pass
        


cal = GoogleCalendarAPI()
cal.GetEvents(cal.GetCalendarList()[3])
