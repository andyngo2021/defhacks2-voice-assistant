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
            events = self.calendar.events().list(calendarId=calendar_id, pageToken=page_token).execute()
            for event in events['items']:
                print(event)
            page_token = events.get('nextPageToken')
            if not page_token:
                break


cal = GoogleCalendarAPI()
cal.GetEvents(cal.GetCalendarList()[3])
