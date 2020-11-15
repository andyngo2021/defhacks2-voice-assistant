import requests

def USACOVID():
    url = 'https://api.covid19api.com/summary'
    resp = requests.get(url).json()["Countries"][181]   # 181 is the code for America

    data = f'''
    Here is data regarding COVID-19 in the United States of America as of {resp['Date']}:
    New Confirmed Cases: {resp['NewConfirmed']}
    Total Confirmed Cases: {resp['TotalConfirmed']}
    New Deaths: {resp['NewDeaths']}
    Total Deaths: {resp['TotalDeaths']}
    New Recoveries: {resp['NewRecovered']}
    Total Recoveries: {resp['TotalRecovered']}
    '''
    return data