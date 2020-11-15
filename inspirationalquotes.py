import requests
import random

def getInspirationalQuote():
    req = requests.get('https://type.fit/api/quotes')
    quote_data = random.choice(req.json())
    quote = quote_data['text']
    author = quote_data['author']
    return f'"{quote}" -{author}'