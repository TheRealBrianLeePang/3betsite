from django.shortcuts import render
from django.http import HttpResponse
import urllib.request
from datetime import date
import json

def addZero(num):
    if len(str(num)) == 1:
        return '0'+str(num)
    else:
        return str(num)

print('Beginning file download with urllib2...')


today = date.today()
year = str(today.year)
month = addZero(today.month)
day = addZero(today.day+1)

games = []

url = 'http://data.nba.net/10s/prod/v1/'+year+month+day+'/scoreboard.json'
print(url)
urllib.request.urlretrieve(url, 'test.json')
with open('test.json') as json_file:
    data = json.load(json_file)
    for p in data['games']:
        print('gameId: ' + p['gameId'])
        games.append(p['gameId'])
        print('')


def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    return HttpResponse(str(games)+"yo")

