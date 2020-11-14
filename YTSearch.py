from googleapiclient.discovery import build
import webbrowser

# Using this class to communicate with YouTube or doing anything relating to YouTube

class YouTubeAPI:
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=self.getAPIKey())
    
    def getAPIKey(self):
        with open('youtubeapikey.txt') as keydata:
            data = keydata.readlines()
            api_key = data[0].strip()
            return str(api_key)

    def SearchForVideo(self, title):
        request = self.youtube.search().list(
            part="snippet",
            maxResults=1,
            q=f"{title}"
        )
        response = request.execute()
        id = response["items"][0]["id"]["videoId"]
        return self.GetYouTubeURL(id)

    def GetYouTubeURL(self, id):
        return f'https://youtu.be/{id}'
